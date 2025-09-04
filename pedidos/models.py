from django.db import models


class Cliente(models.Model):
    cliente_id = models.AutoField(db_column='Cliente_ID', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    email = models.CharField(db_column='Email', unique=True, max_length=100)
    telefono = models.CharField(db_column='Telefono', max_length=255, blank=True, null=True)
    cedula = models.IntegerField(db_column='Cedula', blank=True, null=True)

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


class Orden(models.Model):
    orden_id = models.AutoField(db_column='Orden_ID', primary_key=True)
    fecha_orden = models.DateTimeField(db_column='Fecha_Orden')
    envio = models.ForeignKey(Envio, models.DO_NOTHING, db_column='Envio_ID', blank=True, null=True)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='Cliente_ID', blank=True, null=True)

    # Relación muchos-a-muchos con tabla intermedia
    productos = models.ManyToManyField(Productos, through='OrdenDetalle', related_name='ordenes')

    class Meta:
        db_table = 'orden'

    @property
    def total(self):
        from django.db.models import F, Sum, DecimalField
        return self.detalles.aggregate(
            total=Sum(F('cantidad') * F('precio_unitario'), output_field=DecimalField())
        )['total'] or 0


class OrdenDetalle(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, db_column='Orden_ID', related_name='detalles')
    producto = models.ForeignKey(Productos, on_delete=models.PROTECT, db_column='Producto_ID', related_name='detalles')
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'orden_detalle'
        unique_together = (('orden', 'producto'),)

class Inventario(models.Model):
    producto = models.OneToOneField(Productos, on_delete=models.CASCADE, db_column='Producto_ID', primary_key=True, related_name='inventario')
    cantidad_disponible = models.PositiveIntegerField(db_column='Cantidad_Disponible', default=0)
    cantidad_minima = models.PositiveIntegerField(db_column='Cantidad_Minima', default=10)
    ultima_actualizacion = models.DateTimeField(db_column='Ultima_Actualizacion', auto_now=True)

    class Meta:
        db_table = 'inventario'

    def __str__(self):
        return f"Inventario de {self.producto.producto_nombre}: {self.cantidad_disponible} unidades"
    
