from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# 🔐 Tokens y login
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

# ✅ Respuestas
class SuccessResponseScheme(BaseModel):
    msg: str

# 📧 Recuperación y cambio de contraseña
class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class PasswordResetSchema(BaseModel):
    password: str = Field(..., min_length=8)

class PasswordUpdateSchema(BaseModel):
    old_password: str = Field(..., min_length=8)
    password: str = Field(..., min_length=8)

# 👤 Usuario y correo
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        orm_mode = True

class MailBodySchema(BaseModel):
    type: str
    token: str

class MailTaskSchema(BaseModel):
    user: User
    body: MailBodySchema
