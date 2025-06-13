from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.formulario_ingreso import FormularioCreate, FormularioUpdate, FormularioOut
from app.crud.formulario_ingreso import (
    crear_formulario, 
    actualizar_formulario, 
    eliminar_formulario, 
    ver_formulario,
    get_formulario_by_user_id,
    get_all_formularios
)

# Router para endpoints PÚBLICOS (sin autenticación)
public_router = APIRouter(tags=["Formularios de Ingreso (Público)"])

# ================== RUTAS PÚBLICAS ================== #
@public_router.get("/", response_model=List[FormularioOut])
def obtener_todos_formularios(
    db: Session = Depends(get_db)
):
    formularios = get_all_formularios(db)
    if not formularios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron formularios de ingreso"
        )
    return formularios

@public_router.get("/{id_usuario}", response_model=FormularioOut)
def obtener_formulario_por_id_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    formulario = get_formulario_by_user_id(db, id_usuario)
    if not formulario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe un formulario de ingreso para este usuario"
        )
    return formulario

@public_router.post("/{id_usuario}", response_model=FormularioOut, status_code=status.HTTP_201_CREATED)
def crear_nuevo_formulario(
       id_usuario: int,
       formulario_data: FormularioCreate,
       db: Session = Depends(get_db)
   ):
       # Verificar si el usuario existe
       from app.crud.user import get_user_by_id
       usuario = get_user_by_id(db, id_usuario)
       if not usuario:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Usuario no encontrado"
           )

       # Usar el id_usuario de la ruta en lugar del cuerpo
       return crear_formulario(db, formulario_data, id_usuario)


@public_router.put("/{formulario_id}", response_model=FormularioOut)
def actualizar_formulario_usuario(
    formulario_id: int,
    id_usuario: int,
    formulario_data: FormularioUpdate,
    db: Session = Depends(get_db)
):
    # Verificar si el usuario existe
    from app.crud.user import get_user_by_id
    usuario = get_user_by_id(db, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return actualizar_formulario(db, formulario_id, formulario_data.dict(exclude_unset=True), id_usuario)

@public_router.delete("/{formulario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_formulario_usuario(
    formulario_id: int,
    id_usuario: int,
    db: Session = Depends(get_db)
):
    # Verificar si el usuario existe
    from app.crud.user import get_user_by_id
    usuario = get_user_by_id(db, id_usuario)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    eliminar_formulario(db, formulario_id, id_usuario)
    return None