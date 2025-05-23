from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date
from typing import Optional
from app.models import FormularioIngreso
from app.schemas.formulario_ingreso import FormularioCreate


def crear_formulario(db: Session, formulario_data: FormularioCreate, usuario_id: int):
    # Verificar si el usuario ya tiene un formulario
    existing_form = db.query(FormularioIngreso).filter(
        FormularioIngreso.id_usuario == usuario_id
    ).first()
    
    if existing_form:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya tiene un formulario de ingreso registrado"
        )
    
    # Crear el formulario usando .dict() para convertir el modelo Pydantic a dict
    db_formulario = FormularioIngreso(
        id_usuario=usuario_id,
        **formulario_data.dict()  # Esta es la forma correcta de acceder a los datos
    )
    
    db.add(db_formulario)
    db.commit()
    db.refresh(db_formulario)
    return db_formulario

def actualizar_formulario(db: Session, formulario_id: int, update_data: dict, usuario_id: int):
    db_formulario = db.query(FormularioIngreso).filter(
        FormularioIngreso.id_f_ingreso == formulario_id,
        FormularioIngreso.id_usuario == usuario_id
    ).first()

    if not db_formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulario no encontrado o no pertenece al usuario"
        )
    
    for key, value in update_data.items():
        setattr(db_formulario, key, value)
    
    db.commit()
    db.refresh(db_formulario)
    return db_formulario

def eliminar_formulario(db: Session, formulario_id: int, usuario_id: int):
    db_formulario = db.query(FormularioIngreso).filter(
        FormularioIngreso.id_f_ingreso == formulario_id,
        FormularioIngreso.id_usuario == usuario_id
    ).first()
    
    if not db_formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulario no encontrado o no pertenece al usuario"
        )
    
    # Verificar si tiene muestras asociadas
    if db_formulario.muestras:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el formulario porque tiene muestras asociadas"
        )
    
    db.delete(db_formulario)
    db.commit()
    return {"message": "Formulario eliminado correctamente"}

def ver_formulario(db: Session, usuario_id: int):
    db_formulario = db.query(FormularioIngreso).filter(
        FormularioIngreso.id_usuario == usuario_id
    ).first()
    
    if not db_formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró formulario para este usuario"
        )
    
    return db_formulario