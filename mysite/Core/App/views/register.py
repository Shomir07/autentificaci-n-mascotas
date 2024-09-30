
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate as django_authenticate, login as auth_login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Core.App.form.forms import CustomUserCreationForm
from firebase_admin import credentials, auth as firebase_auth
import pyrebase


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


def register_view(request):
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