from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#Formulario login
# Definimos un formulario personalizado para el login con email
class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico", max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    
    
# Formulario de registro personalizado
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")  # Añadimos el campo de email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Incluimos el email en los campos
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',  
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
