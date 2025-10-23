from django.contrib import admin
from django.urls import path, include
from pedidos.views import custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pedidos.urls')),
]

handler404 = custom_404