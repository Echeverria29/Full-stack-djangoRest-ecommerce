from django.db import models


class Cliente(models.Model):
    rut_cliente = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=80)
    direccion = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    numero_tarjeta = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cliente'


class DetalleCompra(models.Model):
    id_venta = models.OneToOneField('Venta', models.DO_NOTHING, db_column='id_venta', primary_key=True)  # The composite primary key (id_venta, id_libro) found, that is not supported. The first column is selected.
    id_libro = models.ForeignKey('Libro', models.DO_NOTHING, db_column='id_libro')

    class Meta:
        managed = False
        db_table = 'detalle_compra'
        unique_together = (('id_venta', 'id_libro'),)


class Empleado(models.Model):
    rut_empleado = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=80)
    direccion = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'empleado'


class Libro(models.Model):
    id_libro = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    editorial = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    proveedor = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'libro'


class Pago(models.Model):
    id_pago = models.IntegerField(primary_key=True)
    total = models.IntegerField()
    id_venta = models.OneToOneField('Venta', models.DO_NOTHING, db_column='id_venta')
    tipo_pago = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pago'


class Servicio(models.Model):
    id_servicio = models.IntegerField(primary_key=True)
    fecha_servicio = models.DateField()
    direccion_servicio = models.CharField(max_length=80)
    tipo_servicio = models.CharField(max_length=50)
    detalle_servicio = models.CharField(max_length=200)
    rut_tecnico = models.ForeignKey('Tecnico', models.DO_NOTHING, db_column='rut_tecnico')
    rut_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='rut_cliente')

    class Meta:
        managed = False
        db_table = 'servicio'


class Tecnico(models.Model):
    rut_tecnico = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=80)
    direccion = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tecnico'


class Venta(models.Model):
    id_venta = models.IntegerField(primary_key=True)
    fecha_venta = models.DateField()
    tipo_venta = models.CharField(max_length=50)
    rut_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='rut_cliente')
    rut_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='rut_empleado')

    class Meta:
        managed = False
        db_table = 'venta'
