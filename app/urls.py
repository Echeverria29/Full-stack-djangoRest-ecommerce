from operator import index
from unicodedata import name
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  
  path('index/', index, name='index'),
  path('registro/', registro, name='registro'),
  path('lista_libros', lista_libros, name='lista_libros'),
  path('ver_carrito', ver_carrito, name='ver_carrito'),
  path('eliminar_del_carrito/<int:id>', eliminar_del_carrito, name='eliminar_del_carrito'),
  path('agregar_al_carrito',agregar_al_carrito, name='agregar_al_carrito'),
  path('listar_cliente', listar_cliente, name='listar_cliente'),
  path('modificliente/<int:id>', modificliente, name='modificliente'),
  path('servicioform', servicioform, name='servicioform'),
  


]   

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)