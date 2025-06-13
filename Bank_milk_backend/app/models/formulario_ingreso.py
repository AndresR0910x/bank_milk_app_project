from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
import sqlalchemy as sa
from app.database import Base
from sqlalchemy.orm import relationship

class FormularioIngreso(Base):
    __tablename__ = "formularios_ingreso"

    id_f_ingreso = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), unique=True, nullable=False)

    # DATOS PERSONALES
    nombre_mama = Column(String, nullable=False)
    edad_mama = Column(Integer, nullable=False)

    # HISTORIAL CLÍNICO DE LA MADRE
    fecha_parto = Column(Date, nullable=False)
    semanas_gestacion = Column(Integer, nullable=False)
    tipo_parto = Column(String, nullable=False)  # "natural" o "cesárea"
    numero_de_parto = Column(String, nullable=False)  # "1", "2", "3", "4", "5", "más de 5"
    condiciones_medicas = Column(String, nullable=True)  # Ejemplo: "Diabetes tipo 1,Hipertensión,Otra:Especificar"
    uso_medicamentos = Column(String, nullable=True)  # Campo de texto libre
    consumo_sustancias = Column(String, nullable=True)  # Ejemplo: "Tabaco,Alcohol,Otra:Especificar"
    alergias = Column(String, nullable=True)  # Campo de texto libre
    enfermedades_relevantes = Column(String, nullable=True)  # Campo de texto libre

    # DATOS DEL BEBÉ
    nombre_bebe = Column(String, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    peso = Column(sa.Float, nullable=False)  # En kg
    estatura = Column(sa.Float, nullable=False)  # En cm
    edad_gestacional_nacimiento = Column(Integer, nullable=False)  # En semanas
    sexo_bebe = Column(String, nullable=False)  # "Femenino" o "Masculino"
    tipo_alimentacion = Column(String, nullable=False)  # "Lactancia exclusiva" o "Lactancia mixta"
    condicion_medica_bebe = Column(String, nullable=True)  # Campo de texto libre
    prematuro = Column(Boolean, nullable=False)

    # Relaciones
    usuario = relationship("Usuario", back_populates="formulario_ingreso")
    muestras = relationship("MuestraDeLeche", back_populates="formulario")
    analisis = relationship("AnalisisDeMuestra", back_populates="formulario")

    