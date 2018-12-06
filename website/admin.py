from django.contrib import admin

from .models import Producto, Store, TiendaManager, Venta, VentaManager, ProductoManager, Employee
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.site_header = "Anckor - Panel de Administración"
admin.site.site_title = "Anckor - Panel de Administración"
admin.site.index_title = "Bienvenido al Panel de Administración"

# PANEL DE ADIMISTRACIÓN DE TIENDAS
class TiendaAdmin(admin.ModelAdmin):
    list_display = ('nombre','direccion','comuna','ciudad','telefono')

    def get_queryset(self, request):
        queryset = TiendaManager.get_queryset(self, request)
        return queryset

# PANEL DE ADMINISTRACIÓN DE PRODUCTOS
class ProductoAdmin(admin.ModelAdmin):
   #add any other code here
   list_display = ('nombre','marca','novedad','precio_normal','precio_oferta','oferta','stock','tienda')
   #Using that queryset manager created before
   def get_queryset(self, request):
       queryset = ProductoManager.get_queryset(self, request)
       return queryset

class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Tienda Asignada'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)

class VentasAdmin(admin.ModelAdmin):
    model = Venta
    list_display = ('fecha','id_producto','cantidad','monto','id_vendedor','id_tienda')

    def get_queryset(self, request):
        queryset = VentaManager.get_queryset(self, request)
        return queryset

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Store, TiendaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Venta, VentasAdmin)
