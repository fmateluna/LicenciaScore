 
from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from licencia_score.app.core.config import Base

class Licencias(Base):
    __tablename__ = "licencias"
    id = Column(Integer, primary_key=True, index=True)
    propensity_score_rn = Column(Float, default=0)
    propensity_score_rn2 = Column(Float, default=0)
    propensity_score_frecuencia_mensual = Column(Float, default=1.0)
    propensity_score_frecuencia_semanal = Column(Float, default=1.0)
    propensity_score_otorgados_mensual = Column(Float, default=1.0)
    propensity_score_otorgados_semanal = Column(Float, default=1.0)
    propensity_score_ml = Column(Float, default=0.0)
    propensity_score = Column(Float, default=0.0)

    additional_data = relationship("DatosAdicionales", back_populates="licencia")

class DatosAdicionales(Base):
    __tablename__ = "datos_adicionales"
    id = Column(Integer, primary_key=True, index=True)
    licencia_id = Column(Integer, ForeignKey("licencias.id"))
    nombre_campo = Column(String, index=True)
    valor = Column(String)

    licencia = relationship("Licencias", back_populates="additional_data")
