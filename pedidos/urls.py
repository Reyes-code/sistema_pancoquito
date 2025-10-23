from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views,APIView
from .decorators import group_required



urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=True)),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  
    path('home/', views.home, name='home'),
    path("clientes/", group_required('Admin','Empleado')(views.client_view), name='client_view'),
    path('categorias/', group_required('Admin','Empleado')(views.categories_view), name='categories_view'),
    path('productos/', views.products_view, name='products_view'),  
    path('ordenes/', views.orders_view, name='orders_view'),
    path('editar-cliente/<int:cliente_id>/', group_required('Admin')(views.editar_cliente), name='editar_cliente'),
    path('editar-producto/<int:producto_id>/', group_required('Admin')(views.editar_producto), name='editar_producto'),
    path('clientes/<int:cliente_id>/pdf/', group_required('Admin','Empleado')(views.exportar_cliente_pdf), name='exportar_cliente_pdf'),
    path('crear-orden/', group_required('Admin','Cliente')(views.crear_orden), name='crear_orden'),
    path('orden/<int:id>/', views.detalle_orden, name='detalle_orden'),
    path('api/productos/', views.obtener_productos, name='obtener_productos'),
    path('api/login-token/', APIView.LoginView.as_view(), name='api_login_token'),
    path('api/stats/', APIView.StatsView.as_view(), name='main_view_stats'),
]
 