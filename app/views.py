
from django.shortcuts import render,redirect,get_object_or_404

import requests
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError
from datetime import date
from django.db import transaction
from django.contrib.auth import logout
from django.contrib.auth.models import User

def comprafinalizada(request):
    return render(request,'app/comprafinalizada.html')

def home(request):
  return render(request,'app/home.html')

def index(request):
  return render(request,'app/index.html')

def indexpypal(request):
  return render(request,'app/indexpypal.html')

 
@login_required
def realizar_comprastarken(request):
    carrito = Carrito.objects.all()  # Obtener el  objetos del modelo Carrito del usuario actual
    cliente = Cliente.objects.filter(user=request.user).first()  # Obtener el objeto Cliente del usuario actual
    
    # Iterar sobre cada objeto en el carrito
    for item in carrito:
        libro = item.libro  # Obtener el libro del carrito
        nombreProducto = item.libro.nombre  # Obtener el nombre del producto del objeto del carrito
        cantidad = item.cantidad  # Obtener la cantidad del producto del objeto del carrito
        estado = 'pendiente'  # Establecer el estado del producto como "pendiente"
        item_id = item.id  # Obtener el ID del objeto del carrito

        # Iterar sobre cada objeto en el modelo Cliente (suponiendo que solo hay un cliente)
        rut = cliente.rut
        nombre = cliente.nombre
        apellido = cliente.apellido
        direccion = cliente.direccion
        telefono = cliente.telefono

        # Crear el objeto Producto en la base de datos de la API mediante una solicitud POST
        url_api = 'http://127.0.0.1:8080/api/starken/'  # URL de la API donde se creará el objeto Producto (reemplaza con la URL correcta)
        data = {
            'id': item_id,
            'rut': rut,
            'nombre': nombre,
            'apellido': apellido,
            'direccion': direccion,
            'telefono': telefono,
            'nombreProducto': nombreProducto,
            'cantidad': cantidad,
            'estado': estado
        }
        response = requests.post(url_api, json=data)  # Realizar una solicitud POST a la API con los datos del objeto Producto
        if request.method == 'POST':

            total = sum(item.subtotal() for item in carrito)

            # Obtener el cliente y empleado de la base de datos
            cliente = Cliente.objects.first()
            empleado = Empleado.objects.first()

            with transaction.atomic():
                # Crear una nueva venta
                venta = Venta(
                    fecha_venta=date.today(),
                    total=total,
                    cliente=cliente,
                    empleado=empleado
                )
                venta.save()

                # Obtener el objeto Venta recién creado
                venta = Venta.objects.latest('id')

                # Crear un nuevo pago relacionado con la venta
                pago = Pago(
                    total=total,
                    venta=venta
                )
                pago.save()
                libro.stock -= item.cantidad  # Actualizar el stock del libro
                libro.save()  # Guardar los cambios en el libro
        
        if response.status_code == 201:  # Verificar que el objeto se haya creado exitosamente en la API (código de estado 201)
            item.delete()  # Eliminar el elemento del carrito solo si se creó correctamente en la API
        else:
            error_message = f'Error al crear el objeto Producto: {response.content.decode()}'
            messages.error(request, error_message)  # Mostrar un mensaje de error en caso de que falle la creación del objeto

    
    return redirect('indexpypal')  # Redirigir al usuario a la lista de libros después de realizar las compras

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('index')

def crearclienteform(request):
    if request.method == 'POST':
        form = Crearclienteform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado correctamente')
    else:
        form = Crearclienteform()
    return render(request, 'app/crearclienteform.html', {'form': form})

  
def crearempleadoform(request):
    if request.method == 'POST':
        form = Crearempleadoform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado registrado correctamente')
    else:
        form = Crearempleadoform()
    return render(request, 'app/crearempleadoform.html', {'form': form})

  
#FORMULARIO PARA MODIFICAR DATOS CLIENTE
@login_required
def modificliente (request, id):
    cliente = Cliente.objects.get(user_id=id)
    datos = {
        'form' : ModificarClienteForm(instance=cliente)
    }
    if request.method == 'POST':
        formulario = ModificarClienteForm(data=request.POST, files=request.FILES, instance=cliente)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, '¡Modificación de datos exitosa!')
            datos['form'] = formulario

    return render(request, 'app/modificliente.html', datos)

@login_required
def modifiempleado (request, id):
    empleado = Empleado.objects.get(user_id=id)
    datos = {
        'form' : ModificarEmpleadoForm(instance=empleado)
    }
    if request.method == 'POST':
        formulario = ModificarEmpleadoForm(data=request.POST, files=request.FILES, instance=empleado)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, '¡Modificación de datos exitosa!')
            datos['form'] = formulario

    return render(request, 'app/modifiempleado.html', datos)




#funcion para listar los libros agregados
@login_required
def lista_libros(request):
    libros = Libro.objects.all()
    form = AgregarAlCarritoForm()
    return render(request, 'app/lista_libros.html', {'libros': libros, 'form': form})

#FUNCION PARA LISTAR EL SEGUIMIENTO DE API STARKEN
@login_required
def starken_api(request):
    rut = request.user.cliente.rut  # Obtener el rut del cliente actualmente autenticado
    
    url = 'http://127.0.0.1:8080/api/starken/'  # URL de la API de seguimiento de Starken (reemplaza con la URL correcta)
    response = requests.get(url)  # Realizar una solicitud GET a la API de seguimiento de Starken

    if response.status_code == 200:  # Verificar que la solicitud haya sido exitosa (código de estado 200)
        starkenapi = response.json()  # Obtener los datos de la respuesta JSON y guardarlos en la variable starkenapi
        
        # Filtrar los datos de seguimiento por el rut del cliente actual
        starkenapi_filtrado = [item for item in starkenapi if item['rut'] == rut]

        return render(request, 'app/starken_api.html', {'starkenapi': starkenapi_filtrado})
    else:
        # Manejar el error en caso de que la solicitud no sea exitosa
        return render(request, 'error.html', {'mensaje': 'Error al obtener el seguimiento'})





#FUNCION PARA LISTAR LOS LIBROS DE LA API DE ALPHILIA
@login_required
def libros_api(request):
    url = 'http://127.0.0.1:8001/api/libros/'  # URL de la API de libros de Alphilia (reemplaza con la URL correcta)
    response = requests.get(url)  # Realiza una solicitud GET a la API de libros de Alphilia

    if response.status_code == 200:  # Verifica que la solicitud haya sido exitosa (código de estado 200)
        librosimagina = response.json()  # Obtiene los datos de la respuesta JSON y los guarda en la variable librosimagina

        return render(request, 'app/libros_api.html', {'librosimagina': librosimagina})  # Renderiza la plantilla 'libros_api.html' y pasa los datos de librosimagina como contexto
    else:
        # Maneja el error en caso de que la solicitud no sea exitosa
        return render(request, 'app/error.html', {'mensaje': 'Error al obtener los libros'})  # Renderiza la plantilla 'error.html' y pasa un mensaje de error como contexto





#funcion para agregar un libro al carrito y sumar las cantidades ingresadas con el id del libro
@login_required
def agregar_al_carrito(request):
    if request.method == 'POST':
        libro_id = request.POST.get('libro_id')
        cantidad = int(request.POST.get('cantidad', 1))
        libro = get_object_or_404(Libro, id=libro_id)
        carrito = Carrito.objects.filter(usuario=request.user, libro=libro).first()
        if carrito:
            carrito.cantidad += cantidad
            carrito.save()
            messages.success(request, f'Se han agregado {cantidad} "{libro.nombre}" al carrito.')
        else:
            carrito = Carrito.objects.create(usuario=request.user, libro=libro, cantidad=cantidad)
            messages.success(request, f'Se ha agregado "{libro.nombre}" al carrito.')
    return redirect('../lista_libros')


#funcion para ver los libros agregados al carrito

@login_required
def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user)
    total = sum(item.subtotal() for item in carrito)
    context = {
        'carrito': carrito,
        'total': total
    }
    return render(request, 'app/ver_carrito.html', context)



#funcion para eliminar el lo que esta en el carrito
@login_required
def eliminar_del_carrito(request, id):
    carrito = get_object_or_404(Carrito, id=id,usuario=request.user)
    if request.method == 'POST':
        carrito.delete()
        messages.error(request, f'Se ha eliminado "{carrito.libro.nombre}" del carrito.')
    return redirect('ver_carrito')

#FUNCION PARA LISTAR LOS DATOS DEL CLIENTE LA PAGINA PRINCIPAL
@login_required
def listar_personas(request):
    cliente = Cliente.objects.all()
    
     
    datos = {
        #como dato estas listas van en las paginas listar_...
        
        'listaClientes': cliente,
        
        
    }
    return render(request, 'app/listar_personas.html', datos)


#FUNCION PARA LISTAR LOS DATOS DE LOS MATERIALES DEL TECNICO
@login_required
def listar_materiales(request):
    materiales = Materiales.objects.all()
    tecnico= Tecnico.objects.all()
    datos = {
        'listaMateriales': materiales,
        'listaTecnico': tecnico,
        
    }
    return render(request, 'app/listar_materiales.html', datos)

#FUNCION PARA LISTAR LOS SERVICIOS SOLICITADOS AL TECNICO
@login_required
def listar_servicio(request):
    servicio = Servicio.objects.all()
    tecnico= Tecnico.objects.all()
    datos = {
        'listaServicio': servicio,
        'listaTecnico'  :tecnico,
    }
    return render(request, 'app/listar_servicio.html', datos)


#FUNCION PARA LISTAR LOS SERVICIOS SOLICITADOS AL TECNICO
@login_required
def listar_serviciotec(request):
    servicio = Servicio.objects.all()
    tecnico= Tecnico.objects.all()
    datos = {
        'listaServicio2': servicio,
        'listaTecnico2'  :tecnico,
    }
    return render(request, 'app/listar_serviciotec.html', datos)

#FUNCION PARA LISTAR LAS COTIZACIONS PEDIDAS POR EL CLIENTE
@login_required
def listar_cotizaciones(request):
    cotizacion = Cotizaciones.objects.all()
    cliente= Cliente.objects.all()
    datos = {
        'listaCotizacion': cotizacion,
        'listaCliente2'  :cliente,
    }
    return render(request, 'app/listar_cotizaciones.html', datos)





#FUNCION PARA ELIMINAR LOS CLIENTES DEL EMPLEADO

def eliminarpersona(request, id):
    cliente = Cliente.objects.get(user_id=id)
    user = cliente.user

    # Eliminar el cliente y el usuario
    cliente.delete()
    user.delete()

    messages.success(request, 'Cliente eliminado!')

    return redirect('listar_personas')

#FUNCION PARA GUARDAR LOS DATOS DE LOS MATERIALES
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

#FUNCION PARA GUARDAR LOS DATOS DE COTIZACIONES DESDE EL CLIENTE
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

