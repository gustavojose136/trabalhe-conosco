from modules.propriedade.repositories.propriedade_repository import PropriedadeRepository
from modules.propriedade.entities.propriedade import Propriedade
from modules.propriedade.dtos.propriedade_dto import PropriedadeCreateDTO, PropriedadeUpdateDTO
from sqlalchemy.exc import IntegrityError

class PropriedadeService:
    def __init__(self, repository: PropriedadeRepository):
        self.repository = repository

    async def create_propriedade(self, dto: PropriedadeCreateDTO) -> Propriedade:
        if dto.area_agricultavel + dto.area_vegetacao > dto.area_total:
            raise ValueError("A soma das áreas agricultável e de vegetação não pode exceder a área total da fazenda.")
        propriedade = Propriedade(
            nome=dto.nome,
            cidade=dto.cidade,
            estado=dto.estado,
            area_total=dto.area_total,
            area_agricultavel=dto.area_agricultavel,
            area_vegetacao=dto.area_vegetacao,
            produtor_id=dto.produtor_id
        )
        try:
            return await self.repository.create(propriedade)
        except IntegrityError:
            raise ValueError("Erro ao cadastrar propriedade.")

    async def get_all_propriedades(self):
        return await self.repository.get_all()

    async def get_propriedade_by_id(self, propriedade_id: int):
        return await self.repository.get_by_id(propriedade_id)

    async def update_propriedade(self, propriedade_id: int, dto: PropriedadeUpdateDTO):
        propriedade = await self.repository.get_by_id(propriedade_id)
        if not propriedade:
            raise ValueError("Propriedade não encontrada")
        if dto.area_agricultavel + dto.area_vegetacao > dto.area_total:
            raise ValueError("A soma das áreas agricultável e de vegetação não pode exceder a área total da fazenda.")
        propriedade.nome = dto.nome
        propriedade.cidade = dto.cidade
        propriedade.estado = dto.estado
        propriedade.area_total = dto.area_total
        propriedade.area_agricultavel = dto.area_agricultavel
        propriedade.area_vegetacao = dto.area_vegetacao
        propriedade.produtor_id = dto.produtor_id
        return await self.repository.update(propriedade)

    async def delete_propriedade(self, propriedade_id: int):
        propriedade = await self.repository.get_by_id(propriedade_id)
        if not propriedade:
            raise ValueError("Propriedade não encontrada")
        await self.repository.delete(propriedade) 