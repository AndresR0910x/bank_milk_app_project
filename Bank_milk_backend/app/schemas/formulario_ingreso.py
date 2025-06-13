from pydantic import BaseModel
from datetime import date
from typing import Optional

class FormularioBase(BaseModel):
    # DATOS PERSONALES
    nombre_mama: str
    edad_mama: int

    # HISTORIAL CLÍNICO DE LA MADRE
    fecha_parto: date
    semanas_gestacion: int
    tipo_parto: str  # "natural" o "cesárea"
    numero_de_parto: str  # "1", "2", "3", "4", "5", "más de 5"
    condiciones_medicas: Optional[str] = None  # Ejemplo: "Diabetes tipo 1,Hipertensión,Otra:Especificar"
    uso_medicamentos: Optional[str] = None  # Campo de texto libre
    consumo_sustancias: Optional[str] = None  # Ejemplo: "Tabaco,Alcohol,Otra:Especificar"
    alergias: Optional[str] = None  # Campo de texto libre
    enfermedades_relevantes: Optional[str] = None  # Campo de texto libre

    # DATOS DEL BEBÉ
    nombre_bebe: str
    fecha_nacimiento: date
    peso: float  # En kg
    estatura: float  # En cm
    edad_gestacional_nacimiento: int  # En semanas
    sexo_bebe: str  # "Femenino" o "Masculino"
    tipo_alimentacion: str  # "Lactancia exclusiva" o "Lactancia mixta"
    condicion_medica_bebe: Optional[str] = None  # Campo de texto libre
    prematuro: bool

class FormularioCreate(FormularioBase):
    id_usuario: Optional[int] = None  # Hacerlo opcional

class FormularioUpdate(BaseModel):
    # DATOS PERSONALES
    nombre_mama: Optional[str] = None
    edad_mama: Optional[int] = None

    # HISTORIAL CLÍNICO DE LA MADRE
    fecha_parto: Optional[date] = None
    semanas_gestacion: Optional[int] = None
    tipo_parto: Optional[str] = None
    numero_de_parto: Optional[str] = None
    condiciones_medicas: Optional[str] = None
    uso_medicamentos: Optional[str] = None
    consumo_sustancias: Optional[str] = None
    alergias: Optional[str] = None
    enfermedades_relevantes: Optional[str] = None

    # DATOS DEL BEBÉ
    nombre_bebe: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    peso: Optional[float] = None
    estatura: Optional[float] = None
    edad_gestacional_nacimiento: Optional[int] = None
    sexo_bebe: Optional[str] = None
    tipo_alimentacion: Optional[str] = None
    condicion_medica_bebe: Optional[str] = None
    prematuro: Optional[bool] = None

class FormularioOut(FormularioBase):
    id_f_ingreso: int
    id_usuario: int
    
    class Config:
        from_attributes = True