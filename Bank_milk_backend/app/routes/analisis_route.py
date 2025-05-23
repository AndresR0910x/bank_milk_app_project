from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.analisis import AnalisisCreate, AnalisisOut
from app.crud.analisis_de_muestra import generar_analisis, ver_analisis
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/analisis", tags=["Análisis de Muestras"])

@router.post("/", response_model=AnalisisOut, status_code=status.HTTP_201_CREATED)
def crear_nuevo_analisis(
    analisis_data: AnalisisCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return generar_analisis(db, analisis_data, current_user.id_usuario)

@router.get("/", response_model=List[AnalisisOut])
def obtener_analisis_usuario(
    muestra_id: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return ver_analisis(db, current_user.id_usuario, muestra_id)