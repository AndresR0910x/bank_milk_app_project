from pydantic import BaseModel
from enum import Enum
from typing import Optional

class TipoDeLeche(str, Enum):
    calostro = "calostro"
    transicional = "transicional"
    madura = "madura"

class AnalisisBase(BaseModel):
    id_f_ingreso: int
    id_muestra: int
    ph: float
    conductividad: float
    temperatura: float
    mensaje_temp: str
    tipo_de_leche: TipoDeLeche

class AnalisisCreate(AnalisisBase):
    pass

class AnalisisOut(AnalisisBase):
    id_analisis: int
    id_usuario: int
    
    class Config:
        from_attributes = True