from pydantic import BaseModel, condecimal
from typing import Optional

class ProdutorReadDTO(BaseModel):
    id: int
    cpf_cnpj: str
    nome: str
    class Config:
        from_attributes = True

class PropriedadeBaseDTO(BaseModel):
    nome: str
    cidade: str
    estado: str
    area_total: float
    area_agricultavel: float
    area_vegetacao: float
    produtor_id: int

class PropriedadeCreateDTO(PropriedadeBaseDTO):
    pass

class PropriedadeUpdateDTO(PropriedadeBaseDTO):
    pass

class PropriedadeReadDTO(BaseModel):
    id: int
    nome: str
    cidade: str
    estado: str
    area_total: float
    area_agricultavel: float
    area_vegetacao: float
    produtor: Optional[ProdutorReadDTO]

    class Config:
        from_attributes = True 
 