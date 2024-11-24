from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Verificacion
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget = forms.TextInput(attrs={'class':'form-control', 'autocomplete':'off'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control'})


class VerificacionForm(forms.ModelForm):
    class Meta:
        model = Verificacion
        fields = ['nombre_completo', 'email', 'telefono', 'programa_academico', 'contrasena', 'rfid']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'placeholder': 'Nombre completo', 'class':'form-control', 'autocomplete':'off'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'class':'form-control', 'autocomplete':'off'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono', 'maxlength': '10', 'class':'form-control', 'autocomplete':'off'}),
            'programa_academico': forms.TextInput(attrs={'placeholder': 'programa academico', 'class':'form-control', 'autocomplete':'off'}),
            'contrasena': forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class':'form-control',}),
            'rfid': forms.TextInput(attrs={'placeholder': 'RFID', 'maxlength': '10', 'class':'form-control', 'autocomplete':'off'}),
        }

    def clean_contrasena(self):
        contrasena = self.cleaned_data.get('contrasena')
        # Verificar que la contraseña solo contenga números
        if not contrasena.isdigit():
            raise ValidationError("La contraseña debe contener solo números.")
        return contrasena

class VerificacionClave(forms.Form):
    clave = forms.CharField(max_length=10, required=True)
    clave.widget.attrs.update({'class':'form-control', 'autocomplete':'off', 'placeholder':'Ingrese su clave'})
    
    
class VerificacionProfesorForm(forms.ModelForm):
    class Meta:
        model = Verificacion
        fields = ['nombre_completo', 'email', 'telefono', 'programa_academico', 'lab_vision', 'lab_robotica', 'salon_210']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'placeholder': 'Nombre completo', 'class':'form-control', 'autocomplete':'off', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'class':'form-control', 'autocomplete':'off', 'readonly': 'readonly'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono', 'maxlength': '10', 'class':'form-control', 'autocomplete':'off', 'readonly': 'readonly'}),
            'programa_academico': forms.TextInput(attrs={'placeholder': 'programa academico', 'class':'form-control', 'autocomplete':'off', 'readonly': 'readonly'}),
            'lab_vision': forms.CheckboxInput(),
            'lab_robotica': forms.CheckboxInput(),
            'salon_210': forms.CheckboxInput(),
        }
