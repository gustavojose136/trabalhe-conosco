from modules.produtor.repositories.produtor_repository import ProdutorRepository
from modules.produtor.entities.produtor import Produtor
from modules.produtor.dtos.produtor_dto import ProdutorCreateDTO, ProdutorUpdateDTO
from shared.utils.validators import validar_cpf, validar_cnpj
from sqlalchemy.exc import IntegrityError

class ProdutorService:
    def __init__(self, repository: ProdutorRepository):
        self.repository = repository

    async def create_produtor(self, dto: ProdutorCreateDTO) -> Produtor:
        if len(dto.cpf_cnpj) == 11:
            if not validar_cpf(dto.cpf_cnpj):
                raise ValueError("CPF inválido")
        elif len(dto.cpf_cnpj) == 14:
            if not validar_cnpj(dto.cpf_cnpj):
                raise ValueError("CNPJ inválido")
        else:
            raise ValueError("CPF ou CNPJ deve ter 11 ou 14 dígitos")
        produtor = Produtor(cpf_cnpj=dto.cpf_cnpj, nome=dto.nome)
        try:
            return await self.repository.create(produtor)
        except IntegrityError:
            raise ValueError("CPF/CNPJ já cadastrado")

    async def get_all_produtores(self):
        return await self.repository.get_all()

    async def get_produtor_by_id(self, produtor_id: int):
        return await self.repository.get_by_id(produtor_id)

    async def update_produtor(self, produtor_id: int, dto: ProdutorUpdateDTO):
        produtor = await self.repository.get_by_id(produtor_id)
        if not produtor:
            raise ValueError("Produtor não encontrado")
        produtor.nome = dto.nome
        # Não permitir alteração do CPF/CNPJ
        return await self.repository.update(produtor)

    async def delete_produtor(self, produtor_id: int):
        produtor = await self.repository.get_by_id(produtor_id)
        if not produtor:
            raise ValueError("Produtor não encontrado")
        await self.repository.delete(produtor) 