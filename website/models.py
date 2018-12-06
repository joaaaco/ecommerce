from django.db import models
from django.contrib.auth.models import User

# MODELO DE DATOS DE TIENDA
class Store(models.Model):
    nombre = models.CharField('Nombre de Tienda',max_length=100)
    direccion = models.CharField(max_length=200)
    comuna = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=200)
    telefono = models.IntegerField()

    def __str__(self):
        return  self.nombre

# MODELOS DE DATOS, RELACION VENDEDOR-TIENDA (EXTENSIÓN DEL MODELO USER)
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tienda_vendedor = models.ForeignKey(Store, on_delete=models.CASCADE, blank=True, null=True)

#MODELO DE DATOS DE PRODUCTOS
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', default='products/none/no_image.png')
    categorias = (
    ('0','Mac'),
    ('1','iPhone'),
    ('2','iPad'),
    ('3','Watch'),
    ('4','Audio'),
    ('5','Accesorios'),
    )
    categoria = models.CharField('Categoría', max_length=40, choices=categorias)
    novedad = models.BooleanField('¿Producto Nuevo?', default=False)
    precio_normal = models.IntegerField('Precio Normal')
    oferta = models.BooleanField('¿Producto en oferta?', default=False)
    precio_oferta = models.IntegerField('Precio Oferta')
    stock = models.IntegerField(default=0)
    tienda = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return  self.nombre
# MODELO DE DATOS DEL REGISTRO DE VENTAS
class Venta(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_tienda = models.ForeignKey(Store, on_delete=models.CASCADE)
    id_vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad = models.IntegerField()
    monto = models.IntegerField()
    descripcion = models.TextField(blank=True)

class TiendaManager(models.Manager):
    def get_queryset(self, request):
        if request.user.is_superuser:
            query = Store.objects.all()
        else:
            tienda_emp = request.user.employee.tienda_vendedor_id
            query = Store.objects.filter(id=tienda_emp)
        return query

# FILTRO DE PRODUCTOS SEGÚN LA TIENDA ASIGNADA - ADMINISTRADOR VE TODO
class ProductoManager(models.Manager):
    def get_queryset(self, request):
        if request.user.is_superuser:
            query = Producto.objects.all()
        else:
            tienda_emp = request.user.employee.tienda_vendedor_id
            query = Producto.objects.filter(tienda_id=tienda_emp)
        return query

class VentaManager(models.Manager):
    def get_queryset(self, request):
        if request.user.is_superuser:
            query = Venta.objects.all()
        else:
            tienda_emp = request.user.employee.tienda_vendedor_id
            query = Venta.objects.filter(id_tienda=tienda_emp)
        return query
