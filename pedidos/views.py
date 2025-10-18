from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import Cliente, Pedido, Productos, Envio, Categoria, DetallePedido
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache   
from django.views.decorators.http import require_POST
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Max
from django.db.models.functions import TruncDate
from django.utils import timezone
from .forms import ClienteForm, PedidoForm, ProductoForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime, timedelta
from json_response import JsonResponse, json
from .serializers import StatsSerializer



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:  
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'pedidos/login.html')

@require_POST
def logout_view(request):
    logout(request)
    response = redirect('login') 
    response.delete_cookie('sessionid')
    response.delete_cookie('csrftoken')
    return response

def get_stats(request):
    hoy = timezone.now().date()
    
    # 1. Consultas optimizadas
    fecha_reciente = Pedido.objects.aggregate( ultima_fecha=Max(TruncDate('fecha_orden')))['ultima_fecha']
    
    # 2. Órdenes recientes (simplificado)
    ordenes_recientes = 0
    if fecha_reciente:
        fecha_reciente_date = fecha_reciente.date() if hasattr(fecha_reciente, 'date') else fecha_reciente
        ordenes_recientes = Pedido.objects.filter(fecha_orden__date=fecha_reciente_date).count()

    # 3. Mejores clientes (directo a lista)
    mejores_clientes_data = list(Pedido.objects
        .values('cliente_id', 'cliente__nombre')
        .annotate(total=Count('orden_id'))
        .order_by('-total')[:10]
    )
    # 4. Otras métricas
    ordenes_hoy = Pedido.objects.filter(fecha_orden__date=hoy).count()
    
    inicio_mes = hoy.replace(day=1)
    ordenes_mensual = Pedido.objects.filter(fecha_orden__date__gte=inicio_mes).count()
    
    # 5. Series diarias
    fecha_limite = hoy - timedelta(days=30)
    series_diarias_data = [
        {
            'fecha': item['fecha_orden__date'].strftime("%Y-%m-%d"), 
            'total': item['total']
        }
        for item in Pedido.objects
            .filter(fecha_orden__date__gte=fecha_limite)
            .values('fecha_orden__date')
            .annotate(total=Count('orden_id'))
            .order_by('fecha_orden__date')
    ]
    
    # 6. Datos para el serializer
    raw_data = {
        'ordenes_hoy': ordenes_hoy,
        'ordenes_recientes': ordenes_recientes,
        'ordenes_mensual': ordenes_mensual,
        'fecha_reciente': fecha_reciente,
        'mejores_clientes': mejores_clientes_data,
        'series_diarias': series_diarias_data,

    }
    
    # 7. Serializar (¡esto es lo importante!)
    serializer = StatsSerializer(data=raw_data)
    serializer.is_valid(raise_exception=True)
    
    return serializer.data

@never_cache
@login_required
def home(request):
    stats_data = get_stats(request)
    
    # Contexto listo para el template
    context = {
        **stats_data,
        'mejoresclientes_json': json.dumps(stats_data['mejores_clientes']),
        'series_diarias_json': json.dumps(stats_data['series_diarias'])
    }
    
    return render(request, 'pedidos/index.html', context)

@login_required
def client_view(request):
    filtros = {
        'cliente_id': request.GET.get('cliente_id', ''),
        'nombre': request.GET.get('nombre', ''),
        'email': request.GET.get('email', ''),
        'telefono': request.GET.get('telefono', ''),
        'cedula': request.GET.get('cedula', ''),
    }

    clientes = Cliente.objects.all().order_by('cliente_id')

    if any(filtros.values()):
        queries = []
        if filtros['cliente_id']:
            queries.append(Q(cliente_id__icontains=filtros['cliente_id']))
        if filtros['nombre']:
            queries.append(Q(nombre__icontains=filtros['nombre']))
        if filtros['email']:
            queries.append(Q(email__icontains=filtros['email']))
        if filtros['telefono']:
            queries.append(Q(telefono__icontains=filtros['telefono']))
        if filtros['cedula']:
            queries.append(Q(cedula__icontains=filtros['cedula']))

        # Combinar filtros con OR (opcionalmente puede ser AND)
        query = queries.pop()
        for q in queries:
            query |= q
        clientes = clientes.filter(query)

    # Paginación
    paginator = Paginator(clientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filtros': filtros,  # Para mantener los valores en los inputs
    }
    return render(request, 'pedidos/clients_view.html', context)

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('client_view')  # Redirige a la página de inicio después de editar
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'pedidos/editar_cliente.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Productos, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('client_view')  # Redirige a la página de inicio después de editar
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'pedidos/editar_producto.html', {'form': form})


@login_required
def exportar_cliente_pdf(request, cliente_id):
    # Obtener el cliente
    cliente = Cliente.objects.get(cliente_id=cliente_id)
    
    # Crear un buffer para el PDF
    buffer = BytesIO()
    
    # Crear el PDF
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    # Configuración del PDF
    pdf.setTitle(f"Reporte Cliente {cliente.nombre}")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Información del Cliente")
    
    # Datos del cliente
    pdf.setFont("Helvetica", 12)
    y_position = 700
    campos = {
        "ID": cliente.cliente_id,
        "Nombre": cliente.nombre,
        "Email": cliente.email,
        "Teléfono": cliente.telefono,
        "Cédula": cliente.cedula,
    }
    
    for campo, valor in campos.items():
        pdf.drawString(100, y_position, f"{campo}: {valor}")
        y_position -= 30
    
    # Guardar el PDF
    pdf.showPage()
    pdf.save()
    
    # Preparar la respuesta
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cliente_{cliente.nombre}.pdf"'
    
    return response



@login_required
def categories_view(request):
    # Obtener parámetros de filtrado del request
    filtros = {
        'categoria_id': request.GET.get('categoria_id', ''),
        'categoria_nombre': request.GET.get('categoria_nombre', ''),
        'categoria_tipo': request.GET.get('categoria_tipo', ''),
    }

    # Consulta inicial
    categorias = Categoria.objects.all().order_by('categoria_id')

    # Aplicar filtros si existen
    if any(filtros.values()):
        queries = []
        if filtros['categoria_id']:
            queries.append(Q(orden_id__icontains=filtros['categoria_id']))
        if filtros['categoria_nombre']:
            queries.append(Q(nombre__icontains=filtros['categoria_nombre']))
        if filtros['categoria_tipo']:
            queries.append(Q(email__icontains=filtros['categoria_tipo']))

                # Combinar filtros con OR (opcionalmente puede ser AND)
        query = queries.pop()
        for q in queries:
            query |= q
        pedidos = categorias.filter(query)

    # Paginación
    paginator = Paginator(categorias, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filtros': filtros,  # Para mantener los valores en los inputs
    }
    return render(request, 'pedidos/categories_view.html', context)


@login_required
def categories_view(request):
    # Obtener parámetros de filtrado del request
    filtros = {
        'Categoria_ID': request.GET.get('categoria_id', ''),
        'categoria_nombre': request.GET.get('categoria_nombre', ''),
        'categoria_tipo': request.GET.get('categoria_tipo', ''),
    }

    # Consulta inicial
    categorias = Categoria.objects.all().order_by('categoria_id')

    # Aplicar filtros si existen
    if any(filtros.values()):
        queries = []
        if filtros['categoria_id']:
            queries.append(Q(orden_id__icontains=filtros['categoria_id']))
        if filtros['categoria_nombre']:
            queries.append(Q(nombre__icontains=filtros['categoria_nombre']))
        if filtros['categoria_tipo']:
            queries.append(Q(email__icontains=filtros['categoria_tipo']))

                # Combinar filtros con OR (opcionalmente puede ser AND)
        query = queries.pop()
        for q in queries:
            query |= q
        categorias = categorias.filter(query)

    # Paginación
    paginator = Paginator(categorias, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filtros': filtros,  # Para mantener los valores en los inputs
    }
    return render(request, 'pedidos/categories_view.html', context)



@login_required
def products_view(request):
    # Obtener parámetros de filtrado
    filtros = {
        'producto_id': request.GET.get('producto_id', ''),
        'producto_nombre': request.GET.get('producto_nombre', ''),
        'precio': request.GET.get('precio', ''),
        'activo': request.GET.get('activo', ''),
        'categoria_id': request.GET.get('categoria_id', ''),
        'unidad': request.GET.get('unidad', '')
    }
    
    
    productos = Productos.objects.all().select_related('categoria').only(
        'producto_id', 
        'producto_nombre', 
        'precio', 
        'activo', 
        'unidad',
        'categoria__categoria_nombre'  # Solo el nombre de la categoría
    ).order_by('producto_id')
    
    # Aplicar filtros de manera más eficiente
    if filtros['producto_id']:
        productos = productos.filter(producto_id__icontains=filtros['producto_id'])
    if filtros['producto_nombre']:
        productos = productos.filter(producto_nombre__icontains=filtros['producto_nombre'])
    if filtros['precio']:
        try:
            # Para búsqueda exacta de precio
            productos = productos.filter(precio=filtros['precio'])
        except ValueError:
            # Si no es número, buscar como texto
            productos = productos.filter(precio__icontains=filtros['precio'])
    if filtros['activo']:
        activo_value = filtros['activo'].lower() in ['true', '1', 'yes', 'activo']
        productos = productos.filter(activo=activo_value)
    if filtros['categoria_id']:
        productos = productos.filter(categoria__categoria_id__icontains=filtros['categoria_id'])
    if filtros['unidad']:
        productos = productos.filter(unidad__icontains=filtros['unidad'])
    
    # OPTIMIZACIÓN: Paginación más eficiente
    paginator = Paginator(productos, 20)  # Mostrar 20 items por página
    
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'page_obj': page_obj,
        'filtros': filtros,
    }
    
    return render(request, 'pedidos/products_view.html', context)


@login_required
def crear_orden(request):
    productos = Productos.objects.filter(activo=True)
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        
        if form.is_valid():
            try:
                cliente, created = Cliente.objects.get_or_create(user=request.user)
                
                envio = Envio.objects.create(
                    estado='pendiente'
                )
                
                orden = Pedido.objects.create(
                    fecha_orden=datetime.now(),
                    envio=envio,
                    cliente=cliente,
                    fecha_entrega=form.cleaned_data['fecha_entrega'],
                    horario_entrega=form.cleaned_data['horario_entrega']
                )
                
                productos_data = json.loads(request.POST.get('productos_json', '[]'))
                
                for item in productos_data:
                    producto = Productos.objects.get(producto_id=item['producto_id'])
                    DetallePedido.objects.create(
                        pedido=orden,  
                        producto=producto,
                        cantidad=item['cantidad'],
                        precio_unitario=producto.precio
                    )
                
                return redirect('detalle_orden', orden_id=orden.orden_id)
            
            except Exception as e:
                print(f"Error al crear la orden: {str(e)}")
                form.add_error(None, f'Error al crear la orden: {str(e)}')
        else:
            print("Formulario no válido")
            print(form.errors)
    
    else:
        form = PedidoForm()
    
    return render(request, 'pedidos/crear_orden.html', {
        'form': form,
        'productos': productos
    })

@login_required
def detalle_orden(request, orden_id):
    orden = Pedido.objects.get(orden_id=orden_id)
    return render(request, 'pedidos/detalle_orden.html', {
        'orden': orden
    })

def obtener_productos(request):
    productos = Productos.objects.filter(activo=True).values(
        'producto_id', 
        'producto_nombre', 
        'precio',
        'unidad',
        'activo'
    )
    return JsonResponse(list(productos), safe=False)


@login_required
def orders_view(request):
    # Obtener parámetros de filtrado
    filtros = {
        'orden_id': request.GET.get('orden_id', ''),
        'cliente': request.GET.get('cliente', ''),
        'fecha_entrega': request.GET.get('fecha_entrega', ''),
        'horario_entrega': request.GET.get('horario_entrega', ''),
    }
    
    orders = Pedido.objects.all().select_related('cliente').prefetch_related(
        'detalles__producto'
    ).only(
        'orden_id',
        'cliente__nombre',
        'fecha_entrega',  
        'horario_entrega',
        'fecha_orden'
    ).order_by('orden_id')
    
    if filtros['orden_id']:
        orders = orders.filter(orden_id__icontains=filtros['orden_id'])
    if filtros['cliente']:
        orders = orders.filter(cliente__nombre__icontains=filtros['cliente'])
    if filtros['fecha_entrega']:
        orders = orders.filter(fecha_entrega=filtros['fecha_entrega'])
    if filtros['horario_entrega']:
        orders = orders.filter(horario_entrega=filtros['horario_entrega'])

    
    orders_with_totals = []
    for order in orders:
        total = sum(
            detalle.cantidad * detalle.precio_unitario 
            for detalle in order.detalles.all()
        )
        orders_with_totals.append({
            'orden': order,
            'total_calculado': total
        })

    paginator = Paginator(orders_with_totals, 20)  
    
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    context = {
        'page_obj': page_obj,
        'filtros': filtros,
    }
    
    return render(request, 'pedidos/orders_view.html', context)

