from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from modules.propriedade.entities.propriedade import Propriedade
from modules.cultura.entities.cultura import Cultura
from modules.produtor.entities.produtor import Produtor

class DashboardService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def total_fazendas(self) -> int:
        result = await self.session.execute(select(func.count(Propriedade.id)))
        return result.scalar()

    async def total_hectares(self) -> float:
        result = await self.session.execute(select(func.sum(Propriedade.area_total)))
        return result.scalar() or 0.0

    async def fazendas_por_estado(self):
        result = await self.session.execute(
            select(Propriedade.estado, func.count(Propriedade.id)).group_by(Propriedade.estado)
        )
        return [{"estado": row[0], "total": row[1]} for row in result.all()]

    async def fazendas_por_cultura(self):
        result = await self.session.execute(
            select(Cultura.nome, func.count(Cultura.id)).group_by(Cultura.nome)
        )
        return [{"cultura": row[0], "total": row[1]} for row in result.all()]

    async def uso_do_solo(self):
        result = await self.session.execute(
            select(
                func.sum(Propriedade.area_agricultavel),
                func.sum(Propriedade.area_vegetacao)
            )
        )
        row = result.first()
        return {
            "agricultavel": row[0] or 0.0,
            "vegetacao": row[1] or 0.0
        } 