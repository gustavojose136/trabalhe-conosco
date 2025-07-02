from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.cultura.entities.cultura import Cultura
from typing import List, Optional

class CulturaRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Cultura]:
        result = await self.session.execute(select(Cultura))
        return list(result.scalars().all())

    async def get_by_id(self, cultura_id: int) -> Optional[Cultura]:
        result = await self.session.execute(select(Cultura).where(Cultura.id == cultura_id))
        return result.scalars().first()

    async def create(self, cultura: Cultura) -> Cultura:
        self.session.add(cultura)
        await self.session.commit()
        await self.session.refresh(cultura)
        return cultura

    async def update(self, cultura: Cultura) -> Cultura:
        await self.session.commit()
        await self.session.refresh(cultura)
        return cultura

    async def delete(self, cultura: Cultura):
        await self.session.delete(cultura)
        await self.session.commit() 