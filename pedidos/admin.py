from django.contrib import admin
from .models import Cliente, Pedido, Envio, Categoria, Productos, DetallePedido

admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Envio)
admin.site.register(Categoria)
admin.site.register(Productos)
admin.site.register(DetallePedido)