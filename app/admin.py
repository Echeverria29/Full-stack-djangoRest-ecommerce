from django.contrib import admin

from .models import *

class ClienteAdmin(admin.ModelAdmin):
    list_display = ['rut_cliente','nombre','apellido','correo', 'direccion','telefono','numero_tarjeta']
    search_fields = ['rut_cliente']
    list_per_page = 4

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['rut_empleado','nombre','apellido','correo', 'direccion','telefono','cargo','departamento']
    search_fields = ['rut_empleado']
    list_per_page = 4

class LibroAdmin(admin.ModelAdmin):
    list_display = ['id','nombre','autor','editorial', 'precio','stock','proveedor']
    search_fields = ['id']
    list_per_page = 4

class carritoAdmin(admin.ModelAdmin):
    list_display = ['libro','cantidad']
    search_fields = ['']
    list_per_page = 4

class materialesAdmin(admin.ModelAdmin):
    list_display = ['id']
    search_fields = ['id']
    list_per_page = 4

class tipoAdmin(admin.ModelAdmin):
    list_display = ['id','tipo']
    search_fields = ['id']
    list_per_page = 4


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Carrito, carritoAdmin)
admin.site.register(Materiales, materialesAdmin)
admin.site.register(TipoServicio, tipoAdmin)