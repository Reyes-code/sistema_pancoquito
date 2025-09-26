from django import forms
from django.forms import inlineformset_factory
from django import forms
from django.contrib.auth.models import User
from .models import Pedido, DetallePedido, Cliente, Productos
from django.core.exceptions import ValidationError
import json



class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cliente_id','nombre','email','cedula']


    
class ProductoForm(forms.ModelForm):
    class  Meta:
         model = Productos
         fields = ['producto_nombre','precio','activo']   
    
    
class PedidoForm(forms.Form):
    fecha_entrega = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'fecha-entrega'
        })
    )
    
    horario_entrega = forms.ChoiceField(
        choices=[('', 'Seleccione horario...')] + Pedido.HORARIO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'horario-entrega'
        })
    )
    
    productos_json = forms.CharField(
        widget=forms.HiddenInput(attrs={'id': 'productos-json'}),
        required=False
    )

    # Eliminamos la validación manual de usuario
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
