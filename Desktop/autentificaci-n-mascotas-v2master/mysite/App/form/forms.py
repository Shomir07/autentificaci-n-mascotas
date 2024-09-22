from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#Formulario login
# Definimos un formulario personalizado para el login en Django
class loginform(forms.Form):
    username = forms.CharField(label="Nombre de usuario",max_length= 150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    
#Formulario register   
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }