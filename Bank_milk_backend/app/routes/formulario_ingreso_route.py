from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app.schemas.formulario_ingreso import FormularioCreate, FormularioUpdate, FormularioOut
from app.crud.formulario_ingreso import (
    crear_formulario, 
    actualizar_formulario, 
    eliminar_formulario, 
    ver_formulario
)
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/formularios", tags=["Formularios de Ingreso"])

@router.post("/", response_model=FormularioOut, status_code=status.HTTP_201_CREATED)
def crear_nuevo_formulario(
    formulario_data: FormularioCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crear_formulario(db, formulario_data, current_user.id_usuario)

@router.get("/", response_model=FormularioOut)
def obtener_formulario_usuario(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return ver_formulario(db, current_user.id_usuario)

@router.put("/{formulario_id}", response_model=FormularioOut)
def actualizar_formulario_usuario(
    formulario_id: int,
    formulario_data: FormularioUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return actualizar_formulario(db, formulario_id, formulario_data, current_user.id_usuario)

@router.delete("/{formulario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_formulario_usuario(
    formulario_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    eliminar_formulario(db, formulario_id, current_user.id_usuario)
    return None