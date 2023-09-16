# Libreria front-back django
Este es un proyecto de una librería desarrollada utilizando Django como framework web y MySQL como base de datos. Esta aplicación es una aplicación full-stack de una libreria web, integrando Api Rest para el seguimiento(simulando starken) y proveedor(alphilia) más paypal como metodo de pago.
### Caso de uso
[![Caso-de-uso-drawio.png](https://i.postimg.cc/fbjxm95F/Caso-de-uso-drawio.png)](https://postimg.cc/sBxQR1k9)

### Solo se solicitaron algunos de los diagramas 4+1 tales como:

### Vista lógica
[![Logical.png](https://i.postimg.cc/mkw9FfwH/Logical.png)](https://postimg.cc/FkYz26wr)

### 
[![Relational-1.png](https://i.postimg.cc/mDCc9z4q/Relational-1.png)](https://postimg.cc/r0yFXpKC)
### Diagramas de secuencia

### Pago Paypal
[![Diagrama-secuencia-pago.png](https://i.postimg.cc/WzW3v28X/Diagrama-secuencia-pago.png)](https://postimg.cc/N2XY8vWH)

### seguimiento starken
[![Diagrama-secuencia-seguimiento.png](https://i.postimg.cc/tJCTw13s/Diagrama-secuencia-seguimiento.png)](https://postimg.cc/WFCTJ1fV)

### Diagrama de despliegue
[![Diagrama-de-despliegue.png](https://i.postimg.cc/MHr8K548/Diagrama-de-despliegue.png)](https://postimg.cc/K3LW0Px9)

### Index
[![1index.png](https://i.postimg.cc/T3WKPLxK/1index.png)](https://postimg.cc/0zPkWNbv)

[![2index.png](https://i.postimg.cc/Hnxx1j3s/2index.png)](https://postimg.cc/JDfmbr99)

### Registrarse
[![3regis.png](https://i.postimg.cc/Hk5Lgq05/3regis.png)](https://postimg.cc/SnS4LtvN)

### Inicio de sesión
[![4inicioses.png](https://i.postimg.cc/8P75yJjZ/4inicioses.png)](https://postimg.cc/qzd4q7cK)

### Tienda
[![5tienda.png](https://i.postimg.cc/Pf3JzzrL/5tienda.png)](https://postimg.cc/mh9TT99R)

### Carrito
[![6carrito.png](https://i.postimg.cc/TPVhrzpG/6carrito.png)](https://postimg.cc/DWz2hYrY)

### Pago con PayPal
[![7pagopaypal.png](https://i.postimg.cc/sX0BXpMZ/7pagopaypal.png)](https://postimg.cc/vgf82xLQ)

### Comenzando 🚀

Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.

### Pre-requisitos 📋
Antes de comenzar, asegúrate de tener instalados los siguientes requisitos:

1.Python: Para instalar Django, necesitarás tener Python instalado en tu sistema. Puedes descargar la última versión de Python desde su sitio web oficial: https://www.python.org/downloads/

2.Anaconda: Puedes descargar la última versión de Python desde su sitio web oficial: 
https://www.anaconda.com/

3.MySQL: Asegúrate de tener una instancia de MySQL instalada y configurada.
Puedes descargar MySQL desde su sitio web oficial:
https://www.mysql.com/downloads/

4.XAMPP: En caso de que no puedas instalar My SQL por espacio, prueba esta alternativa.
Puedes descargar XAMPP desde su sitio web oficial:
https://www.apachefriends.org/es/download.html
tutorial: https://www.youtube.com/watch?v=MtllDrDm4cM

### Instalación 🔧

_Una serie de ejemplos paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_

1.Instala las dependencias necesarias:

```
pip install -r requirements.txt
```

2.Configura la base de datos principal:
Crea una base de datos MySQL o XAMPP para el proyecto.
turial XAMPP: https://www.youtube.com/watch?v=BKyqmDwz1pM
Actualiza la configuración de la base de datos en el archivo settings.py en la sección DATABASES con tus credenciales de MySQL.

3.Realiza las migraciones:

```
python manage.py migrate
```
4.Ejecuta el servidor de desarrollo:

```
python manage.py runserver
```

5.Configura la base de datos para las APIS:
Crea una base de datos MySQL o XAMPP para las APIS que estan en el rar integradas
(Tienen que estar funcionando las apis en simultaneo para el funcionamiento completo del proyecto).
turial XAMPP: https://www.youtube.com/watch?v=BKyqmDwz1pM
Actualiza la configuración de la base de datos en el archivo settings.py en la sección DATABASES con tus credenciales de MySQL(El mismo procedimiento que la apliación principal).

6.Bases de datos con entorno virtual(opcional, esto es si no pudiste con la forma de arriba):

Tutorial: https://www.youtube.com/watch?v=SXVdnEGetPI
```
python -m venv myenv
```

Activar el entorno virtual:

En Windows:

```
myenv\Scripts\activate
```

En macOS y Linux:

```
source myenv/bin/activate
```

Realiza las migraciones:

```
python manage.py migrate
```

Ejecuta el servidor de desarrollo:

```
python manage.py runserver
```

4.Accede a la aplicación principal en tu navegador visitando http://localhost:8000/.

  Accede a la aplicación starken APi en tu navegador visitando http://localhost:8080/.
  
  Accede a la aplicación alphilia en tu navegador visitando http://localhost:8001/.


## Ejecutando las pruebas ⚙️

Para ejecutar las pruebas automatizadas para este sistema, utiliza el siguiente comando:

```
python manage.py test
```

### Analice las pruebas end-to-end 🔩

Las pruebas end-to-end verifican que todas las partes de la aplicación, tanto el front-end como el back-end, funcionen correctamente en conjunto. Estas pruebas prueban los flujos de trabajo completos del sistema para garantizar su correcto funcionamiento.

### Y las pruebas de estilo de codificación ⌨️

Las pruebas de estilo de codificación aseguran que el código escrito siga las pautas y convenciones establecidas por el proyecto. Esto ayuda a mantener un código limpio y fácilmente comprensible para todos los colaboradores.


## Construido con 🛠️

Las herramientas utilizadas para crear este proyecto son:

Django - El framework web utilizado.
MySQL - Base de datos utilizada.
Boostrap - Diseño web.
SASS - Diseño web.
Otros paquetes y dependencias de Python especificados en requirements.txt.

## Autores ✒️

* **Orlando Echeverría Hernandez** - *Proyecto completo* - [Echeverría](https://github.com/Echeverria29)


## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 🤓.
* Dona con cripto a esta dirección: 0xf253fc233333078436d111175e5a76a649890000 (broma, ¡no es una dirección real! 😄)

---
⌨️ con ❤️ por [Echeverría](https://github.com/Echeverria29) 😊
¡Gracias por interesarte en este proyecto! Si tienes alguna pregunta o necesitas ayuda, no dudes en comunicarte con nosotros. ¡Disfruta trabajando con Django y MySQL!
