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
from django.core.exceptions import ValidationError

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


@login_required
def listar_personas(request):
    cliente = Cliente.objects.all()

     
    datos = {
        #como dato estas listas van en las paginas listar_...
        
        'listaClientes': cliente,
      
        
    }
    return render(request, 'app/listar_personas.html', datos)

@login_required
def listar_empleado(request):
    empleado = Empleado.objects.all()
    cantidad_empleados = empleado.count()
    datos = {
        #como dato estas listas van en las paginas listar_...
        'listaEmpleado': empleado,
        'cantidad_empleados': cantidad_empleados
    }
    return render(request, 'app/listar_empleado.html', datos)


@login_required
def listar_tecnico(request):
    tecnicos = Tecnico.objects.all()
    cantidad_tecnicos = tecnicos.count()
    datos = {
        'listaTecnico': tecnicos,
        'cantidad_tecnicos': cantidad_tecnicos
    }
    return render(request, 'app/listar_tecnico.html', datos)


@login_required
def listar_materiales(request):
    materiales = Materiales.objects.all()
    tecnico= Tecnico.objects.all()
    datos = {
        'listaMateriales': materiales,
        'listaTecnico': tecnico,
        
    }
    return render(request, 'app/listar_materiales.html', datos)


@login_required
def listar_servicio(request):
    servicio = Servicio.objects.all()
    tecnico= Tecnico.objects.all()
    datos = {
        'listaServicio': servicio,
        'listaTecnico'  :tecnico,
    }
    return render(request, 'app/listar_servicio.html', datos)

@login_required
def listar_serviciotec(request):
    servicio = Servicio.objects.all()
    tecnico= Tecnico.objects.all()
    datos = {
        'listaServicio2': servicio,
        'listaTecnico2'  :tecnico,
    }
    return render(request, 'app/listar_serviciotec.html', datos)

@login_required
def listar_cotizaciones(request):
    cotizacion = Cotizaciones.objects.all()
    cliente= Cliente.objects.all()
    datos = {
        'listaCotizacion': cotizacion,
        'listaCliente2'  :cliente,
    }
    return render(request, 'app/listar_cotizaciones.html', datos)

@login_required
def empleadoform(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            # Crea una instancia del modelo Servicio sin especificar el campo "id"
            #esto se hace para que el cliente no tenga que ingresar ese campo que no le corresponde
            #digando agrega igual ese id . idealmente realizar trigger en base de datos para que 
            #ese id sea autoincrementable
            empleado = Empleado(
                rut_empleado=form.cleaned_data['rut_empleado'],
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                correo=form.cleaned_data['correo'],
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono'],
                cargo=form.cleaned_data['cargo'],
                departamento=form.cleaned_data['departamento'],
                
            )
            empleado.save()
            messages.success(request,'Datos agregados correctamente!')
    else:
        form = EmpleadoForm()
    return render(request, 'app/empleadoform.html', {'form': form})

@login_required
def modifiempleado (request, id):
    usuario = Empleado.objects.get(id=id)
    datos = {
        'form' : EmpleadoForm(instance=usuario)
    }
    if request.method == 'POST':
        formulario = EmpleadoForm(data=request.POST, files=request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, '¡Modificación de datos exitosa!')
            datos['form'] = formulario

    return render(request, 'app/modifiempleado.html', datos)

@login_required
def modificliempleado (request, id):
    usuario = Cliente.objects.get(id=id)
    datos = {
        'form' : ClienteForm(instance=usuario)
    }
    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST, files=request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, '¡Modificación de datos exitosa!')
            datos['form'] = formulario

    return render(request, 'app/modifiempleado.html', datos)

def eliminarpersona(request,id):

  cliemple = Cliente.objects.get(id=id)
  cliemple.delete()
  messages.success(request,'Cliente eliminado!')

  return redirect(to="listar_personas")


@login_required
def tecnicoform(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST)
        if form.is_valid():
            # Crea una instancia del modelo Servicio sin especificar el campo "id"
            #esto se hace para que el cliente no tenga que ingresar ese campo que no le corresponde
            #digando agrega igual ese id . idealmente realizar trigger en base de datos para que 
            #ese id sea autoincrementable
            tecnico = Tecnico(
                rut_tecnico=form.cleaned_data['rut_tecnico'],
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                correo=form.cleaned_data['correo'],
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono'],
                
            )
            tecnico.save()
            messages.success(request,'Datos agregados correctamente!')
    else:
        form = TecnicoForm()
    return render(request, 'app/tecnicoform.html', {'form': form})

@login_required
def materialesform(request):
    if request.method == 'POST':
        form = MaterialesForm(request.POST)
        if form.is_valid():
            # Crea una instancia del modelo Servicio sin especificar el campo "id"
            #esto se hace para que el cliente no tenga que ingresar ese campo que no le corresponde
            #digando agrega igual ese id . idealmente realizar trigger en base de datos para que 
            #ese id sea autoincrementable
            materiales = Materiales(
                
                nombre=form.cleaned_data['nombre'],
                stock=form.cleaned_data['stock'],
                tecnico_id=form.cleaned_data['tecnico_id'],
            )
            materiales.save()
            messages.success(request,'Datos agregados correctamente!')
    else:
        form = MaterialesForm()
    return render(request, 'app/materialesform.html', {'form': form})





@login_required
def modifitecnico (request, id):
    usuario = Tecnico.objects.get(id=id)
    datos = {
        'form' : TecnicoForm(instance=usuario)
    }
    if request.method == 'POST':
        formulario = TecnicoForm(data=request.POST, files=request.FILES, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, '¡Modificación de datos exitosa!')
            datos['form'] = formulario

    return render(request, 'app/modifitecnico.html', datos)


# LISTAR DATOS DEL CLIENTE
@login_required
def listar_cliente(request):
    clientes = Cliente.objects.all()
    cantidad_clientes = clientes.count()
    datos = {
        'listaCliente': clientes,
        'cantidad_clientes': cantidad_clientes
    }
    return render(request, 'app/listar_cliente.html', datos)


#FORMULARIO PARA AGREGAR DATOS DEL CLIENTE,ESTE AGREGA AUTOMATICAMENTE EL ID SIN QUE EL USUARIO LO TENGA QUE ESCRIBIR
@login_required
def clienteform(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            # Crea una instancia del modelo Servicio sin especificar el campo "id"
            #esto se hace para que el cliente no tenga que ingresar ese campo que no le corresponde
            #digando agrega igual ese id . idealmente realizar trigger en base de datos para que 
            #ese id sea autoincrementable
            cliente = Cliente(
                rut_cliente=form.cleaned_data['rut_cliente'],
                nombre=form.cleaned_data['nombre'],
                apellido=form.cleaned_data['apellido'],
                correo=form.cleaned_data['correo'],
                direccion=form.cleaned_data['direccion'],
                telefono=form.cleaned_data['telefono'],
                numero_tarjeta=form.cleaned_data['numero_tarjeta']
            )
            cliente.save()
            messages.success(request,'Datos agregados correctamente!')
    else:
        form = ClienteForm()
    return render(request, 'app/clienteform.html', {'form': form})




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
            messages.success(request, '¡Modificación de datos exitosa!')
            datos['form'] = formulario

    return render(request, 'app/modificliente.html', datos)


#FORMULARIO DE SOLICITAR SERVICIO,ESTE AGREGA AUTOMATICAMENTE EL ID SIN QUE EL USUARIO LO TENGA QUE ESCRIBIR
@login_required
def servicioform(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            # Verifica si la fecha y hora ya está ocupada
            fecha_servicio = form.cleaned_data['fecha_servicio']
            if Servicio.objects.filter(fecha_servicio=fecha_servicio).exists():
                form.add_error('fecha_servicio', 'Esta hora ya está ocupada, por favor elija otra hora.')
            
            else:
                # Crea una instancia del modelo Servicio sin especificar el campo "id"
                # esto se hace para que el cliente no tenga que ingresar ese campo que no le corresponde
                # digando agrega igual ese id . idealmente realizar trigger en base de datos para que
                # ese id sea autoincrementable
                servicio = Servicio(
                    fecha_servicio=fecha_servicio,
                    direccion_servicio=form.cleaned_data['direccion_servicio'],
                    detalle_servicio=form.cleaned_data['detalle_servicio'],
                    tecnico=form.cleaned_data['tecnico'],
                    cliente=form.cleaned_data['cliente'],
                    tipo=form.cleaned_data['tipo']
                )
                servicio.save()
                messages.success(request, 'Servicio agendado correctamente!')
    else:
        form = ServicioForm()
    return render(request, 'app/servicioform.html', {'form': form})


@login_required
def cotizacionesform(request):
    if request.method == 'POST':
        form = CotizacionesForm(request.POST)
        if form.is_valid():
            # Verifica si la fecha y hora ya está ocupada
            fecha = form.cleaned_data['fecha']
            if Cotizaciones.objects.filter(fecha=fecha).exists():
                form.add_error('fecha', 'Esta hora ya está ocupada, por favor elija otra hora.')
            
            else:
                # Crea una instancia del modelo Servicio sin especificar el campo "id"
                # esto se hace para que el cliente no tenga que ingresar ese campo que no le corresponde
                # digando agrega igual ese id . idealmente realizar trigger en base de datos para que
                # ese id sea autoincrementable
                cotizaciones = Cotizaciones(
                    fecha=form.cleaned_data['fecha'],
                    correo=form.cleaned_data['correo'],
                    detalle=form.cleaned_data['detalle'],                  
                    cliente=form.cleaned_data['cliente'],
                )
                cotizaciones.save()
                messages.success(request, 'Cotizacion enviada correctamente')
    else:
        form = CotizacionesForm()
    return render(request, 'app/cotizacionesform.html', {'form': form})

