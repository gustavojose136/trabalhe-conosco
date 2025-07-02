from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.session import get_db
from modules.dashboard.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Retorna estatísticas do dashboard"""
    service = DashboardService(db)
    return {
        "total_produtores": await service.total_produtores(),
        "total_propriedades": await service.total_propriedades(),
        "total_culturas": await service.total_culturas(),
        "total_safras": await service.total_safras(),
        "area_total_agricultavel": await service.area_total_agricultavel(),
        "area_total_vegetacao": await service.area_total_vegetacao()
    }

@router.get("/totais")
async def get_totais(db: AsyncSession = Depends(get_db)):
    service = DashboardService(db)
    return {
        "total_fazendas": await service.total_fazendas(),
        "total_hectares": await service.total_hectares(),
    }

@router.get("/por-estado")
async def get_por_estado(db: AsyncSession = Depends(get_db)):
    service = DashboardService(db)
    return await service.fazendas_por_estado()

@router.get("/por-cultura")
async def get_por_cultura(db: AsyncSession = Depends(get_db)):
    service = DashboardService(db)
    return await service.fazendas_por_cultura()

@router.get("/uso-do-solo")
async def get_uso_do_solo(db: AsyncSession = Depends(get_db)):
    service = DashboardService(db)
    return await service.uso_do_solo() 