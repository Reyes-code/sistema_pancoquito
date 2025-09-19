from django.db import models
from django.contrib.auth.models import User 
from datetime import datetime

class Cliente(models.Model):
    cliente_id = models.AutoField(db_column='Cliente_ID', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    email = models.CharField(db_column='Email', unique=True, max_length=100)
    telefono = models.CharField(db_column='Telefono', max_length=255, blank=True, null=True)
    cedula = models.IntegerField(db_column='Cedula', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cliente', null=True)

    class Meta:
        db_table = 'cliente'



class Envio(models.Model):
    envio_id = models.AutoField(db_column='Envio_ID', primary_key=True)
    tipo = models.CharField(db_column='Tipo', max_length=50)
    estado = models.CharField(db_column='Estado', max_length=50)

    class Meta:
        db_table = 'envio'


class Categoria(models.Model):
    categoria_id = models.PositiveIntegerField(primary_key=True)
    categoria_nombre = models.CharField(db_column='Categoria_nombre', max_length=100)
    categoria_tipo = models.CharField(db_column='Categoria_Tipo', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'categoria'


class Productos(models.Model):
    producto_id = models.PositiveIntegerField(db_column='Producto_ID', primary_key=True,null=False)
    producto_nombre = models.CharField(db_column='Producto_nombre', max_length=100)
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='Categoria_ID', blank=True, null=True)
    unidad = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'productos'


class Pedido(models.Model):
    HORARIO_CHOICES = [
        ('mañana', 'Mañana'),
        ('tarde', 'Tarde'),
    ]
    
    orden_id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_entrega = models.DateField()
    horario_entrega = models.CharField(max_length=10, choices=HORARIO_CHOICES)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_orden = models.DateTimeField(auto_now_add=True) 
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE)  
    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def subtotal(self):
        return self.cantidad * self.precio_unitario