from modules.cultura.repositories.cultura_repository import CulturaRepository
from modules.cultura.entities.cultura import Cultura
from modules.cultura.dtos.cultura_dto import CulturaCreateDTO, CulturaUpdateDTO
from sqlalchemy.exc import IntegrityError

class CulturaService:
    def __init__(self, repository: CulturaRepository):
        self.repository = repository

    async def create_cultura(self, dto: CulturaCreateDTO) -> Cultura:
        cultura = Cultura(nome=dto.nome, safra_id=dto.safra_id, propriedade_id=dto.propriedade_id)
        try:
            return await self.repository.create(cultura)
        except IntegrityError:
            raise ValueError("Erro ao cadastrar cultura.")

    async def get_all_culturas(self):
        return await self.repository.get_all()

    async def get_cultura_by_id(self, cultura_id: int):
        return await self.repository.get_by_id(cultura_id)

    async def update_cultura(self, cultura_id: int, dto: CulturaUpdateDTO):
        cultura = await self.repository.get_by_id(cultura_id)
        if not cultura:
            raise ValueError("Cultura não encontrada")
        cultura.nome = dto.nome
        cultura.safra_id = dto.safra_id
        cultura.propriedade_id = dto.propriedade_id
        return await self.repository.update(cultura)

    async def delete_cultura(self, cultura_id: int):
        cultura = await self.repository.get_by_id(cultura_id)
        if not cultura:
            raise ValueError("Cultura não encontrada")
        await self.repository.delete(cultura) 