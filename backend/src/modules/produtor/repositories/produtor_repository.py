from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from modules.produtor.entities.produtor import Produtor
from typing import List, Optional
from sqlalchemy.orm import selectinload

class ProdutorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Produtor]:
        result = await self.session.execute(
            select(Produtor).options(selectinload(Produtor.propriedades))
        )
        return list(result.scalars().all())

    async def get_by_id(self, produtor_id: int) -> Optional[Produtor]:
        result = await self.session.execute(
            select(Produtor).options(selectinload(Produtor.propriedades)).where(Produtor.id == produtor_id)
        )
        return result.scalars().first()

    async def get_by_cpf_cnpj(self, cpf_cnpj: str) -> Optional[Produtor]:
        result = await self.session.execute(select(Produtor).where(Produtor.cpf_cnpj == cpf_cnpj))
        return result.scalars().first()

    async def create(self, produtor: Produtor) -> Produtor:
        self.session.add(produtor)
        await self.session.commit()
        await self.session.refresh(produtor)
        return produtor

    async def update(self, produtor: Produtor) -> Produtor:
        await self.session.commit()
        await self.session.refresh(produtor)
        return produtor

    async def delete(self, produtor: Produtor):
        await self.session.delete(produtor)
        await self.session.commit() 