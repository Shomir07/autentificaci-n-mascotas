from .login import login_view
from .register import register_view
from .home import home_view
from .logout import logout_view
from ...Deteccion.views.camera import camera_view

__all__ = [
    'login_view',
    'register_view',
    'home_view',
    'logout_view',
    'camera_view',
]