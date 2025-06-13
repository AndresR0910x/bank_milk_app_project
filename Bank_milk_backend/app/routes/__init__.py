# app/routes/__init__.py
from .formulario_ingreso_route import public_router
from .auth_route import router as auth_router
from .muestra_route import router as muestra_router
from .analisis_route import router as analisis_router

__all__ = [
    'public_router',
    'auth_router',
    'muestra_router',
    'analisis_router'
]