from django import forms
from django.contrib.auth.models import User, Group
from .models import Vehiculo, Tarea
import datetime


# ==========================
# FORMULARIO VEHÍCULOS
# ==========================

class VehiculoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

        # Campos bloqueados al modificar
        if self.instance and self.instance.pk:

            self.fields['placa'].disabled = True
            self.fields['modelo'].disabled = True
            self.fields['color'].disabled = True
            self.fields['fecha_ingreso'].disabled = True
            self.fields['imagen'].disabled = True

        # Resaltar errores
        if self.is_bound:
            self.full_clean()

            for campo in self.errors:
                css = self.fields[campo].widget.attrs.get('class', '')
                self.fields[campo].widget.attrs['class'] = f'{css} is-invalid'

    class Meta:
        model = Vehiculo
        fields = '__all__'

        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control'}),

            'marca': forms.TextInput(attrs={'class': 'form-control'}),

            'modelo': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': '1900',
                'max': str(datetime.date.today().year),
                'placeholder': 'Ej. 2026'
            }),

            'color': forms.TextInput(attrs={'class': 'form-control'}),

            'propietario': forms.TextInput(attrs={'class': 'form-control'}),

            'ID': forms.NumberInput(attrs={'class': 'form-control'}),

            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),

            'Correo': forms.EmailInput(attrs={'class': 'form-control'}),

            'diagnostico': forms.Textarea(attrs={'class': 'form-control','rows': 4}),

            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),

            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

#funciones de errores
    def clean_placa(self):

        if self.instance and self.instance.pk:
            return self.instance.placa

        placa = self.cleaned_data.get('placa')

        if len(placa) != 6:
            raise forms.ValidationError(
                "La placa debe tener exactamente 6 caracteres."
            )

        return placa.upper()

    def clean_modelo(self):

        if self.instance and self.instance.pk:
            return self.instance.modelo

        modelo = self.cleaned_data.get('modelo')
        anio_actual = datetime.date.today().year

        if modelo < 1900 or modelo > anio_actual:
            raise forms.ValidationError(
                f"El año debe estar entre 1900 y {anio_actual}."
            )

        return modelo

    def clean_color(self):

        if self.instance and self.instance.pk:
            return self.instance.color

        return self.cleaned_data.get('color')

    def clean_fecha_ingreso(self):

        if self.instance and self.instance.pk:
            return self.instance.fecha_ingreso

        return self.cleaned_data.get('fecha_ingreso')

    def clean_imagen(self):

        if self.instance and self.instance.pk:
            return self.instance.imagen

        return self.cleaned_data.get('imagen')

    def clean_ID(self):

        identificacion = self.cleaned_data.get('ID')

        if identificacion and identificacion <= 0:
            raise forms.ValidationError(
                "La identificación debe ser mayor que cero."
            )

        return identificacion


# ==========================
# FORMULARIO USUARIOS
# ==========================

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    grupo = forms.ModelChoiceField(queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            user.groups.add(self.cleaned_data['grupo'])

        return user



# ==========================
# FORMULARIO TAREAS
# ==========================

class TareaForm(forms.ModelForm):

    class Meta:
        model = Tarea

        fields = [
            'vehiculo',
            'descripcion',
            'estado'
        ]

        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'form-control'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
            
            
        }