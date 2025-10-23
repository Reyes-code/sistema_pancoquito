from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views,APIView
from .decorators import group_required



urlpatterns = [
    path('login/', views.login_view, name='login'),
    path("clientes/", group_required('Admin', 'Operador')(views.client_view), name='client_view'),
    path('logout/', views.logout_view, name='logout'), 
    
    
    
    path('clientes/', views.client_view, name='client_view'),
    path('categorias/', views.categories_view, name='categories_view'),
    path('productos/', views.products_view, name='products_view'),  
    path('ordenes/', views.orders_view, name='orders_view'),
    path('home/', views.home, name='home'),
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('editar-cliente/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('clientes/<int:cliente_id>/pdf/', views.exportar_cliente_pdf, name='exportar_cliente_pdf'),
    path('crear-orden/', views.crear_orden, name='crear_orden'),
    path('orden/<int:id>/', views.detalle_orden, name='detalle_orden'),
    path('api/productos/', views.obtener_productos, name='obtener_productos'),
    path('api/login-token/', APIView.LoginView.as_view(), name='api_login_token'),
    path('api/stats/', APIView.StatsView.as_view(), name='main_view_stats'),
]
 