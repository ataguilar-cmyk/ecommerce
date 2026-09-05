from django import forms
from .models import PaqueteTuristico
from django.core.exceptions import ValidationError

class PaqueteTuristicoModelForm(forms.ModelForm):
    class Meta:
        model = PaqueteTuristico
        fields = ['nombre', 'destino', 'precio', 'categoria', 'disponible', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

    # Sanitización y validación individual de campo (clean_<campo>)
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if len(nombre) < 3:
            raise ValidationError("El nombre es demasiado corto (mínimo 3 caracteres).")
        # Sanitización: elimina espacios vacíos basura y aplica formato título
        return nombre.strip().title()

    def clean_destino(self):
        destino = self.cleaned_data.get('destino')
        if len(destino) < 3:
            raise ValidationError("El destino es demasiado corto (mínimo 3 caracteres).")
        return destino.strip().title()

    # Validación global multicampo del formulario (clean)
    def clean(self):
        cleaned_data = super().clean()
        categoria = cleaned_data.get('categoria')
        precio = cleaned_data.get('precio')

        # Regla de negocio cruzada entre dos campos
        if categoria == 'AVENTURA' and precio and precio < 1000:
            raise ValidationError("Un paquete de aventura no puede costar menos de $1,000 MXN.")
        return cleaned_data