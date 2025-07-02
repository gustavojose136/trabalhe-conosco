from modules.safra.repositories.safra_repository import SafraRepository
from modules.safra.entities.safra import Safra
from modules.safra.dtos.safra_dto import SafraCreateDTO, SafraUpdateDTO
from sqlalchemy.exc import IntegrityError

class SafraService:
    def __init__(self, repository: SafraRepository):
        self.repository = repository

    async def create_safra(self, dto: SafraCreateDTO) -> Safra:
        safra = Safra(ano=dto.ano, propriedade_id=dto.propriedade_id)
        try:
            return await self.repository.create(safra)
        except IntegrityError:
            raise ValueError("Erro ao cadastrar safra.")

    async def get_all_safras(self):
        return await self.repository.get_all()

    async def get_safra_by_id(self, safra_id: int):
        return await self.repository.get_by_id(safra_id)

    async def update_safra(self, safra_id: int, dto: SafraUpdateDTO):
        safra = await self.repository.get_by_id(safra_id)
        if not safra:
            raise ValueError("Safra não encontrada")
        safra.ano = dto.ano
        safra.propriedade_id = dto.propriedade_id
        return await self.repository.update(safra)

    async def delete_safra(self, safra_id: int):
        safra = await self.repository.get_by_id(safra_id)
        if not safra:
            raise ValueError("Safra não encontrada")
        await self.repository.delete(safra) 