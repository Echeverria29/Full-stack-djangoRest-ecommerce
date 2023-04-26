from urllib import request
from django.http import response
from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.

import requests
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required


def index(request):
  return render(request,'app/index.html')

#FORMULARIO PARA REGISTRASE A LA PAGINA
def registro(request):
    
  datos = {
        
    'form' : RegistroUsuarioForm()
  }
  if request.method == 'POST':
    formulario = RegistroUsuarioForm(data=request.POST)

    if formulario.is_valid():

      formulario.save()
      #user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
      #login(request,user)
      messages.success(request,'Registrado correctamente!')
      #return redirect(to="home")
      datos["form"] = formulario

  return render(request, 'registration/register.html', datos)

#funcion para listar los libros agregados
def lista_libros(request):
    libros = Libro.objects.all()
    form = AgregarAlCarritoForm()
    return render(request, 'app/lista_libros.html', {'libros': libros, 'form': form})

#funcion para agregar un libro al carrito y sumar las cantidades ingresadas con el id del libro
def agregar_al_carrito(request):
    if request.method == 'POST':
        libro_id = request.POST.get('libro_id')
        cantidad = int(request.POST.get('cantidad', 1))
        libro = get_object_or_404(Libro, id=libro_id)
        carrito = Carrito.objects.filter(libro=libro).first()
        if carrito:
            carrito.cantidad += cantidad
            carrito.save()
            messages.success(request, f'Se han agregado {cantidad} "{libro.nombre}" al carrito.')
        else:
            carrito = Carrito.objects.create(libro=libro, cantidad=cantidad)
            messages.success(request, f'Se ha agregado "{libro.nombre}" al carrito.')
    return redirect('lista_libros')

#funcion para ver los libros agregados al carrito
def ver_carrito(request):
    carrito = Carrito.objects.all()
    total = sum(item.subtotal() for item in carrito)
    context = {
        'carrito': carrito,
        'total': total
    }
    return render(request, 'app/ver_carrito.html', context)

#funcion para eliminar el lo que esta en el carrito
def eliminar_del_carrito(request, id):
    carrito = get_object_or_404(Carrito, id=id)
    if request.method == 'POST':
        carrito.delete()
        messages.success(request, f'Se ha eliminado "{carrito.libro.nombre}" del carrito.')
    return redirect('ver_carrito')