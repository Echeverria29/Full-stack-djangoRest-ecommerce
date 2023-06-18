from operator import index
from unicodedata import name
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
  path('login/', iniciar_sesion, name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
  path('crear_empleado/', crear_empleado, name='crear_empleado'),
  path('crear_tecnico/', crear_tecnico, name='crear_tecnico'),
  path('crear_cliente/', crear_cliente, name='crear_cliente'),
  path('home/', home, name='home'),
  path('index/', index, name='index'),
  path('indexpypal/', indexpypal, name='indexpypal'),
  path('comprafinalizada/', comprafinalizada, name='comprafinalizada'),
  path('lista_libros', lista_libros, name='lista_libros'),
  path('ver_carrito', ver_carrito, name='ver_carrito'),
  path('eliminar_del_carrito/<int:id>', eliminar_del_carrito, name='eliminar_del_carrito'),
  path('agregar_al_carrito',agregar_al_carrito, name='agregar_al_carrito'),
  path('listar_empleado', listar_empleado, name='listar_empleado'),
  path('modifiempleado/<int:id>', modifiempleado, name='modifiempleado'),
  path('modificliempleado/<int:id>', modificliempleado, name='modificliempleado'),
  path('listar_personas', listar_personas, name='listar_personas'),
  path('eliminarpersona/<int:id>', eliminarpersona, name='eliminarpersona'),
  path('listar_materiales', listar_materiales, name='listar_materiales'),
  path('empleadoform', empleadoform, name='empleadoform'),
  path('tecnicoform', tecnicoform, name='tecnicoform'),
  path('materialesform', materialesform, name='materialesform'),
  path('listar_tecnico', listar_tecnico, name='listar_tecnico'),
  path('listar_serviciotec', listar_serviciotec, name='listar_serviciotec'),
  path('modifitecnico/<int:id>', modifitecnico, name='modifitecnico'),
  path('modificliente/<int:id>', modificliente, name='modificliente'),
  path('servicioform', servicioform, name='servicioform'),
  path('cotizacionesform', cotizacionesform, name='cotizacionesform'),
  path('clienteform', clienteform, name='clienteform'),
  path('listar_servicio', listar_servicio, name='listar_servicio'),
  path('listar_cotizaciones', listar_cotizaciones, name='listar_cotizaciones'),
  path('libros_api', libros_api, name='libros_api'),
  path('starken_api', starken_api, name='starken_api'),
  path('realizar_comprastarken/', realizar_comprastarken, name='realizar_comprastarken'),
 
 


]   

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)