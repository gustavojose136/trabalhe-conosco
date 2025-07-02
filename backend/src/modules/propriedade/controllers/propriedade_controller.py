from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.session import get_db
from modules.propriedade.dtos.propriedade_dto import PropriedadeCreateDTO, PropriedadeUpdateDTO, PropriedadeReadDTO
from modules.propriedade.repositories.propriedade_repository import PropriedadeRepository
from modules.propriedade.services.propriedade_service import PropriedadeService

router = APIRouter(prefix="/propriedades", tags=["Propriedades"])

@router.post("/", response_model=PropriedadeReadDTO, status_code=status.HTTP_201_CREATED)
async def create_propriedade(dto: PropriedadeCreateDTO, db: AsyncSession = Depends(get_db)):
    service = PropriedadeService(PropriedadeRepository(db))
    try:
        propriedade = await service.create_propriedade(dto)
        return propriedade
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[PropriedadeReadDTO])
async def list_propriedades(db: AsyncSession = Depends(get_db)):
    service = PropriedadeService(PropriedadeRepository(db))
    return await service.get_all_propriedades()

@router.get("/{propriedade_id}", response_model=PropriedadeReadDTO)
async def get_propriedade(propriedade_id: int, db: AsyncSession = Depends(get_db)):
    service = PropriedadeService(PropriedadeRepository(db))
    propriedade = await service.get_propriedade_by_id(propriedade_id)
    if not propriedade:
        raise HTTPException(status_code=404, detail="Propriedade não encontrada")
    return propriedade

@router.put("/{propriedade_id}", response_model=PropriedadeReadDTO)
async def update_propriedade(propriedade_id: int, dto: PropriedadeUpdateDTO, db: AsyncSession = Depends(get_db)):
    service = PropriedadeService(PropriedadeRepository(db))
    try:
        return await service.update_propriedade(propriedade_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{propriedade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_propriedade(propriedade_id: int, db: AsyncSession = Depends(get_db)):
    service = PropriedadeService(PropriedadeRepository(db))
    try:
        await service.delete_propriedade(propriedade_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 