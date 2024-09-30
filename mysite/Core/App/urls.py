
from django.urls import path
from Core.App.views import login_view, register_view, logout_view, camera_view, home_view


urlpatterns = [
    path('', login_view, name='login'),  # Página de inicio de sesión
    path('home/', home_view, name='home'),  # Página principal después del inicio de sesión
    path('register/', register_view, name='register'),  # Página de registro
    path('logout/', logout_view, name='logout'),
    path('camera/', camera_view, name='camera_view'),
]