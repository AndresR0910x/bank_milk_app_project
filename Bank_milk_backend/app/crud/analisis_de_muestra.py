from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models import MuestraDeLeche, FormularioIngreso, AnalisisDeMuestra
from app.schemas.analisis import AnalisisCreate

def generar_analisis(db: Session, analisis_data: AnalisisCreate, usuario_id: int):
    # Verificar que la muestra exista y pertenezca al usuario
    muestra = db.query(MuestraDeLeche).filter(
        MuestraDeLeche.id_muestra == analisis_data.id_muestra,  # Acceso como atributo
        MuestraDeLeche.id_usuario == usuario_id
    ).first()
    
    if not muestra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Muestra no encontrada o no pertenece al usuario"
        )

    # Verificar que el formulario exista y pertenezca al usuario
    formulario = db.query(FormularioIngreso).filter(
        FormularioIngreso.id_f_ingreso == analisis_data.id_f_ingreso,
        FormularioIngreso.id_usuario == usuario_id
    ).first()
    
    if not formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulario de ingreso no encontrado o no pertenece al usuario"
        )

    # Crear el análisis
    db_analisis = AnalisisDeMuestra(
        id_usuario=usuario_id,
        id_f_ingreso=analisis_data.id_f_ingreso,
        id_muestra=analisis_data.id_muestra,
        ph=analisis_data.ph,
        conductividad=analisis_data.conductividad,
        temperatura=analisis_data.temperatura,
        mensaje_temp=analisis_data.mensaje_temp,
        tipo_de_leche=analisis_data.tipo_de_leche
    )
    
    db.add(db_analisis)
    db.commit()
    db.refresh(db_analisis)
    return db_analisis

def ver_analisis(db: Session, usuario_id: int, muestra_id: Optional[int] = None):
    query = db.query(AnalisisDeMuestra).filter(
        AnalisisDeMuestra.id_usuario == usuario_id
    )
    
    if muestra_id:
        query = query.filter(AnalisisDeMuestra.id_muestra == muestra_id)
    
    analisis = query.all()
    
    if not analisis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron análisis para los criterios proporcionados"
        )
    
    return analisis