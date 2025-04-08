from django.shortcuts import render
from .models import Cliente
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('nombre')  # Ordenados por nombre
    return render(request, 'pedidos/lista_clientes.html', {'clientes': clientes})
def home(request):
    return render(request, 'pedidos/home.html')



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

def logout_view(request):
    logout(request)
    return redirect('login') 
