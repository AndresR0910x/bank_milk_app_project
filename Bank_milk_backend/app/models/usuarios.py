# SQLAlchemy MODEL

from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    password_history = Column(String, nullable=True)  # Added this column

    formulario_ingreso = relationship("FormularioIngreso", back_populates="usuario", uselist=False)
    muestras = relationship("MuestraDeLeche", back_populates="usuario")
    analisis = relationship("AnalisisDeMuestra", back_populates="usuario")
