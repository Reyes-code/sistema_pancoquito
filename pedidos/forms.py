from django import forms
from .models import Cliente,Orden, Productos, Envio
from django.forms import inlineformset_factory



class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cliente_id','nombre','email','cedula']


class EnvioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = ['tipo', 'estado']

class OrdenForm(forms.Form):
    cliente_id = forms.IntegerField(label='ID del Cliente')
    productos = forms.ModelMultipleChoiceField(
        queryset=Productos.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    cantidad = forms.IntegerField(min_value=1, initial=1)
    
    # Campos para nuevo envío
    tipo_envio = forms.CharField(max_length=50)
    estado_envio = forms.CharField(max_length=50, initial='Pendiente')