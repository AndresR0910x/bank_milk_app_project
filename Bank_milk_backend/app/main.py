from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analisis_route, auth_route, formulario_ingreso_route, muestra_route
from app.database import Base, engine
from app.models import usuarios, formulario_ingreso, muestra, analisis

# Drop all tables and recreate them (solo para desarrollo)
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Gestión de Banco de Leche Materna")

# Middleware CORS para permitir peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplaza con tus dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de autenticación
app.include_router(auth_route.router, prefix="/auth", tags=["Auth"])

# Rutas de formularios de ingreso
app.include_router(formulario_ingreso_route.router, prefix="/formularios", tags=["Formularios de Ingreso"])

# Rutas de muestras de leche
app.include_router(muestra_route.router, prefix="/muestras", tags=["Muestras de Leche"])

# Rutas de análisis
app.include_router(analisis_route.router, prefix="/analisis", tags=["Análisis de Muestras"])

# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}