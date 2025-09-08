from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Usa tu vista personalizada
    path('clientes/', views.client_view, name='client_view'),
    path('categorias/', views.categories_view, name='categories_view'),
    path('productos/', views.products_view, name='products_view'),
    path('home/', views.home, name='home'),
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/pdf/', views.exportar_cliente_pdf, name='exportar_cliente_pdf'),


    path('crear-orden/', views.crear_orden, name='crear_orden'),
    path('orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('api/validar-cliente/', views.validar_cliente, name='validar_cliente'),
    path('api/productos/', views.obtener_productos, name='obtener_productos'),
]
 