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
from django.core.exceptions import ValidationError
import requests
from django.utils import timezone
from django.db import connection
from datetime import date

from django.db import transaction


def index(request):
  return render(request,'app/index.html')

@login_required
def realizar_compra(request):
    carrito = Carrito.objects.all()  # Obtener todos los objetos del modelo Carrito
    cliente = Cliente.objects.all()  # Obtener todos los objetos del modelo Cliente
    saldo_tarjeta_url = 'http://127.0.0.1:8002/api/tarjetas/1/'  # URL de la API para obtener el saldo de la tarjeta
    url_api_pagos = 'http://127.0.0.1:8002/api/pagos/'  # URL de la API para realizar el pago
    url_api_starken = 'http://127.0.0.1:8080/api/starken/'  # URL de la API de Starken (reemplaza con la URL correcta)

    try:
        response = requests.get(saldo_tarjeta_url)  # Realizar una solicitud GET a la URL de la API de saldo de tarjeta
        if response.status_code == 200:
            saldo_tarjeta = response.json().get('saldo')  # Obtener el saldo de la tarjeta de la respuesta JSON
        else:
            error_message = f'Error al obtener el saldo de la tarjeta: {response.content.decode()}'
            messages.error(request, error_message)
            return redirect('lista_libros')
    except requests.exceptions.RequestException as e:
        error_message = f'Error al conectar con la API de tarjetas: {str(e)}'
        messages.error(request, error_message)
        return redirect('lista_libros')

    for item in carrito:  # Iterar sobre los objetos en el carrito
        libro = item.libro  # Obtener el libro del carrito
        libro.stock -= item.cantidad  # Actualizar el stock del libro
        libro.save()  # Guardar los cambios en el libro
        nombreProducto = item.libro.nombre
        cantidad = item.cantidad
        estado = 'pendiente'
        item_id = item.id

        for x in cliente:  # Obtener los datos del cliente para usarlos en la API de Starken
            nombre = x.nombre
            apellido = x.apellido
            direccion = x.direccion
            telefono = x.telefono
            numerodetarjeta = x.numero_tarjeta

        monto = sum(item.subtotal() for item in carrito)  # Calcular el monto total de la compra
        saldo_total = saldo_tarjeta - monto  # Calcular el saldo restante después de la compra

        if saldo_total < 0:
            error_message = 'Saldo insuficiente. No se puede realizar la compra.'
            messages.error(request, error_message)
            return redirect('lista_libros')

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

        # Actualizar el saldo en la API de tarjetas
        data_tarjetas = {'id': 1, 'numerodetarjeta': numerodetarjeta, 'nombre': nombre, 'apellido': apellido, 'saldo': saldo_total}
        try:
            response_tarjetas = requests.put(saldo_tarjeta_url, json=data_tarjetas)  # Realizar una solicitud PUT a la API de saldo de tarjeta para actualizar el saldo
            if response_tarjetas.status_code != 200:
                error_message = f'Error al actualizar el saldo de la tarjeta: {response_tarjetas.content.decode()}'
                messages.error(request, error_message)
                return redirect('lista_libros')
        except requests.exceptions.RequestException as e:
            error_message = f'Error al conectar con la API de tarjetas: {str(e)}'
            messages.error(request, error_message)
            return redirect('lista_libros')

        # Agregar la compra a la API de pagos
        data_pagos = {'id': item_id, 'numerodetarjeta': numerodetarjeta, 'nombre': nombre, 'apellido': apellido, 'monto': monto, 'saldofinal': saldo_total}
        try:
            response_pagos = requests.post(url_api_pagos, json=data_pagos)  # Realizar una solicitud POST a la API de pagos para crear un nuevo objeto de pago
            if response_pagos.status_code == 201:
                # Agregar el producto a Starken solo si la compra fue realizada correctamente
                data_starken = {'id': item_id, 'nombre': nombre, 'apellido': apellido, 'direccion': direccion, 'telefono': telefono, 'nombreProducto': nombreProducto, 'cantidad': cantidad, 'estado': estado}
                response_starken = requests.post(url_api_starken, json=data_starken)  # Realizar una solicitud POST a la API de Starken para crear un nuevo objeto de producto

                if response_starken.status_code != 201:
                    error_message = f'Error al crear el objeto Producto en la API de Starken: {response_starken.content.decode()}'
                    messages.error(request, error_message)
            else:
                error_message = f'Error al crear el objeto Pago: {response_pagos.content.decode()}'
                messages.error(request, error_message)
                return redirect('lista_libros')
        except requests.exceptions.RequestException as e:
            error_message = f'Error al conectar con la API de pagos: {str(e)}'
            messages.error(request, error_message)
            return redirect('lista_libros')

    item.delete()  # Eliminar el objeto del carrito
    messages.success(request, 'Compra realizada exitosamente.')
    return redirect('lista_libros')



@login_required
def realizar_comprastarken(request):
    carrito = Carrito.objects.all()  # Obtener todos los objetos del modelo Carrito
    cliente = Cliente.objects.all()  # Obtener todos los objetos del modelo Cliente
    
    # Iterar sobre cada objeto en el carrito
    for item in carrito:
        nombreProducto = item.libro.nombre  # Obtener el nombre del producto del objeto del carrito
        cantidad = item.cantidad  # Obtener la cantidad del producto del objeto del carrito
        estado = 'pendiente'  # Establecer el estado del producto como "pendiente"
        item_id = item.id  # Obtener el ID del objeto del carrito

        # Iterar sobre cada objeto en el modelo Cliente (suponiendo que solo hay un cliente)
        for x in cliente:
            nombre = x.nombre  # Obtener el nombre del cliente
            apellido = x.apellido  # Obtener el apellido del cliente
            direccion = x.direccion  # Obtener la dirección del cliente
            telefono = x.telefono  # Obtener el número de teléfono del cliente

        # Crear el objeto Producto en la base de datos de la API mediante una solicitud POST
        url_api = 'http://127.0.0.1:8080/api/starken/'  # URL de la API donde se creará el objeto Producto (reemplaza con la URL correcta)
        data = {
            'id': item_id,
            'nombre': nombre,
            'apellido': apellido,
            'direccion': direccion,
            'telefono': telefono,
            'nombreProducto': nombreProducto,
            'cantidad': cantidad,
            'estado': estado
        }
        response = requests.post(url_api, json=data)  # Realizar una solicitud POST a la API con los datos del objeto Producto

        if response.status_code == 201:  # Verificar que el objeto se haya creado exitosamente en la API (código de estado 201)
            item.delete()  # Eliminar el elemento del carrito solo si se creó correctamente en la API
        else:
            error_message = f'Error al crear el objeto Producto: {response.content.decode()}'
            messages.error(request, error_message)  # Mostrar un mensaje de error en caso de que falle la creación del objeto

    messages.success(request, 'Compra realizada exitosamente.')  # Mostrar un mensaje de éxito si todas las compras se realizan correctamente
    return redirect('lista_libros')  # Redirigir al usuario a la lista de libros después de realizar las compras


@login_required
def realizar_pagotarjeta(request):
    carrito = Carrito.objects.all()  # Obtener todos los objetos del modelo Carrito
    cliente = Cliente.objects.first()  # Obtener el primer objeto del modelo Cliente
    saldo_tarjeta_url = 'http://127.0.0.1:8002/api/tarjetas/1/'  # URL de la API para obtener el saldo de la tarjeta
    url_api_pagos = 'http://127.0.0.1:8002/api/pagos/'  # URL de la API para realizar el pago

    try:
        response = requests.get(saldo_tarjeta_url)  # Realizar una solicitud GET a la URL de la API de saldo de tarjeta
        if response.status_code == 200:
            saldo_tarjeta = response.json().get('saldo')  # Obtener el saldo de la tarjeta de la respuesta JSON
        else:
            error_message = f'Error al obtener el saldo de la tarjeta: {response.content.decode()}'
            messages.error(request, error_message)
            return redirect('lista_libros')
    except requests.exceptions.RequestException as e:
        error_message = f'Error al conectar con la API de tarjetas: {str(e)}'
        messages.error(request, error_message)
        return redirect('lista_libros')

    for item in carrito:  # Iterar sobre los objetos en el carrito
        libro = item.libro  # Obtener el libro del carrito
        libro.stock -= item.cantidad  # Actualizar el stock del libro
        libro.save()  # Guardar los cambios en el libro
        item_id = item.id

    # Obtener los datos del cliente
    nombre = cliente.nombre
    apellido = cliente.apellido
    numerodetarjeta = cliente.numero_tarjeta

    monto = sum(item.subtotal() for item in carrito)  # Calcular el monto total de la compra
    saldo_total = saldo_tarjeta - monto  # Calcular el saldo restante después de la compra

    if saldo_total < 0:
        error_message = 'Saldo insuficiente. No se puede realizar la compra.'
        messages.error(request, error_message)
        return redirect('lista_libros')

    if request.method == 'POST':
        total = sum(item.subtotal() for item in carrito)

    # Actualizar el saldo en la API de tarjetas
    data_tarjetas = {'id': 1, 'numerodetarjeta': numerodetarjeta, 'nombre': nombre, 'apellido': apellido, 'saldo': saldo_total}
    try:
        response_tarjetas = requests.put(saldo_tarjeta_url, json=data_tarjetas)  # Realizar una solicitud PUT a la API de saldo de tarjeta para actualizar el saldo
        if response_tarjetas.status_code != 200:
            error_message = f'Error al actualizar el saldo de la tarjeta: {response_tarjetas.content.decode()}'
            messages.error(request, error_message)
            return redirect('lista_libros')
    except requests.exceptions.RequestException as e:
        error_message = f'Error al conectar con la API de tarjetas: {str(e)}'
        messages.error(request, error_message)
        return redirect('lista_libros')

    # Agregar el saldo total en la API de pagos
    data_pagos = {'id': item_id, 'numerodetarjeta': numerodetarjeta, 'nombre': nombre, 'apellido': apellido, 'monto': monto, 'saldofinal': saldo_total}
    try:
        response_pagos = requests.post(url_api_pagos, json=data_pagos)  # Realizar una solicitud POST a la API de pagos para crear un nuevo objeto de pago
        if response_pagos.status_code != 201:
            error_message = f'Error al crear el objeto Pago: {response_pagos.content.decode()}'
            messages.error(request, error_message)
            return redirect('lista_libros')
    except requests.exceptions.RequestException as e:
        error_message = f'Error al conectar con la API de pagos: {str(e)}'
        messages.error(request, error_message)
        return redirect('lista_libros')

    for item in carrito:
        item.delete()  # Eliminar los objetos del carrito

    messages.success(request, 'Compra realizada exitosamente.')
    return redirect('lista_libros')


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

#FUNCION PARA LISTAR EL SEGUIMIENTO DE API STARKEN
@login_required
def starken_api(request):
    url = 'http://127.0.0.1:8080/api/starken/'  # URL de la API de seguimiento de Starken (reemplaza con la URL correcta)
    response = requests.get(url)  # Realiza una solicitud GET a la API de seguimiento de Starken

    if response.status_code == 200:  # Verifica que la solicitud haya sido exitosa (código de estado 200)
        starkenapi = response.json()  # Obtiene los datos de la respuesta JSON y los guarda en la variable starkenapi

        return render(request, 'app/starken_api.html', {'starkenapi': starkenapi})  # Renderiza la plantilla 'starken_api.html' y pasa los datos de starkenapi como contexto
    else:
        # Maneja el error en caso de que la solicitud no sea exitosa
        return render(request, 'app/error.html', {'mensaje': 'Error al obtener el seguimiento'})  # Renderiza la plantilla 'error.html' y pasa un mensaje de error como contexto






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

#FUNCION PARA LISTAR LOS DATOS DEL EMPLEADO PAGINA PRINCIPAL
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

#FUNCION PARA LISTAR LOS DATOS DEL TECNICO PAGINA PRINCIPAL
@login_required
def listar_tecnico(request):
    tecnicos = Tecnico.objects.all()
    cantidad_tecnicos = tecnicos.count()
    datos = {
        'listaTecnico': tecnicos,
        'cantidad_tecnicos': cantidad_tecnicos
    }
    return render(request, 'app/listar_tecnico.html', datos)

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

#FORM PARA GUARDAR LOS DATOS DEL EMPLEADO
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

#FUNCION PARA MODIFICAR AL EMPLEADO
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

#FUNCION PARA MODIFICAR LOS CLIENTES DEL EMPLEADO
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

#FUNCION PARA ELIMINAR LOS CLIENTES DEL EMPLEADO
def eliminarpersona(request,id):

  cliemple = Cliente.objects.get(id=id)
  cliemple.delete()
  messages.success(request,'Cliente eliminado!')

  return redirect(to="listar_personas")

#FORM PARA GUARDAR LOS DATOS DEL TECNICO
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




#FUNCION PARA MODIFICAR EL TECNICO
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

