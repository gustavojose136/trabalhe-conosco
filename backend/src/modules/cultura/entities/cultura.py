from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from shared.database.base import Base

class Cultura(Base):
    __tablename__ = "culturas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String, nullable=True)
    safra_id = Column(Integer, ForeignKey("safras.id"), nullable=False)
    propriedade_id = Column(Integer, ForeignKey("propriedades.id"), nullable=False)
    safra = relationship("Safra", back_populates="culturas")
    propriedade = relationship("Propriedade", back_populates="culturas") 