from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Usa tu vista personalizada
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('pedidos/', views.lista_categorias, name='lista_pedidos'),
    path('home/', views.home, name='home'),
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/pdf/', views.exportar_cliente_pdf, name='exportar_cliente_pdf'),
    path('ordenes/nueva/', views.CrearOrdenView.as_view(), name='crear_orden'),
]