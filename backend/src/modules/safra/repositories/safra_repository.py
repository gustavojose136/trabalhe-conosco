from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.safra.entities.safra import Safra
from typing import List, Optional

class SafraRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Safra]:
        result = await self.session.execute(select(Safra))
        return list(result.scalars().all())

    async def get_by_id(self, safra_id: int) -> Optional[Safra]:
        result = await self.session.execute(select(Safra).where(Safra.id == safra_id))
        return result.scalars().first()

    async def create(self, safra: Safra) -> Safra:
        self.session.add(safra)
        await self.session.commit()
        await self.session.refresh(safra)
        return safra

    async def update(self, safra: Safra) -> Safra:
        await self.session.commit()
        await self.session.refresh(safra)
        return safra

    async def delete(self, safra: Safra):
        await self.session.delete(safra)
        await self.session.commit() 