
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=15)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    
    class Meta:
        abstract = True

    

    def actualizar_user_fields(self):
        
        self.user.first_name = self.nombre
        self.user.last_name = self.apellido
        self.user.email = self.correo
        self.user.save()

class Empleado(Perfil):
    cargo = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        created = not bool(self.pk)
        super().save(*args, **kwargs)
        if created:
            self.actualizar_user_fields()

class Cliente(Perfil):
  

    def save(self, *args, **kwargs):
        created = not bool(self.pk)
        super().save(*args, **kwargs)
        if created:
            self.actualizar_user_fields()

class Tecnico(Perfil):
    

    def save(self, *args, **kwargs):
        created = not bool(self.pk)
        super().save(*args, **kwargs)
        if created:
            self.actualizar_user_fields()

class Cotizaciones(models.Model):
   
    fecha = models.DateTimeField()
    correo = models.CharField(max_length=80)
    detalle = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
      return self.cliente


    class Meta:
       
        db_table = 'cotizaciones'



class Materiales(models.Model):
   
    nombre = models.CharField( max_length=30)
    stock = models.IntegerField()
    tecnico = models.ForeignKey(Tecnico, models.CASCADE)

    class Meta:
        
        db_table = 'materiales'


class Tipo(models.Model):

    tipo = models.CharField(max_length=40)

    def __str__(self):
        return self.tipo
    class Meta:
        
        db_table = 'tipo'

class Servicio(models.Model):
  
    fecha_servicio = models.DateTimeField()
    direccion_servicio = models.CharField(max_length=80)
    detalle_servicio = models.CharField(max_length=200)
    tipo = models.ForeignKey(Tipo,on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)
    
    
    
    class Meta:
        db_table = 'servicio'


class Venta(models.Model):
   
    fecha_venta = models.DateField()
    total = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    class Meta:
        
        db_table = 'venta'

class Pago(models.Model):
   
    total = models.IntegerField()
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    def __str__(self):
        return self.total
    class Meta:
       
        db_table = 'pago'


class Libro(models.Model):
   
    nombre = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    editorial = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    proveedor = models.CharField(max_length=50)

    def stockfinal(self):
      return self.stock - self.carrito.cantidad

    def __str__(self):
      return self.nombre
  

    class Meta:
       
        db_table = 'libro'

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
    def subtotal(self):
        return self.libro.precio * self.cantidad

    def __str__(self):
        return self.libro.nombre
    
    class Meta:
        
        db_table = 'carrito'

class DetalleVenta(models.Model):
    
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)  
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)

    class Meta:
        
        db_table = 'detalle_venta'
      



