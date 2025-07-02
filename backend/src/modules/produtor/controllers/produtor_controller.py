from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.session import get_db
from modules.produtor.dtos.produtor_dto import ProdutorCreateDTO, ProdutorUpdateDTO, ProdutorReadDTO
from modules.produtor.repositories.produtor_repository import ProdutorRepository
from modules.produtor.services.produtor_service import ProdutorService

router = APIRouter(prefix="/produtores", tags=["Produtores"])

@router.post("/", response_model=ProdutorReadDTO, status_code=status.HTTP_201_CREATED)
async def create_produtor(dto: ProdutorCreateDTO, db: AsyncSession = Depends(get_db)):
    service = ProdutorService(ProdutorRepository(db))
    try:
        produtor = await service.create_produtor(dto)
        return produtor
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ProdutorReadDTO])
async def list_produtores(db: AsyncSession = Depends(get_db)):
    service = ProdutorService(ProdutorRepository(db))
    try:
        return await service.get_all_produtores()
    except Exception as e:
        import traceback
        print("Erro ao listar produtores:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar produtores: {e}")

@router.get("/{produtor_id}", response_model=ProdutorReadDTO)
async def get_produtor(produtor_id: int, db: AsyncSession = Depends(get_db)):
    service = ProdutorService(ProdutorRepository(db))
    produtor = await service.get_produtor_by_id(produtor_id)
    if not produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return produtor

@router.put("/{produtor_id}", response_model=ProdutorReadDTO)
async def update_produtor(produtor_id: int, dto: ProdutorUpdateDTO, db: AsyncSession = Depends(get_db)):
    service = ProdutorService(ProdutorRepository(db))
    try:
        return await service.update_produtor(produtor_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{produtor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_produtor(produtor_id: int, db: AsyncSession = Depends(get_db)):
    service = ProdutorService(ProdutorRepository(db))
    try:
        await service.delete_produtor(produtor_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 