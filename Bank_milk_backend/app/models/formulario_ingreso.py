from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class FormularioIngreso(Base):
    __tablename__ = "formularios_ingreso"

    id_f_ingreso = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), unique=True, nullable=False)

    nombre_mama = Column(String, nullable=False)
    nombre_bebe = Column(String, nullable=False)
    sexo_bebe = Column(String, nullable=False)
    edad_mama = Column(Integer, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    semanas_del_parto = Column(Integer, nullable=False)
    prematuro = Column(Boolean, nullable=False)
    numero_de_parto = Column(Integer, nullable=False)
    peso = Column(Integer, nullable=False)
    tamaño = Column(Integer, nullable=False)

    usuario = relationship("Usuario", back_populates="formulario_ingreso")
    muestras = relationship("MuestraDeLeche", back_populates="formulario")
    analisis = relationship("AnalisisDeMuestra", back_populates="formulario")
