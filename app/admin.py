from django.contrib import admin

from .models import *

class ClienteAdmin(admin.ModelAdmin):
    list_display = ['rut_cliente','nombre','apellido','correo', 'direccion','telefono','numero_tarjeta']
    search_fields = ['rut_cliente']
    list_per_page = 4

class LibroAdmin(admin.ModelAdmin):
    list_display = ['id_libro','nombre','autor','editorial', 'precio','stock','proveedor']
    search_fields = ['id_libro']
    list_per_page = 4

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Libro, LibroAdmin)