from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Producto, Store, Venta, Employee
from .forms import VentaForm

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url =  reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

class LogoutView(RedirectView):
    pattern_name = 'panel-login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

@login_required(login_url='/')
def home(request):
    id_tienda = request.user.employee.tienda_vendedor_id
    tiendas = Store.objects.get(pk=id_tienda)
    productos = Producto.objects.all().order_by('-id')
    return render(request, 'home.html', {'productos': productos, 'tiendas': tiendas})

@login_required(login_url='/')
def chart(request, pk):
    tienda = request.user.employee.tienda_vendedor_id
    chart = Venta.objects.get(pk=pk)
    current_period = datetime.datetime.now() # Asigna fecha actual
    ventas_periodo_actual = Venta.objects.filter(id_vendedor=pk, fecha__year=current_period.year,fecha__month=current_period.month).order_by('-id')
    ventas_periodo_anterior = Venta.objects.filter(id_vendedor=pk, fecha__year=current_period.year,fecha__month=current_period.month - 1).order_by('-id')
    unidades_periodo_actual = ventas_periodo_actual.aggregate(Sum('cantidad'))['cantidad__sum'] or 0.00
    unidades_periodo_anterior = ventas_periodo_anterior.aggregate(Sum('cantidad'))['cantidad__sum'] or 0.00
    importe_periodo_actual = ventas_periodo_actual.aggregate(Sum('monto'))['monto__sum'] or 0.00
    importe_periodo_anterior = ventas_periodo_anterior.aggregate(Sum('monto'))['monto__sum'] or 0.00
    if unidades_periodo_anterior > 0:
        porcentaje_ventas_periodo = ( unidades_periodo_actual / unidades_periodo_anterior ) * 100
    else:
        porcentaje_ventas_periodo = 'No hay datos para el mes anterior'
    if importe_periodo_anterior > 0:
        porcentaje_importe_periodo = ( importe_periodo_actual / importe_periodo_anterior ) * 100
    else:
        porcentaje_importe_periodo = 'No hay datos para el mes anterior'
    usuario = Employee.objects.filter(tienda_vendedor=tienda, user_id=pk)
    user_list = Employee.objects.filter(tienda_vendedor=tienda)
    return render(request, 'chart.html',
    {'ventas_periodo_actual': ventas_periodo_actual,
    'ventas_periodo_anterior': ventas_periodo_anterior,
    'unidades_periodo_actual': unidades_periodo_actual,
    'unidades_periodo_anterior': unidades_periodo_anterior,
    'importe_periodo_actual': importe_periodo_actual,
    'importe_periodo_anterior': importe_periodo_anterior,
    'porcentaje_ventas_periodo': porcentaje_ventas_periodo,
    'porcentaje_importe_periodo': porcentaje_importe_periodo,
    'usuario': usuario,
    'user_list': user_list,
    })

@login_required(login_url='/')
def chart_admin(request):
    tienda = request.user.employee.tienda_vendedor_id
    current_period = datetime.datetime.now() # Asigna fecha actual
    ventas_periodo_actual = Venta.objects.filter(id_tienda=tienda, fecha__year=current_period.year,fecha__month=current_period.month).order_by('-id')
    ventas_periodo_anterior = Venta.objects.filter(id_tienda=tienda, fecha__year=current_period.year,fecha__month=current_period.month - 1).order_by('-id')
    unidades_periodo_actual = ventas_periodo_actual.aggregate(Sum('cantidad'))['cantidad__sum'] or 0.00
    unidades_periodo_anterior = ventas_periodo_anterior.aggregate(Sum('cantidad'))['cantidad__sum'] or 0.00
    importe_periodo_actual = ventas_periodo_actual.aggregate(Sum('monto'))['monto__sum'] or 0.00
    importe_periodo_anterior = ventas_periodo_anterior.aggregate(Sum('monto'))['monto__sum'] or 0.00
    if unidades_periodo_anterior > 0:
        porcentaje_ventas_periodo = ( unidades_periodo_actual / unidades_periodo_anterior ) * 100
    else:
        porcentaje_ventas_periodo = 'No hay datos para el mes anterior'
    if importe_periodo_anterior > 0:
        porcentaje_importe_periodo = ( importe_periodo_actual / importe_periodo_anterior ) * 100
    else:
        porcentaje_importe_periodo = 'No hay datos para el mes anterior'
    return render(request, 'chart_admin.html',
    {'ventas_periodo_actual': ventas_periodo_actual,
    'ventas_periodo_anterior': ventas_periodo_anterior,
    'unidades_periodo_actual': unidades_periodo_actual,
    'unidades_periodo_anterior': unidades_periodo_anterior,
    'importe_periodo_actual': importe_periodo_actual,
    'importe_periodo_anterior': importe_periodo_anterior,
    'porcentaje_ventas_periodo': porcentaje_ventas_periodo,
    'porcentaje_importe_periodo': porcentaje_importe_periodo,
    })

@login_required(login_url='/')
def product(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = VentaForm(pk=pk, data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.id_producto_id = producto.id
            post.id_tienda_id = request.user.employee.tienda_vendedor_id
            post.id_vendedor_id = request.user.id
            if producto.oferta == '0':
                cantidad = form.cleaned_data.get("cantidad") * producto.precio_normal
            else:
                cantidad = form.cleaned_data.get("cantidad") * producto.precio_oferta
            post.monto = cantidad
            post.fecha = timezone.now()
            stock = Producto.objects.get(pk=pk)
            stock_actualizado = stock.stock - form.cleaned_data.get("cantidad")
            Producto.objects.filter(pk=pk).update(stock=stock_actualizado)
            post.save()
            messages.info(request, 'La venta del producto se ha registrado correctamente.')
            return redirect('product', pk=pk)
    else:
        form = VentaForm(pk=pk)
    return render(request, 'product-detail.html', {'form': form, 'producto': producto})
