
from django.db import models


class Tecnico(models.Model):
    rut_tecnico = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=80)
    direccion = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        
        db_table = 'tecnico'

class Cliente(models.Model):
    rut_cliente = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=80)
    direccion = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    numero_tarjeta = models.IntegerField()


    def __str__(self):
      return self.nombre


    class Meta:
       
        db_table = 'cliente'

class Empleado(models.Model):
    rut_empleado = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=80)
    direccion = models.CharField(max_length=80, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
  
    class Meta:
        
        db_table = 'empleado'

class Servicio(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_servicio = models.DateField()
    direccion_servicio = models.CharField(max_length=80)
    tipo_servicio = models.CharField(max_length=50)
    detalle_servicio = models.CharField(max_length=200)
    rut_tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)
    rut_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        
        db_table = 'servicio'

class Venta(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha_venta = models.DateField()
    total = models.IntegerField()
    rut_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    rut_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    class Meta:
        
        db_table = 'venta'

class Pago(models.Model):
    id = models.IntegerField(primary_key=True)
    total = models.IntegerField()
    id_venta = models.OneToOneField(Venta, on_delete=models.CASCADE, db_column='id_venta')
    tipo_pago = models.CharField(max_length=50)

    class Meta:
       
        db_table = 'pago'


class Libro(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    editorial = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    proveedor = models.CharField(max_length=50)

    def __str__(self):
      return self.nombre
  

    class Meta:
       
        db_table = 'libro'

class Carrito(models.Model):
    id = models.IntegerField(primary_key=True)
    libro = models.ForeignKey(Libro, models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
    def subtotal(self):
        return self.libro.precio * self.cantidad

    def __str__(self):
        return self.libro.nombre
    
    class Meta:
        
        db_table = 'carrito'

class DetalleVenta(models.Model):
    id = models.IntegerField(primary_key=True)
    venta_venta_id = models.ForeignKey(Venta, on_delete=models.CASCADE)  
    venta_libro_id = models.ForeignKey(Libro, on_delete=models.CASCADE)

    class Meta:
        
        db_table = 'detalle_venta'
      







