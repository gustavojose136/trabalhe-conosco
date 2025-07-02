from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from shared.database.base import Base

class Safra(Base):
    __tablename__ = "safras"
    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, nullable=False)
    propriedade_id = Column(Integer, ForeignKey("propriedades.id"), nullable=False)
    propriedade = relationship("Propriedade", back_populates="safras")
    culturas = relationship("Cultura", back_populates="safra") 