#DATABASE ACCESS

from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.core.auth import get_password_hash
from app.utils.password_validation import validate_password
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
