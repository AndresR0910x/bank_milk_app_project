from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth_router,
    public_router,
    muestra_router,
    analisis_router
)
from app.database import Base, engine
from app.models import usuarios, formulario_ingreso, muestra, analisis

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestión de Banco de Leche Materna")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de autenticación
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Rutas de formularios (PÚBLICAS y PRIVADAS)
app.include_router(public_router, prefix="/formularios")


# Rutas de muestras y análisis
app.include_router(muestra_router, prefix="/muestras", tags=["Muestras de Leche"])
app.include_router(analisis_router, prefix="/analisis", tags=["Análisis de Muestras"])

# Health check
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}