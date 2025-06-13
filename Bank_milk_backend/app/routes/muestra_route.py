from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app.schemas.muestra import MuestraCreate, MuestraUpdate, MuestraOut, MuestraResumenPorFecha
from app.crud.muestra_de_leche import (
    crear_muestra,
    actualizar_muestra,
    ver_muestras_por_fecha,
    obtener_resumen_todas_muestras
)
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/muestras", tags=["Muestras de Leche"])

@router.post("/", response_model=MuestraOut, status_code=status.HTTP_201_CREATED)
def crear_nueva_muestra(
    muestra_data: MuestraCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crear_muestra(db, muestra_data, current_user.id_usuario)

@router.put("/{muestra_id}", response_model=MuestraOut)
def actualizar_muestra_usuario(
    muestra_id: int,
    muestra_data: MuestraUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return actualizar_muestra(db, muestra_id, muestra_data, current_user.id_usuario)

@router.get("/fecha/{fecha_consulta}", response_model=List[MuestraOut])
def obtener_muestras_por_fecha(
    fecha_consulta: date,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return ver_muestras_por_fecha(db, current_user.id_usuario, fecha_consulta)

@router.get("/resumen-todas-fechas/", response_model=List[MuestraResumenPorFecha])
def obtener_resumen_muestras(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return obtener_resumen_todas_muestras(db, current_user.id_usuario)