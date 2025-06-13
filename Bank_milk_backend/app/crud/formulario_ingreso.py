from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Dict, Any, Optional
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

    # Crear el formulario directamente con los datos del esquema
    db_formulario = FormularioIngreso(
        id_usuario=usuario_id,
        **formulario_data.dict(exclude={"id_usuario"})  # Excluir id_usuario del esquema
    )

    db.add(db_formulario)
    db.commit()
    db.refresh(db_formulario)
    return db_formulario


def actualizar_formulario(db: Session, formulario_id: int, update_data: Dict[str, Any], usuario_id: int):
    db_formulario = db.query(FormularioIngreso).filter(
        FormularioIngreso.id_f_ingreso == formulario_id,
        FormularioIngreso.id_usuario == usuario_id
    ).first()

    if not db_formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulario no encontrado o no pertenece al usuario"
        )

    # Actualizar solo los campos enviados
    for key, value in update_data.items():
        if hasattr(db_formulario, key) and value is not None:  # Ignorar valores None
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


def get_formulario_by_user_id(db: Session, id_usuario: int) -> Optional[FormularioIngreso]:
    return db.query(FormularioIngreso).filter(FormularioIngreso.id_usuario == id_usuario).first()


def get_all_formularios(db: Session):
    return db.query(FormularioIngreso).all()