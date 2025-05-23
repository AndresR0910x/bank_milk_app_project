from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id_usuario: int
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

class PasswordReset(BaseModel):
    token: str
    new_password: str

class ForgotPassword(BaseModel):
    email: EmailStr

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

class UserListOut(BaseModel):
    id_usuario: int
    email: str
    full_name: str
    
    class Config:
        from_attributes = True


class UserBasicInfo(BaseModel):
    id_usuario: int
    email: str
    full_name: str
    
    class Config:
        from_attributes = True