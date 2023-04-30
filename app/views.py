from urllib import request
from django.http import response
from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from .forms import *
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
@login_required
def lista_libros(request):
    libros = Libro.objects.all()
    form = AgregarAlCarritoForm()
    return render(request, 'app/lista_libros.html', {'libros': libros, 'form': form})

#funcion para agregar un libro al carrito y sumar las cantidades ingresadas con el id del libro
@login_required
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
@login_required
def ver_carrito(request):
    carrito = Carrito.objects.all()
    total = sum(item.subtotal() for item in carrito)
    context = {
        'carrito': carrito,
        'total': total
    }
    return render(request, 'app/ver_carrito.html', context)

#funcion para eliminar el lo que esta en el carrito
@login_required
def eliminar_del_carrito(request, id):
    carrito = get_object_or_404(Carrito, id=id)
    if request.method == 'POST':
        carrito.delete()
        messages.success(request, f'Se ha eliminado "{carrito.libro.nombre}" del carrito.')
    return redirect('ver_carrito')


# LISTAR DATOS DEL CLIENTE
@login_required
def listar_cliente(request):
    
    clienteall = Cliente.objects.all()
    datos = {
      'listaCliente' : clienteall
    }
    return render(request,'app/listar_cliente.html',datos)

#FORMULARIO PARA MODIFICAR DATOS CLIENTE
@login_required
def modificliente (request, id):
    usuario = Cliente.objects.get(id=id)
    datos = {
        'form' : ClienteForm(instance=usuario)
    }
    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST, files=request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, '¡Modificación exitosa!')
            datos['form'] = formulario

    return render(request, 'app/modificliente.html', datos)


@login_required
def servicioform(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            # Crea una instancia del modelo Servicio sin especificar el campo "id"
            #esto se hace para que el cliente no tenga que ingresar ese campo que no le corresponde
            servicio = Servicio(
                fecha_servicio=form.cleaned_data['fecha_servicio'],
                direccion_servicio=form.cleaned_data['direccion_servicio'],
                detalle_servicio=form.cleaned_data['detalle_servicio'],
                tecnico=form.cleaned_data['tecnico'],
                cliente=form.cleaned_data['cliente'],
                tipo=form.cleaned_data['tipo']
            )
            servicio.save()
    else:
        form = ServicioForm()
    return render(request, 'app/servicioform.html', {'form': form})
