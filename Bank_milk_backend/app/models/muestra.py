from sqlalchemy import Column, Integer, String, Date, Time, Float, Enum, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
import enum

class ColorMuestra(str, enum.Enum):
    blanco = "blanco"
    amarillento = "amarillento"
    transparente = "transparente"

class UbicacionMuestra(str, enum.Enum):
    refrigerador = "refrigerador"
    congelador = "congelador"
    banco_de_leche = "banco_de_leche"

class MuestraDeLeche(Base):
    __tablename__ = "muestras"

    id_muestra = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_f_ingreso = Column(Integer, ForeignKey("formularios_ingreso.id_f_ingreso"), nullable=False)

    nombre_muestra = Column(String, nullable=False)
    fecha_de_extraccion = Column(Date, nullable=False)
    hora_de_extraccion = Column(Time, nullable=False)
    volumen = Column(Float, nullable=False)
    pecho = Column(String, nullable=False)
    color = Column(Enum(ColorMuestra), nullable=False)
    ubicacion = Column(Enum(UbicacionMuestra), nullable=False)
    observacion = Column(String, nullable=True)
    foto_de_muestra = Column(String, nullable=True)

    usuario = relationship("Usuario", back_populates="muestras")
    formulario = relationship("FormularioIngreso", back_populates="muestras")
    analisis = relationship("AnalisisDeMuestra", back_populates="muestra", uselist=False)
