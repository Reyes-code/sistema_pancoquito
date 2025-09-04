from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Usa tu vista personalizada
    path('home/clientes/', views.client_view, name='client_view'),
    path('home/categorias/', views.categories_view, name='categories_view'),
    path('home/productos/', views.products_view, name='products_view'),
    path('home/', views.home, name='home'),
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/pdf/', views.exportar_cliente_pdf, name='exportar_cliente_pdf'),
    path('ordenes/nueva/', views.CrearOrdenView.as_view(), name='crear_orden'),
]