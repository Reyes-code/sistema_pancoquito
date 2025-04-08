# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categoria(models.Model):
    categoria_id = models.AutoField(db_column='Categoria_ID', primary_key=True)  # Field name made lowercase.
    categoria_nombre = models.CharField(db_column='Categoria_nombre', max_length=100)  # Field name made lowercase.
    categoria_tipo = models.CharField(db_column='Categoria_Tipo', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categoria'


class Cliente(models.Model):
    cliente_id = models.AutoField(db_column='Cliente_ID', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=100)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=100)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cliente'


class Envio(models.Model):
    envio_id = models.AutoField(db_column='Envio_ID', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=50)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'envio'


class Orden(models.Model):
    orden_id = models.AutoField(db_column='Orden_ID', primary_key=True)  # Field name made lowercase.
    fecha_orden = models.DateTimeField(db_column='Fecha_Orden')  # Field name made lowercase.
    envio = models.ForeignKey(Envio, models.DO_NOTHING, db_column='Envio_ID', blank=True, null=True)  # Field name made lowercase.
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='Cliente_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orden'


class Productos(models.Model):
    producto_id = models.AutoField(db_column='Producto_ID', primary_key=True)  # Field name made lowercase.
    producto_nombre = models.CharField(db_column='Producto_nombre', max_length=100)  # Field name made lowercase.
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='Categoria_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productos'
