from pydantic import BaseModel, constr
from typing import Optional, List, Annotated

class PropriedadeReadDTO(BaseModel):
    id: int
    nome: str
    cidade: str
    estado: str
    area_total: float
    area_agricultavel: float
    area_vegetacao: float

    class Config:
        from_attributes = True

class ProdutorBaseDTO(BaseModel):
    cpf_cnpj: Annotated[str, constr(strip_whitespace=True, min_length=11, max_length=18)]
    nome: str

class ProdutorCreateDTO(ProdutorBaseDTO):
    pass

class ProdutorUpdateDTO(ProdutorBaseDTO):
    pass

class ProdutorReadDTO(BaseModel):
    id: int
    cpf_cnpj: str
    nome: str
    propriedades: Optional[List[PropriedadeReadDTO]] = None

    class Config:
        from_attributes = True 