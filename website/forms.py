from django import forms
from .models import Venta, Producto
from django.core.exceptions import ValidationError

class VentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ('descripcion','cantidad',)

    def __init__(self, pk, *args, **kwargs):
        self.pk = pk
        super(VentaForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cd = self.cleaned_data
        stock_disponible = Producto.objects.get(id=self.pk)

        cantidad = cd.get("cantidad")
        if cantidad <= 0:
            raise ValidationError('Ingresa una cantidad válida')
            return cd
        if cantidad > stock_disponible.stock:
            raise ValidationError('No hay suficientes productos para realizar la venta')
            return cd
