from sqlalchemy import Column, Integer, Float, String, Enum, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
import enum

class TipoDeLeche(str, enum.Enum):
    calostro = "calostro"
    transicional = "transicional"
    madura = "madura"

class AnalisisDeMuestra(Base):
    __tablename__ = "analisis"

    id_analisis = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_f_ingreso = Column(Integer, ForeignKey("formularios_ingreso.id_f_ingreso"), nullable=False)
    id_muestra = Column(Integer, ForeignKey("muestras.id_muestra"), nullable=False)

    ph = Column(Float, nullable=False)
    conductividad = Column(Float, nullable=False)
    temperatura = Column(Float, nullable=False)
    mensaje_temp = Column(String, nullable=False)
    tipo_de_leche = Column(Enum(TipoDeLeche), nullable=False)

    usuario = relationship("Usuario", back_populates="analisis")
    formulario = relationship("FormularioIngreso", back_populates="analisis")
    muestra = relationship("MuestraDeLeche", back_populates="analisis")