from sqlalchemy import Column, Integer, String, Date, Time, Float, Enum, ForeignKey, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
import enum

class ColorMuestra(str, enum.Enum):
    blanco = "blanco"
    amarillento = "amarillento"
    transparente = "transparente"
    verde = "verde"
    rosada_roja = "rosada_roja"

class UbicacionMuestra(str, enum.Enum):
    refrigerador = "refrigerador"
    congelador = "congelador"
    banco_de_leche = "banco_de_leche"

class OlorMuestra(str, enum.Enum):
    dulce = "dulce"
    neutro = "neutro"
    agrio = "agrio"
    rancio = "rancio"
    quimico_metalico = "quimico_metalico"

class PresenciaSuciedades(str, enum.Enum):
    si = "si"
    no = "no"

class TipoRecipiente(str, enum.Enum):
    vidrio = "vidrio"
    plastico = "plastico"
    bolsa = "bolsa"

    @classmethod
    def get_db_value(cls, value):
        if value == "plastico":
            return "plastico"
        return value

class MetodoExtraccion(str, enum.Enum):
    manual = "manual"
    electrico = "electrico"
    mixto = "mixto"

class Pecho(str, enum.Enum):
    derecho = "derecho"
    izquierdo = "izquierdo"
    ambos = "ambos"

class RespuestaSiNo(str, enum.Enum):
    si = "si"
    no = "no"

class EstadoMuestra(str, enum.Enum):  # Nuevo enum para estado
    sin_analisis = "sin_analisis"
    analizado = "analizado"

class MuestraDeLeche(Base):
    __tablename__ = "muestras"

    id_muestra = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_f_ingreso = Column(Integer, ForeignKey("formularios_ingreso.id_f_ingreso"), nullable=False)

    nombre_muestra = Column(String, nullable=False)
    fecha_de_extraccion = Column(Date, nullable=False)
    hora_de_extraccion = Column(Time, nullable=False)
    volumen = Column(Float, nullable=False)
    pecho = Column(Enum(Pecho), nullable=False)
    color = Column(Enum(ColorMuestra), nullable=False)
    ubicacion = Column(Enum(UbicacionMuestra), nullable=False)
    olor = Column(Enum(OlorMuestra), nullable=False)
    presencia_de_suciedades = Column(Enum(PresenciaSuciedades), nullable=False)
    tipo_de_recipiente = Column(Enum(TipoRecipiente), nullable=False)
    observacion = Column(String, nullable=True)
    foto_de_muestra = Column(String, nullable=True)
    metodo_extraccion = Column(Enum(MetodoExtraccion), nullable=False)
    medicamentos_hoy = Column(Enum(RespuestaSiNo), nullable=False)
    condicion_salud_hoy = Column(Enum(RespuestaSiNo), nullable=False)
    estado = Column(Enum(EstadoMuestra), nullable=False, default="sin_analisis")  # Nuevo campo

    usuario = relationship("Usuario", back_populates="muestras")
    formulario = relationship("FormularioIngreso", back_populates="muestras")
    analisis = relationship("AnalisisDeMuestra", back_populates="muestra", uselist=False)