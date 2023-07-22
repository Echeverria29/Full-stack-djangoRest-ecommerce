# Libreria front-back django
Este es un proyecto de una librería desarrollada utilizando Django como framework web y MySQL como base de datos. Esta aplicación es una aplicación full-stack de una libreria web, integrando Api Rest para el seguimiento(simulando starken) y proveedor(alphilia) más paypal como metodo de pago 
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

4.Configura la base de datos para las APIS:
Crea una base de datos MySQL o XAMPP para las APIS que estan en el rar integradas.
(el pago no funciona y en empleado proveedor)
turial XAMPP: https://www.youtube.com/watch?v=BKyqmDwz1pM
Actualiza la configuración de la base de datos en el archivo settings.py en la sección DATABASES con tus credenciales de MySQL(El mismo procedimiento que la apliación principal).

5.Crea un entorno virtual (opcional, pero se recomienda):

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

_Finaliza con un ejemplo de cómo obtener datos del sistema o como usarlos para una pequeña demo_


## Ejecutando las pruebas ⚙️

_Explica como ejecutar las pruebas automatizadas para este sistema_

### Analice las pruebas end-to-end 🔩

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

### Y las pruebas de estilo de codificación ⌨️

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

## Despliegue 📦

_Agrega notas adicionales sobre como hacer deploy_

## Construido con 🛠️

_Menciona las herramientas que utilizaste para crear tu proyecto_

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - El framework web usado
* [Maven](https://maven.apache.org/) - Manejador de dependencias
* [ROME](https://rometools.github.io/rome/) - Usado para generar RSS

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki](https://github.com/tu/proyecto/wiki)

## Versionado 📌

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).

## Autores ✒️

_Menciona a todos aquellos que ayudaron a levantar el proyecto desde sus inicios_

* **Andrés Villanueva** - *Trabajo Inicial* - [villanuevand](https://github.com/villanuevand)
* **Fulanito Detal** - *Documentación* - [fulanitodetal](#fulanito-de-tal)

También puedes mirar la lista de todos los [contribuyentes](https://github.com/your/project/contributors) quíenes han participado en este proyecto. 

## Licencia 📄

Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 🤓.
* Dona con cripto a esta dirección: `0xf253fc233333078436d111175e5a76a649890000`
* etc.



---
⌨️ con ❤️ por [Villanuevand](https://github.com/Villanuevand) 😊
