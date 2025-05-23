from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date, time
from app.models import FormularioIngreso, MuestraDeLeche
from app.schemas.muestra import MuestraCreate, MuestraUpdate

def crear_muestra(db: Session, muestra_data: MuestraCreate, usuario_id: int):
    # Verificar que el formulario de ingreso exista y pertenezca al usuario
    formulario = db.query(FormularioIngreso).filter(
        FormularioIngreso.id_f_ingreso == muestra_data.id_f_ingreso,  # Acceso como atributo
        FormularioIngreso.id_usuario == usuario_id
    ).first()
    
    if not formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulario de ingreso no encontrado o no pertenece al usuario"
        )
    
    # Crear la muestra usando .dict() para convertir el modelo Pydantic
    db_muestra = MuestraDeLeche(
        id_usuario=usuario_id,
        **muestra_data.model_dump()  # Forma correcta en Pydantic v2
    )
    
    db.add(db_muestra)
    db.commit()
    db.refresh(db_muestra)
    return db_muestra

def actualizar_muestra(db: Session, muestra_id: int, update_data: MuestraUpdate, usuario_id: int):
    db_muestra = db.query(MuestraDeLeche).filter(
        MuestraDeLeche.id_muestra == muestra_id,
        MuestraDeLeche.id_usuario == usuario_id
    ).first()
    
    if not db_muestra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Muestra no encontrada o no pertenece al usuario"
        )
    
    # Convertir el modelo Pydantic a dict excluyendo valores None
    update_dict = update_data.model_dump(exclude_unset=True)
    
    # Actualizar solo los campos proporcionados
    for key, value in update_dict.items():
        setattr(db_muestra, key, value)
    
    db.commit()
    db.refresh(db_muestra)
    return db_muestra

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date
from typing import List

def ver_muestras_por_fecha(db: Session, usuario_id: int, fecha_consulta: date):
    """
    Versión adaptada a tu estructura de tabla
    """
    try:
        muestras = db.query(MuestraDeLeche).filter(
            MuestraDeLeche.id_usuario == usuario_id,
            MuestraDeLeche.fecha_de_extraccion == fecha_consulta
        ).order_by(MuestraDeLeche.hora_de_extraccion.asc()).all()
        
        return muestras or []  # Devuelve lista vacía si no hay resultados
        
    except Exception as e:
        print(f"Error en consulta: {str(e)}")
        return []  # Devuelve lista vacía en caso de error