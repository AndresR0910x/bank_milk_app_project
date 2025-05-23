from pydantic import BaseModel
from datetime import date, time
from enum import Enum
from typing import Optional

class ColorMuestra(str, Enum):
    blanco = "blanco"
    amarillento = "amarillento"
    transparente = "transparente"

class UbicacionMuestra(str, Enum):
    refrigerador = "refrigerador"
    congelador = "congelador"
    banco_de_leche = "banco_de_leche"

class MuestraBase(BaseModel):
    id_f_ingreso: int
    nombre_muestra: str
    fecha_de_extraccion: date
    hora_de_extraccion: time
    volumen: float
    pecho: str
    color: ColorMuestra
    ubicacion: UbicacionMuestra
    observacion: Optional[str] = None
    foto_de_muestra: Optional[str] = None

class MuestraCreate(MuestraBase):
    pass

class MuestraUpdate(BaseModel):
    nombre_muestra: Optional[str] = None
    fecha_de_extraccion: Optional[date] = None
    hora_de_extraccion: Optional[time] = None
    volumen: Optional[float] = None
    pecho: Optional[str] = None
    color: Optional[ColorMuestra] = None
    ubicacion: Optional[UbicacionMuestra] = None
    observacion: Optional[str] = None
    foto_de_muestra: Optional[str] = None

class MuestraOut(MuestraBase):
    id_muestra: int
    id_usuario: int
    
    class Config:
        from_attributes = True