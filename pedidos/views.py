from django.shortcuts import render
from .models import Cliente
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
from .forms import ClienteForm

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
    return render(request, 'pedidos/home.html')

@never_cache
@login_required
def lista_clientes(request):
    # Filtrado
    query = request.GET.get('q', '')
    clientes = Cliente.objects.all().order_by('cliente_id')
    
    if query:
        clientes = clientes.filter(
            Q(cliente_id__icontains=query) |
            Q(nombre__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query)|
            Q(cedula__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(clientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    response = render(request, 'pedidos/lista_clientes.html', {
        'query': query,
        'page_obj' : page_obj
    })
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response


@never_cache
@login_required
def lista_clientes(request):
    # Filtrados
    query = request.GET.get('q', '')
    clientes = Cliente.objects.all().order_by('cliente_id')
    
    if query:
        clientes = clientes.filter(
            Q(cliente_id__icontains=query) |
            Q(nombre__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query)|
            Q(cedula__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(clientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    response = render(request, 'pedidos/lista_clientes.html', {
        'query': query,
        'page_obj' : page_obj
    })
    response['Cache-Control'] = 'no-store, must-revalidate'
    print(response)
    return response

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')  # Redirige a la página de inicio después de editar
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'pedidos/editar_cliente.html', {'form': form})



