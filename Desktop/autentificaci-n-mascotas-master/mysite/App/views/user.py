from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login

def vistaPrinc(request):
    # Define los datos para las tarjetas
    cards = [
        {
            'title': 'Meeting your Colleagues',
            'description': '6 Video - 40 min',
            'icon': 'Business Trip',
        },
        {
            'title': 'Meeting your Colleagues',
            'description': '6 Video - 40 min',
            'icon': 'Business Trip',
        },
        {
            'title': 'Meeting your Colleagues',
            'description': '6 Video - 40 min',
            'icon': 'Business Trip',
        },
    ]
    
    # Define el contexto para pasar a la plantilla
    context = {
        'cards': cards,  # Pasa la lista de tarjetas al contexto
    }
    
    # Renderiza la plantilla 'vista_user.html' con el contexto definido
    return render(request, 'templates/vista_user.html', context)