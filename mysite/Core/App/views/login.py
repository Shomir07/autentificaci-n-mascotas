from django.shortcuts import render, redirect
from django.contrib.auth import authenticate as django_authenticate, login as auth_login
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pyrebase

from Core.App.form.forms import LoginForm

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


def login_view(request):
    form = LoginForm(request.POST or None)
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
                        return redirect('home')
                    else:
                        error_message = "Contraseña incorrecta en Django"
            except Exception as e:
                print(f"Error en Firebase o Django: {e}")
                error_message = "Verifica tus credenciales."

    return render(request, 'login.html', {'form': form, 'error_message': error_message})
