from django.contrib import admin
from .models import Cliente, Orden, Envio, Categoria, Productos, OrdenDetalle

admin.site.register(Cliente)
admin.site.register(Orden)
admin.site.register(Envio)
admin.site.register(Categoria)
admin.site.register(Productos)
admin.site.register(OrdenDetalle)