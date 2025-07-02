from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from shared.database.base import Base

class Produtor(Base):
    __tablename__ = "produtores"
    id = Column(Integer, primary_key=True, index=True)
    cpf_cnpj = Column(String(18), unique=True, nullable=False, index=True)
    nome = Column(String(100), nullable=False)
    propriedades = relationship("Propriedade", back_populates="produtor", lazy="selectin") 