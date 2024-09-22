import os
import datetime
import random
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate as django_authenticate, login as auth_login
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError 
from .form.forms import loginform, CustomUserCreationForm

import requests

from django.contrib import messages

from django.contrib.auth import logout


from django.contrib.auth.decorators import login_required


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



class loginform(forms.Form):
    email = forms.EmailField(label="Correo Electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


def logout_view(request):
    logout(request)
    return redirect('login')



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Las contraseñas no coinciden.")
            
        if User.objects.filter(email=email).exists():
            self.add_error('email', "El correo electrónico ya está registrado.")

        
# Configuración de Firebase
def initialize_firebase():
    file_path = os.path.join(os.path.dirname(__file__), 'config', 'autentificacion-de-animales-firebase-adminsdk-5y36b-a96e9d2b32.json')
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No se encuentra el archivo de credenciales en la ruta: {file_path}")

    if not firebase_admin._apps:
        cred = credentials.Certificate(file_path)
        firebase_admin.initialize_app(cred)




# Configuración de Pyrebase
config = {
    'apiKey': "AIzaSyDODdAaKjeUDaLsfm-t-nFLBFFEPYjo44Y",
    'authDomain': "autentificacion-de-animales.firebaseapp.com",
    "databaseURL": "https://autentificacion-de-animales.firebaseio.com",
    'projectId': "autentificacion-de-animales",
    'storageBucket': "autentificacion-de-animales.appspot.com",
    'messagingSenderId': "135378187853",
    'appId': "1:135378187853:web:955a63790002c3fb4a4e04",
    'measurementId': "G-L13XR3G9LB"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        id_token = body.get('id_token')

        try:
            # Verificar el idToken usando Firebase Admin SDK
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email')

            # Verificar si el usuario ya existe en Django
            user, created = User.objects.get_or_create(username=uid, email=email)
            if created:
                user.set_unusable_password()
                user.save()

            # Autenticar al usuario en Django y crear sesión
            auth_login(request, user)

            return JsonResponse({'status': 'success', 'redirect_url': '/vistaPrinc/'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def login(request):
    form = loginform(request.POST or None)
    error_message = None

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                # Autenticación con Firebase
                firebase_user = auth.sign_in_with_email_and_password(email, password)
                print(f"Usuario autenticado en Firebase: {firebase_user}")

                # Autenticación con Django
                django_user = User.objects.filter(email=email).first()
                if django_user is None:
                    error_message = "Usuario no encontrado en Django"
                else:
                    django_user = django_authenticate(request, username=django_user.username, password=password)
                    if django_user is not None:
                        auth_login(request, django_user)
                        return redirect('vistaPrincipal')
                    else:
                        error_message = "Contraseña incorrecta en Django"
            except Exception as e:
                print(f"Error en Firebase o Django: {e}")
                error_message = "Verifica tus credenciales."

    return render(request, 'login.html', {'form': form, 'error_message': error_message})


def register(request):
    error_message = None

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            if User.objects.filter(email=email).exists():
                error_message = "El correo electrónico ya está registrado en Django."
            else:
                try:
                    # Registro en Firebase
                    firebase_user = auth.create_user_with_email_and_password(email, password)
                    print(f"Usuario registrado en Firebase: {firebase_user}")

                    # Registro en Django
                    django_user = form.save()
                    django_user = django_authenticate(request, username=django_user.username, password=password)
                    
                    if django_user is not None:
                        auth_login(request, django_user)
                        return redirect('login')
                except firebase_auth.EmailAlreadyExistsError:
                    error_message = "El correo electrónico ya está registrado en Firebase."
                except Exception as e:
                    error_message = f"Error de autenticación en Firebase: {e}"
        else:
            error_message = "Por favor, corrige los errores en el formulario."
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form, 'error_message': error_message})


def vistaPrinc(request):
    # Datos de las tarjetas
    cards = [
        {'title': 'MOD. DETECCIÓN DE ANIMALES', 'description': 'Descripción: ', 'image': 'picture/Car_1.jpeg'},
        {'title': 'MOD. CLASIFICACIÓN DE ANIMALES', 'description': 'Descripción: ', 'image': 'picture/Car_2.jpeg'},
        {'title': 'MOD. HISTORIAL DE ANIMALES', 'description': 'Descripción: ', 'image': 'picture/Car_3.jpeg'},
    ]
    
    # Arreglo de imágenes de perfil disponibles
    profile_images = [
        'icons/profiles_random/profile1.png',
        'icons/profiles_random/profile2.png',
        'icons/profiles_random/profile3.png',
        'icons/profiles_random/profile4.png',
        'icons/profiles_random/profile5.png',
    ]
    # Obtener el correo del usuario autenticado y su nombre
    if request.user.is_authenticated:
        user_email = request.user.email
        user_username = request.user.username  
    else:
        user_email = None
        user_username = None

    # Selección de una imagen de perfil aleatoria o uso de la existente en la sesión
    if 'profile_image' not in request.session:
        request.session['profile_image'] = random.choice(profile_images)

    selected_profile_image = request.session['profile_image']

    # Contexto para pasar al template
    context = {
        'cards': cards,
        'user_email': user_email,
        'user_username': user_username,
        'profile_image': selected_profile_image,  
    }
    
    return render(request, 'vista_user.html', context)

# FUNCION PARA MOSTRAR LA CAMARA DEL MODULO 1
def camera_view(request):
    return render(request, 'detector_vista.html')