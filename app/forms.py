from genericpath import exists
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

class RegistroUsuarioForm(UserCreationForm):
    
    
    class Meta:
        model= User 
        fields = ['username','password1','password2']

class AgregarAlCarritoForm(forms.Form):
    libro_id = forms.IntegerField(widget=forms.HiddenInput())
    cantidad = forms.IntegerField()

    class Meta:
        
        model = Carrito
      
        fields = ['libro_id','cantidad']



