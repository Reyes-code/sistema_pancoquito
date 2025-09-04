from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Orden, Productos, Envio, Categoria
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache   
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ClienteForm, OrdenForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
from django.views import View

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

@never_cache  # Evita que el navegador cachee la respuesta
@login_required
def home(request):
    return render(request, 'pedidos/index.html')

@login_required
def client_view(request):
    # Obtener parámetros de filtrado del request
    filtros = {
        'cliente_id': request.GET.get('cliente_id', ''),
        'nombre': request.GET.get('nombre', ''),
        'email': request.GET.get('email', ''),
        'telefono': request.GET.get('telefono', ''),
        'cedula': request.GET.get('cedula', ''),
    }

    # Consulta inicial
    clientes = Cliente.objects.all().order_by('cliente_id')

    # Aplicar filtros si existen
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



class CrearOrdenView(View):
    def get(self, request):
        form = OrdenForm()
        return render(request, 'pedidos/crear_orden.html', {'form': form})

    def post(self, request):
        form = OrdenForm(request.POST)
        if form.is_valid():
            # 1. Crear nuevo envío
            envio = Envio.objects.create(
                tipo=form.cleaned_data['tipo_envio'],
                estado=form.cleaned_data['estado_envio']
            )
            
            # 2. Obtener el próximo ID de orden
            ultima_orden = Orden.objects.all().order_by('-orden_id').first()
            nuevo_orden_id = ultima_orden.orden_id + 1 if ultima_orden else 1
            
            # 3. Crear registros de orden para cada producto
            for producto in form.cleaned_data['productos']:
                Orden.objects.create(
                    orden_id=nuevo_orden_id,
                    fecha_orden=datetime.now(),
                    envio=envio,
                    cliente_id=form.cleaned_data['cliente_id'],
                    producto=producto,
                    precio=producto.precio,
                    cantidad=form.cleaned_data['cantidad']
                )
            
            return redirect('lista_ordenes')

        
        return render(request, 'pedidos/crear_orden.html', {'form': form})



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
    # Obtener parámetros de filtro (corregir nombres)
    filtros = {
        'producto_id': request.GET.get('Producto_ID', ''), 
        'producto_nombre': request.GET.get('Producto_nombre', ''),
        'precio': request.GET.get('precio', ''),
        'activo': request.GET.get('activo', ''),
        'categoria_id': request.GET.get('Categoria_ID', ''),
        'unidad': request.GET.get('unidad', '')
    }
    
    # Query inicial con select_related
    productos = Productos.objects.all().select_related('categoria').order_by('producto_id')
    
    # Aplicar filtros
    if any(filtros.values()):
        query = Q()
        
        if filtros['producto_id']:
            query &= Q(producto_id__icontains=filtros['producto_id'])
        if filtros['producto_nombre']:
            query &= Q(producto_nombre__icontains=filtros['producto_nombre'])
        if filtros['precio']:
            query &= Q(precio__icontains=filtros['precio'])
        if filtros['activo']:
            # Convertir string a booleano
            activo_value = filtros['activo'].lower() in ['true', '1', 'yes']
            query &= Q(activo=activo_value)
        if filtros['categoria_id']:
            query &= Q(categoria__categoria_id__icontains=filtros['categoria_id'])
        if filtros['unidad']:
            query &= Q(unidad__icontains=filtros['unidad'])
        
        productos = productos.filter(query)
    
    # Paginación
    paginator = Paginator(productos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filtros': filtros,
    }
    return render(request, 'pedidos/products_view.html', context)