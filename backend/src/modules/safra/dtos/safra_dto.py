from pydantic import BaseModel
from typing import Optional, List

class CulturaReadDTO(BaseModel):
    id: int
    nome: str
    propriedade_id: int
    safra_id: int

    class Config:
        from_attributes = True  

class SafraBaseDTO(BaseModel):
    ano: int
    propriedade_id: int

class SafraCreateDTO(SafraBaseDTO):
    pass

class SafraUpdateDTO(SafraBaseDTO):
    pass

class SafraReadDTO(BaseModel):
    id: int
    ano: int
    propriedade_id: int
    culturas: Optional[List[CulturaReadDTO]] = None

    class Config:
        from_attributes = True  