from pydantic import BaseModel, field_validator
from datetime import date, time
from enum import Enum
from typing import Optional

class ColorMuestra(str, Enum):
    blanco = "blanco"
    amarillento = "amarillento"
    transparente = "transparente"
    verde = "verde"
    rosada_roja = "rosada_roja"

class UbicacionMuestra(str, Enum):
    refrigerador = "refrigerador"
    congelador = "congelador"
    banco_de_leche = "banco_de_leche"

class OlorMuestra(str, Enum):
    dulce = "dulce"
    neutro = "neutro"
    agrio = "agrio"
    rancio = "rancio"
    quimico_metalico = "quimico_metalico"

class PresenciaSuciedades(str, Enum):
    si = "si"
    no = "no"

class TipoRecipiente(str, Enum):
    vidrio = "vidrio"
    plastico = "plastico"
    bolsa = "bolsa"

    @classmethod
    def validate(cls, v):
        if v == "plasticosinbpa":
            return "plastico"
        return v

class MetodoExtraccion(str, Enum):
    manual = "manual"
    electrico = "electrico"
    mixto = "mixto"

class Pecho(str, Enum):
    derecho = "derecho"
    izquierdo = "izquierdo"
    ambos = "ambos"

class RespuestaSiNo(str, Enum):
    si = "si"
    no = "no"

class EstadoMuestra(str, Enum):  # Nuevo enum para estado
    sin_analisis = "sin_analisis"
    analizado = "analizado"

class MuestraBase(BaseModel):
    id_f_ingreso: int
    nombre_muestra: str
    fecha_de_extraccion: date
    hora_de_extraccion: time
    volumen: float
    pecho: Pecho
    color: ColorMuestra
    ubicacion: UbicacionMuestra
    olor: OlorMuestra
    presencia_de_suciedades: PresenciaSuciedades
    tipo_de_recipiente: TipoRecipiente
    observacion: Optional[str] = None
    foto_de_muestra: Optional[str] = None
    metodo_extraccion: MetodoExtraccion
    medicamentos_hoy: RespuestaSiNo
    condicion_salud_hoy: RespuestaSiNo
    estado: EstadoMuestra = EstadoMuestra.sin_analisis  # Nuevo campo con valor por defecto

    @field_validator('tipo_de_recipiente', mode='before')
    def validate_tipo_recipiente(cls, v):
        if isinstance(v, str) and v == "plastico_sin_bpa":
            return "plastico"
        return v

class MuestraCreate(MuestraBase):
    pass

class MuestraUpdate(BaseModel):
    nombre_muestra: Optional[str] = None
    fecha_de_extraccion: Optional[date] = None
    hora_de_extraccion: Optional[time] = None
    volumen: Optional[float] = None
    pecho: Optional[Pecho] = None
    color: Optional[ColorMuestra] = None
    ubicacion: Optional[UbicacionMuestra] = None
    olor: Optional[OlorMuestra] = None
    presencia_de_suciedades: Optional[PresenciaSuciedades] = None
    tipo_de_recipiente: Optional[TipoRecipiente] = None
    observacion: Optional[str] = None
    foto_de_muestra: Optional[str] = None
    metodo_extraccion: Optional[MetodoExtraccion] = None
    medicamentos_hoy: Optional[RespuestaSiNo] = None
    condicion_salud_hoy: Optional[RespuestaSiNo] = None
    estado: Optional[EstadoMuestra] = None  # Permitir actualización opcional

class MuestraOut(MuestraBase):
    id_muestra: int
    id_usuario: int

    class Config:
        from_attributes = True

class MuestraResumenPorFecha(BaseModel):
    fecha: date
    cantidad: int

    class Config:
        from_attributes = True