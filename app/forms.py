from genericpath import exists
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from datetime import datetime, time

#formulario para registrarse
class RegistroUsuarioForm(UserCreationForm):
    
    
    class Meta:
        model= User 
        fields = ['username','email','password1','password2']


#formulario para agregar productos al carrito
class AgregarAlCarritoForm(forms.Form):
    libro_id = forms.IntegerField(widget=forms.HiddenInput())
    cantidad = forms.IntegerField()

    class Meta:
        
        model = Carrito
      
        fields = ['libro_id','cantidad']

#formulario para que el cliente agrege sus datos , sin el id esta programado en  views para que no se coloque
class ClienteForm(ModelForm):
   
    rut_cliente = forms.CharField(min_length=3 ,max_length=15)
    nombre = forms.CharField(min_length=3 ,max_length=50)
    apellido = forms.CharField(min_length=3 ,max_length=50)
    correo = forms.CharField(min_length=3 ,max_length=80)
    direccion = forms.CharField(min_length=3 ,max_length=80)
    telefono = forms.CharField(min_length=3 ,max_length=20)
    numero_tarjeta = forms.IntegerField()

    class Meta:
        model = Cliente
        fields = ['rut_cliente','nombre','apellido','correo','direccion','telefono', 'numero_tarjeta']

class EmpleadoForm(ModelForm):
   
    rut_empleado = forms.CharField(min_length=3 ,max_length=15)
    nombre = forms.CharField(min_length=3 ,max_length=50)
    apellido = forms.CharField(min_length=3 ,max_length=50)
    correo = forms.CharField(min_length=3 ,max_length=80)
    direccion = forms.CharField(min_length=3 ,max_length=80)
    telefono = forms.CharField(min_length=3 ,max_length=20)
    cargo = forms.CharField(min_length=3 ,max_length=20)
    departamento = forms.CharField(min_length=3 ,max_length=20)
    

    class Meta:
        model = Empleado
        fields = ['rut_empleado','nombre','apellido','correo','direccion','telefono', 'cargo','departamento']




class TecnicoForm(ModelForm):
   
    rut_tecnico = forms.CharField(min_length=3 ,max_length=15)
    nombre = forms.CharField(min_length=3 ,max_length=50)
    apellido = forms.CharField(min_length=3 ,max_length=50)
    correo = forms.CharField(min_length=3 ,max_length=80)
    direccion = forms.CharField(min_length=3 ,max_length=80,required=False)
    telefono = forms.CharField(min_length=3 ,max_length=20,required=False)
    

    class Meta:
        model = Tecnico
        fields = ['rut_tecnico','nombre','apellido','correo','direccion','telefono']


class MaterialesForm(ModelForm):
   
   
    nombre = forms.CharField(min_length=3 ,max_length=50)
    stock = forms.IntegerField()
    tecnico = forms.ModelChoiceField(queryset=Tecnico.objects.all())

    

    class Meta:
        model = Tecnico
        fields = ['nombre','stock','tecnico']



#formulario para solicitar el servicio por parte del cliente
class ServicioForm(ModelForm):
    fecha_servicio = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'step': '60'}),input_formats=['%Y-%m-%dT%H:%M'])
    direccion_servicio = forms.CharField(max_length=80)
    detalle_servicio = forms.CharField(max_length=200)
    tecnico = forms.ModelChoiceField(queryset=Tecnico.objects.all())
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())
    tipo = forms.ModelChoiceField(queryset=Tipo.objects.all())

    class Meta:
        model = Servicio
        fields = ['fecha_servicio','direccion_servicio', 'detalle_servicio', 'tecnico','cliente','tipo']


#formulario para solicitar cotizaciones por parte del cliente
class CotizacionesForm(ModelForm):
    fecha = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'step': '60'}),input_formats=['%Y-%m-%dT%H:%M'])
    correo = forms.CharField(max_length=80)
    detalle = forms.CharField(max_length=200)
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())

    class Meta:
        model = Cotizaciones
        fields = ['fecha','correo', 'detalle','cliente']
