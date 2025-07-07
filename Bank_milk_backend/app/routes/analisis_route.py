from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.analisis import AnalisisDeMuestra
from app.models.muestra import MuestraDeLeche
from app.schemas.analisis import AnalisisCreate, AnalisisOut
from app.schemas.muestra import MuestraOut
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

@router.get("/{id_analisis}", response_model=AnalisisOut)
def obtener_analisis_por_id(
    id_analisis: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    analisis = db.query(AnalisisDeMuestra).filter(
        AnalisisDeMuestra.id_analisis == id_analisis,
        AnalisisDeMuestra.id_usuario == current_user.id_usuario
    ).first()
    
    if not analisis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Análisis no encontrado o no pertenece al usuario"
        )
    
    return analisis

@router.get("/muestra/{id_muestra}", response_model=List[AnalisisOut])
def obtener_analisis_por_muestra(
    id_muestra: int,
    db: Session = Depends(get_db)
):
    analisis = db.query(AnalisisDeMuestra).filter(
        AnalisisDeMuestra.id_muestra == id_muestra
    ).all()
    
    if not analisis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron análisis para la muestra especificada"
        )
    
    return analisis

@router.get("/muestras/", response_model=List[MuestraOut])
def obtener_todas_las_muestras(
    db: Session = Depends(get_db)
):
    muestras = db.query(MuestraDeLeche).all()
    
    if not muestras:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron muestras en la base de datos"
        )
    
    return muestras

@router.get("/all/", response_model=List[AnalisisOut])
def obtener_todos_los_analisis(
    db: Session = Depends(get_db)
):
    analisis = db.query(AnalisisDeMuestra).all()
    
    if not analisis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron análisis en la base de datos"
        )
    
    return analisis