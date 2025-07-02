from pydantic import BaseModel

class CulturaBaseDTO(BaseModel):
    nome: str
    safra_id: int
    propriedade_id: int

class CulturaCreateDTO(CulturaBaseDTO):
    pass

class CulturaUpdateDTO(CulturaBaseDTO):
    pass

class CulturaReadDTO(BaseModel):
    id: int
    nome: str
    safra_id: int
    propriedade_id: int

    class Config:
        from_attributes = True
 