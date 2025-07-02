from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.session import get_db
from modules.cultura.dtos.cultura_dto import CulturaCreateDTO, CulturaUpdateDTO, CulturaReadDTO
from modules.cultura.repositories.cultura_repository import CulturaRepository
from modules.cultura.services.cultura_service import CulturaService

router = APIRouter(prefix="/culturas", tags=["Culturas"])

@router.post("/", response_model=CulturaReadDTO, status_code=status.HTTP_201_CREATED)
async def create_cultura(dto: CulturaCreateDTO, db: AsyncSession = Depends(get_db)):
    service = CulturaService(CulturaRepository(db))
    try:
        cultura = await service.create_cultura(dto)
        return cultura
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[CulturaReadDTO])
async def list_culturas(db: AsyncSession = Depends(get_db)):
    service = CulturaService(CulturaRepository(db))
    return await service.get_all_culturas()

@router.get("/{cultura_id}", response_model=CulturaReadDTO)
async def get_cultura(cultura_id: int, db: AsyncSession = Depends(get_db)):
    service = CulturaService(CulturaRepository(db))
    cultura = await service.get_cultura_by_id(cultura_id)
    if not cultura:
        raise HTTPException(status_code=404, detail="Cultura não encontrada")
    return cultura

@router.put("/{cultura_id}", response_model=CulturaReadDTO)
async def update_cultura(cultura_id: int, dto: CulturaUpdateDTO, db: AsyncSession = Depends(get_db)):
    service = CulturaService(CulturaRepository(db))
    try:
        return await service.update_cultura(cultura_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{cultura_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cultura(cultura_id: int, db: AsyncSession = Depends(get_db)):
    service = CulturaService(CulturaRepository(db))
    try:
        await service.delete_cultura(cultura_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 