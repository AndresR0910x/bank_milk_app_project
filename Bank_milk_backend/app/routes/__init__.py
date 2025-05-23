from .auth_route import router as auth_router
from .formulario_ingreso_route import router as formulario_ingreso_router
from .muestra_route import router as muestra_router
from .analisis_route import router as analisis_router

__all__ = [
    "auth_router",
    "formulario_ingreso_router",
    "muestra_router",
    "analisis_router"
]