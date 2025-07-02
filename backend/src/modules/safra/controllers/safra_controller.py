from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.session import get_db
from modules.safra.dtos.safra_dto import SafraCreateDTO, SafraUpdateDTO, SafraReadDTO
from modules.safra.repositories.safra_repository import SafraRepository
from modules.safra.services.safra_service import SafraService

router = APIRouter(prefix="/safras", tags=["Safras"])

@router.post("/", response_model=SafraReadDTO, status_code=status.HTTP_201_CREATED)
async def create_safra(dto: SafraCreateDTO, db: AsyncSession = Depends(get_db)):
    service = SafraService(SafraRepository(db))
    try:
        safra = await service.create_safra(dto)
        return safra
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[SafraReadDTO])
async def list_safras(db: AsyncSession = Depends(get_db)):
    service = SafraService(SafraRepository(db))
    return await service.get_all_safras()

@router.get("/{safra_id}", response_model=SafraReadDTO)
async def get_safra(safra_id: int, db: AsyncSession = Depends(get_db)):
    service = SafraService(SafraRepository(db))
    safra = await service.get_safra_by_id(safra_id)
    if not safra:
        raise HTTPException(status_code=404, detail="Safra não encontrada")
    return safra

@router.put("/{safra_id}", response_model=SafraReadDTO)
async def update_safra(safra_id: int, dto: SafraUpdateDTO, db: AsyncSession = Depends(get_db)):
    service = SafraService(SafraRepository(db))
    try:
        return await service.update_safra(safra_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{safra_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_safra(safra_id: int, db: AsyncSession = Depends(get_db)):
    service = SafraService(SafraRepository(db))
    try:
        await service.delete_safra(safra_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 