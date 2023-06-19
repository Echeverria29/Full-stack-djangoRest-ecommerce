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
  path('crearclienteform/', crearclienteform, name='crearclienteform'),
  path('crearempleadoform/', crearempleadoform, name='crearempleadoform'),
  path('home/', home, name='home'),
  path('index/', index, name='index'),
  path('indexpypal/', indexpypal, name='indexpypal'),
  path('comprafinalizada/', comprafinalizada, name='comprafinalizada'),
  path('lista_libros', lista_libros, name='lista_libros'),
  path('ver_carrito', ver_carrito, name='ver_carrito'),
  path('eliminar_del_carrito/<int:id>', eliminar_del_carrito, name='eliminar_del_carrito'),
  path('agregar_al_carrito',agregar_al_carrito, name='agregar_al_carrito'),
  path('listar_personas', listar_personas, name='listar_personas'),
  path('eliminarpersona/<int:id>', eliminarpersona, name='eliminarpersona'),
  path('listar_materiales', listar_materiales, name='listar_materiales'),
  path('materialesform', materialesform, name='materialesform'),
  path('listar_serviciotec', listar_serviciotec, name='listar_serviciotec'),
  path('modificliente/<int:id>', modificliente, name='modificliente'),
  path('modifiempleado/<int:id>', modifiempleado, name='modifiempleado'),
  path('servicioform', servicioform, name='servicioform'),
  path('cotizacionesform', cotizacionesform, name='cotizacionesform'),
  path('listar_servicio', listar_servicio, name='listar_servicio'),
  path('listar_cotizaciones', listar_cotizaciones, name='listar_cotizaciones'),
  path('libros_api', libros_api, name='libros_api'),
  path('starken_api', starken_api, name='starken_api'),
  path('realizar_comprastarken/', realizar_comprastarken, name='realizar_comprastarken'),
 
 


]   

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)