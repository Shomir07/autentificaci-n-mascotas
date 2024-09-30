from django.urls import path
from Core.Deteccion.views import camera_view, procesar_img
urlpatterns = [
    path('camera/', camera_view, name='camera_view'),
    path('procesar/',procesar_img , name='procesar_imagen'),
]