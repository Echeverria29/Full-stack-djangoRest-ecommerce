from genericpath import exists
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from datetime import datetime, time
from django.contrib.auth.forms import AuthenticationForm
#formulario para registrarse


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


#formulario para agregar productos al carrito
class AgregarAlCarritoForm(forms.Form):
    libro_id = forms.IntegerField(widget=forms.HiddenInput())
    cantidad = forms.IntegerField()

    class Meta:
        
        model = Carrito
      
        fields = ['libro_id','cantidad']

class Crearclienteform(ModelForm):
    username = forms.CharField(min_length=3, max_length=15, label="Nombre de usuario")
    password = forms.CharField(min_length=3, max_length=15, label="Contraseña")
    rut = forms.CharField(min_length=3, max_length=15, label="RUT")
    nombre = forms.CharField(min_length=3, max_length=50, label="Nombre")
    apellido = forms.CharField(min_length=3, max_length=50, label="Apellido")
    correo = forms.CharField(min_length=3, max_length=80, label="Correo electrónico")
    direccion = forms.CharField(min_length=3, max_length=80, label="Dirección")
    telefono = forms.CharField(min_length=3, max_length=20, label="Teléfono")

    class Meta:
        model = Cliente
        fields = ['username', 'password', 'rut', 'nombre', 'apellido', 'correo', 'direccion', 'telefono']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        cliente = super().save(commit=False)
        cliente.user = user
        if commit:
            cliente.save()
        return cliente

class ModificarClienteForm(forms.ModelForm):
    rut = forms.CharField(min_length=3, max_length=15, label="RUT")
    nombre = forms.CharField(min_length=3, max_length=50, label="Nombre")
    apellido = forms.CharField(min_length=3, max_length=50, label="Apellido")
    correo = forms.CharField(min_length=3, max_length=80, label="Correo electrónico")
    direccion = forms.CharField(min_length=3, max_length=80, label="Dirección")
    telefono = forms.CharField(min_length=3, max_length=20, label="Teléfono")

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.user.first_name = self.cleaned_data['nombre']
        cliente.user.last_name = self.cleaned_data['apellido']
        cliente.user.email = self.cleaned_data['correo']
        if commit:
            cliente.save()
            cliente.user.save()
        return cliente

    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'correo', 'direccion', 'telefono']

class Crearempleadoform(ModelForm):
    username = forms.CharField(min_length=3, max_length=15, label="Nombre de usuario")
    password = forms.CharField(min_length=3, max_length=15, label="Contraseña")
    rut = forms.CharField(min_length=3, max_length=15, label="RUT")
    nombre = forms.CharField(min_length=3, max_length=50, label="Nombre")
    apellido = forms.CharField(min_length=3, max_length=50, label="Apellido")
    correo = forms.CharField(min_length=3, max_length=80, label="Correo electrónico")
    direccion = forms.CharField(min_length=3, max_length=80, label="Dirección")
    telefono = forms.CharField(min_length=3, max_length=20, label="Teléfono")
    cargo = forms.CharField(min_length=3, max_length=20, label="cargo")
    departamento = forms.CharField(min_length=3, max_length=20, label="departamento")
   
    class Meta:
        model = Empleado
        fields = ['username', 'password', 'rut', 'nombre', 'apellido', 'correo', 'direccion', 'telefono','cargo','departamento']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        empleado = super().save(commit=False)
        empleado.user = user
        if commit:
            empleado.save()
        return empleado

class ModificarEmpleadoForm(forms.ModelForm):
    rut = forms.CharField(min_length=3, max_length=15, label="RUT")
    nombre = forms.CharField(min_length=3, max_length=50, label="Nombre")
    apellido = forms.CharField(min_length=3, max_length=50, label="Apellido")
    correo = forms.CharField(min_length=3, max_length=80, label="Correo electrónico")
    direccion = forms.CharField(min_length=3, max_length=80, label="Dirección")
    telefono = forms.CharField(min_length=3, max_length=20, label="Teléfono")
    def save(self, commit=True):
        empleado = super().save(commit=False)
        empleado.user.first_name = self.cleaned_data['nombre']
        empleado.user.last_name = self.cleaned_data['apellido']
        empleado.user.email = self.cleaned_data['correo']
        if commit:
            empleado.save()
            empleado.user.save()
        return empleado 
    class Meta:
        model = Empleado
        fields = ['rut', 'nombre', 'apellido', 'correo', 'direccion', 'telefono']


class Creartecnicoform(ModelForm):
    username = forms.CharField(min_length=3, max_length=15, label="Nombre de usuario")
    password = forms.CharField(min_length=3, max_length=15, label="Contraseña")
    rut = forms.CharField(min_length=3, max_length=15, label="RUT")
    nombre = forms.CharField(min_length=3, max_length=50, label="Nombre")
    apellido = forms.CharField(min_length=3, max_length=50, label="Apellido")
    correo = forms.CharField(min_length=3, max_length=80, label="Correo electrónico")
    direccion = forms.CharField(min_length=3, max_length=80, label="Dirección")
    telefono = forms.CharField(min_length=3, max_length=20, label="Teléfono")

   
    class Meta:
        model = Tecnico
        fields = ['username', 'password', 'rut', 'nombre', 'apellido', 'correo', 'direccion', 'telefono']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        tecnico = super().save(commit=False)
        tecnico.user = user
        if commit:
            tecnico.save()
        return tecnico

class ModificarTecnicoForm(forms.ModelForm):
    rut = forms.CharField(min_length=3, max_length=15, label="RUT")
    nombre = forms.CharField(min_length=3, max_length=50, label="Nombre")
    apellido = forms.CharField(min_length=3, max_length=50, label="Apellido")
    correo = forms.CharField(min_length=3, max_length=80, label="Correo electrónico")
    direccion = forms.CharField(min_length=3, max_length=80, label="Dirección")
    telefono = forms.CharField(min_length=3, max_length=20, label="Teléfono")
    def save(self, commit=True):
        tecnico = super().save(commit=False)
        tecnico.user.first_name = self.cleaned_data['nombre']
        tecnico.user.last_name = self.cleaned_data['apellido']
        tecnico.user.email = self.cleaned_data['correo']
        if commit:
            tecnico.save()
            tecnico.user.save()
        return tecnico 
    class Meta:
        model = Tecnico
        fields = ['rut', 'nombre', 'apellido', 'correo', 'direccion', 'telefono']



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

##############################################################
#############################################################
##########################admin##############################


    
class ModificarClienteadminForm(forms.ModelForm):
    rut = forms.CharField(min_length=3, max_length=15, label="RUT")
    nombre = forms.CharField(min_length=3, max_length=50, label="Nombre")
    apellido = forms.CharField(min_length=3, max_length=50, label="Apellido")
    correo = forms.CharField(min_length=3, max_length=80, label="Correo electrónico")
    direccion = forms.CharField(min_length=3, max_length=80, label="Dirección")
    telefono = forms.CharField(min_length=3, max_length=20, label="Teléfono")

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.user.first_name = self.cleaned_data['nombre']
        cliente.user.last_name = self.cleaned_data['apellido']
        cliente.user.email = self.cleaned_data['correo']
        if commit:
            cliente.save()
            cliente.user.save()
        return cliente

    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'apellido', 'correo', 'direccion', 'telefono']



class ModificarEmpleadoadminForm(forms.ModelForm):
    rut = forms.CharField(min_length=3, max_length=15, label="RUT")
    nombre = forms.CharField(min_length=3, max_length=50, label="Nombre")
    apellido = forms.CharField(min_length=3, max_length=50, label="Apellido")
    correo = forms.CharField(min_length=3, max_length=80, label="Correo electrónico")
    direccion = forms.CharField(min_length=3, max_length=80, label="Dirección")
    telefono = forms.CharField(min_length=3, max_length=20, label="Teléfono")
    cargo = forms.CharField(min_length=3, max_length=20, label="Cargo")
    departamento = forms.CharField(min_length=3, max_length=20, label="Departamento")
    def save(self, commit=True):
        empleado = super().save(commit=False)
        empleado.user.first_name = self.cleaned_data['nombre']
        empleado.user.last_name = self.cleaned_data['apellido']
        empleado.user.email = self.cleaned_data['correo']
        if commit:
            empleado.save()
            empleado.user.save()
        return empleado 
    class Meta:
        model = Empleado
        fields = ['rut', 'nombre', 'apellido', 'correo', 'direccion', 'telefono']



class ModificarTecnicoadminForm(forms.ModelForm):
    rut = forms.CharField(min_length=3, max_length=15, label="RUT")
    nombre = forms.CharField(min_length=3, max_length=50, label="Nombre")
    apellido = forms.CharField(min_length=3, max_length=50, label="Apellido")
    correo = forms.CharField(min_length=3, max_length=80, label="Correo electrónico")
    direccion = forms.CharField(min_length=3, max_length=80, label="Dirección")
    telefono = forms.CharField(min_length=3, max_length=20, label="Teléfono")
    def save(self, commit=True):
        tecnico = super().save(commit=False)
        tecnico.user.first_name = self.cleaned_data['nombre']
        tecnico.user.last_name = self.cleaned_data['apellido']
        tecnico.user.email = self.cleaned_data['correo']
        if commit:
            tecnico.save()
            tecnico.user.save()
        return tecnico 
    class Meta:
        model = Tecnico
        fields = ['rut', 'nombre', 'apellido', 'correo', 'direccion', 'telefono']

