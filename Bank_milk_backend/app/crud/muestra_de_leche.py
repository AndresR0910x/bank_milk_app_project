from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date, time
from app.models import FormularioIngreso, MuestraDeLeche
from app.schemas.muestra import MuestraCreate, MuestraUpdate

def crear_muestra(db: Session, muestra_data: MuestraCreate, usuario_id: int):
    # Verificar formulario
    formulario = db.query(FormularioIngreso).filter(
        FormularioIngreso.id_f_ingreso == muestra_data.id_f_ingreso,
        FormularioIngreso.id_usuario == usuario_id
    ).first()
    
    if not formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formulario de ingreso no encontrado o no pertenece al usuario"
        )
    
    # Convertir el modelo Pydantic a dict y manejar el tipo de recipiente
    data_dict = muestra_data.model_dump()
    
    db_muestra = MuestraDeLeche(
        id_usuario=usuario_id,
        **data_dict
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
    
    update_dict = update_data.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        setattr(db_muestra, key, value)
    
    db.commit()
    db.refresh(db_muestra)
    return db_muestra

def ver_muestras_por_fecha(db: Session, usuario_id: int, fecha_consulta: date):
    try:
        muestras = db.query(MuestraDeLeche).filter(
            MuestraDeLeche.id_usuario == usuario_id,
            MuestraDeLeche.fecha_de_extraccion == fecha_consulta
        ).order_by(MuestraDeLeche.hora_de_extraccion.asc()).all()
        
        return muestras or []
    except Exception as e:
        print(f"Error en consulta: {str(e)}")
        return []

def obtener_resumen_todas_muestras(db: Session, usuario_id: int):
    try:
        resumen = (
            db.query(
                MuestraDeLeche.fecha_de_extraccion.label("fecha"),
                func.count(MuestraDeLeche.id_muestra).label("cantidad")
            )
            .filter(MuestraDeLeche.id_usuario == usuario_id)
            .group_by(MuestraDeLeche.fecha_de_extraccion)
            .order_by(MuestraDeLeche.fecha_de_extraccion.asc())
            .all()
        )
        return [
            {"fecha": row.fecha, "cantidad": row.cantidad}
            for row in resumen
        ] or []
    except Exception as e:
        print(f"Error en consulta de resumen: {str(e)}")
        return []