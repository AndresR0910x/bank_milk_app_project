#DATABASE ACCESS

from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.core.auth import get_password_hash
from app.utils.password_validation import validate_password
from fastapi import HTTPException, status
import json

def get_user_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def create_user(db: Session, user_create):
    db_user = Usuario(
        email=user_create.email,
        hashed_password=get_password_hash(user_create.password),
        full_name=user_create.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, user_id: int, new_password: str, new_hashed_password: str):
    user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if user:
        # Validate password complexity
        validate_password(new_password)
        
        # Check password history
        password_history = json.loads(user.password_history or '[]')
        if new_hashed_password in password_history:
            raise HTTPException(
                status_code=400,
                detail="Cannot reuse any of your last 5 passwords"
            )
        
        # Update password and history
        password_history.append(user.hashed_password)
        password_history = password_history[-5:]  # Keep only last 5 passwords
        
        user.hashed_password = new_hashed_password
        user.password_history = json.dumps(password_history)
        
        db.commit()
        return user
    return None

def eliminar_usuario(db: Session, user_id: int):
    db_user = db.query(Usuario).filter(Usuario.id_usuario == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Usuario no encontrado"
        )
    
    # Verificar si tiene formularios, muestras o analisis asociados 
    if db_user.formulario_ingreso or db_user.muestras or db_user.analisis:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el usuario porque tiene datos asociados"
        )
    
    #Eliminar el usuario 
    db.delete(db_user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}

def get_all_users(db: Session):
    """Obtiene todos los usuarios con paginación"""
    return db.query(Usuario).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id_usuario == user_id).first()