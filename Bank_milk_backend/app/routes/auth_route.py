from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Cookie
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from app.utils.rate_limit import RateLimiter
from app.utils.email import send_reset_email
from app.crud.user import get_user_by_email, create_user
from app.schemas.user import UserCreate, UserOut, UserBasicInfo, TokenResponse
from app.schemas.auth import Token, SuccessResponseScheme
from app.database import get_db
from app.core.auth import verify_password, create_access_token, refresh_token_state,decode_token
from app.dependencies.auth import get_current_user, oauth2_scheme
from app.crud.user import get_user_by_email, update_user_password, eliminar_usuario, get_all_users
from app.core.auth import create_password_reset_token, verify_password_reset_token, get_password_hash, create_refresh_token

router = APIRouter()

blacklisted_tokens = set()
password_reset_limiter = RateLimiter(max_requests=3, window_seconds=3600)  # 3 requests per hour

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, email=user_create.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    user = create_user(db, user_create)
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {
        "user": {
            "id_usuario": user.id_usuario,
            "email": user.email,
            "full_name": user.full_name
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {
        "user": {
            "id_usuario": user.id_usuario,
            "email": user.email,
            "full_name": user.full_name
        },
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserOut)
def read_users_me(current_user = Depends(get_current_user)):
    return current_user


from pydantic import BaseModel

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/refresh")
def refresh(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token de refresco inválido")
    
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Email no encontrado en el token")
    
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    new_access_token = create_access_token(data={"sub": email})
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.get("/verify", response_model=SuccessResponseScheme)
def verify(token: str, db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Token inválido")

    email = payload.get("sub")
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Simula una "activación"
    user.is_active = True  # Asegúrate de tener este campo en el modelo
    db.commit()
    return {"msg": "Activado exitosamente"}

@router.post("/logout", response_model=SuccessResponseScheme)
def logout(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    blacklisted_tokens.add(token)  # Simulación
    return {"msg": "Sesión cerrada exitosamente"}


# Add these new models
class ForgotPassword(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

@router.post("/forgot-password")
async def forgot_password(email_data: ForgotPassword, db: Session = Depends(get_db)):
    # Check rate limit
    password_reset_limiter.check_rate_limit(email_data.email)
    
    user = get_user_by_email(db, email=email_data.email)
    if not user:
        # Return success even if user doesn't exist to prevent email enumeration
        return {"message": "If an account exists with this email, a reset link will be sent"}
    
    token = create_password_reset_token(email=email_data.email)
    await send_reset_email(email_data.email, token)
    
    return {"message": "If an account exists with this email, a reset link will be sent"}

@router.post("/password-reset")
def reset_password(reset_data: PasswordReset, db: Session = Depends(get_db)):
    email = verify_password_reset_token(reset_data.token)
    if not email:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )
    
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    hashed_password = get_password_hash(reset_data.new_password)
    update_user_password(db, user.id_usuario, hashed_password)
    return {"message": "Password updated successfully"}

@router.post("/password-update")
def update_password(
    current_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )
    
    hashed_password = get_password_hash(new_password)
    update_user_password(db, current_user.id_usuario, hashed_password)
    return {"message": "Password updated successfully"}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cuenta_usuario(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    eliminar_usuario(db, current_user.id_usuario)
    return None

#Ruta para ver todos los usuarios registrados 
@router.get("/todos", response_model=List[UserBasicInfo])
def obtener_todos_usuarios(db: Session = Depends(get_db)):
    """
    Obtiene todos los usuarios registrados
    (Actualmente accesible sin autenticación)
    """
    return get_all_users(db)