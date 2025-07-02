from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from shared.database.base import Base

class Propriedade(Base):
    __tablename__ = "propriedades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    area_total = Column(Float, nullable=False)
    area_agricultavel = Column(Float, nullable=False)
    area_vegetacao = Column(Float, nullable=False)
    produtor_id = Column(Integer, ForeignKey("produtores.id"), nullable=False)
    produtor = relationship("Produtor", back_populates="propriedades")
    safras = relationship("Safra", back_populates="propriedade")
    culturas = relationship("Cultura", back_populates="propriedade") 