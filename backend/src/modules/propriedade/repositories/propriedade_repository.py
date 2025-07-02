from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.propriedade.entities.propriedade import Propriedade
from typing import List, Optional

class PropriedadeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Propriedade]:
        result = await self.session.execute(select(Propriedade))
        return result.scalars().all()

    async def get_by_id(self, propriedade_id: int) -> Optional[Propriedade]:
        result = await self.session.execute(select(Propriedade).where(Propriedade.id == propriedade_id))
        return result.scalars().first()

    async def create(self, propriedade: Propriedade) -> Propriedade:
        self.session.add(propriedade)
        await self.session.commit()
        await self.session.refresh(propriedade)
        return propriedade

    async def update(self, propriedade: Propriedade) -> Propriedade:
        await self.session.commit()
        await self.session.refresh(propriedade)
        return propriedade

    async def delete(self, propriedade: Propriedade):
        await self.session.delete(propriedade)
        await self.session.commit() 