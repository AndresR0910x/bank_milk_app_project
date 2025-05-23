from pydantic import BaseModel
from datetime import date
from typing import Optional

class FormularioBase(BaseModel):
    nombre_mama: str
    nombre_bebe: str
    sexo_bebe: str
    edad_mama: int
    fecha_nacimiento: date
    semanas_del_parto: int
    prematuro: bool
    numero_de_parto: int
    peso: int
    tamaño: int

class FormularioCreate(FormularioBase):
    pass

class FormularioUpdate(BaseModel):
    nombre_mama: Optional[str] = None
    nombre_bebe: Optional[str] = None
    sexo_bebe: Optional[str] = None
    edad_mama: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    semanas_del_parto: Optional[int] = None
    prematuro: Optional[bool] = None
    numero_de_parto: Optional[int] = None
    peso: Optional[int] = None
    tamaño: Optional[int] = None

class FormularioOut(FormularioBase):
    id_f_ingreso: int
    id_usuario: int
    
    class Config:
        from_attributes = True