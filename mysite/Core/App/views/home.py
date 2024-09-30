from django.shortcuts import render
import random

def home_view(request):
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
    
    return render(request, 'home.html', context)