import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from shared.database.session import engine
from shared.database.base import Base
from modules.produtor.entities.produtor import Produtor
from modules.propriedade.entities.propriedade import Propriedade
from modules.safra.entities.safra import Safra
from modules.cultura.entities.cultura import Cultura

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with engine.begin() as conn:
        # PRODUTORES
        for produtor in [
            {"cpf_cnpj": "12345678901", "nome": "João Silva"},
            {"cpf_cnpj": "98765432100", "nome": "Maria Souza"},
            {"cpf_cnpj": "12345678000199", "nome": "Agro S/A"},
        ]:
            result = await conn.execute(
                Produtor.__table__.select().where(Produtor.cpf_cnpj == produtor["cpf_cnpj"])
            )
            if not result.first():
                await conn.execute(Produtor.__table__.insert().values(**produtor))
        
        # PROPRIEDADES
        propriedades = [
            {"nome": "Fazenda Boa Vista", "cidade": "Uberlândia", "estado": "MG", "area_total": 100.0, "area_agricultavel": 60.0, "area_vegetacao": 40.0, "produtor_id": 1},
            {"nome": "Sítio Esperança", "cidade": "Ribeirão Preto", "estado": "SP", "area_total": 50.0, "area_agricultavel": 30.0, "area_vegetacao": 20.0, "produtor_id": 2},
            {"nome": "Fazenda Agro S/A", "cidade": "Campo Grande", "estado": "MS", "area_total": 200.0, "area_agricultavel": 150.0, "area_vegetacao": 50.0, "produtor_id": 3},
        ]
        for prop in propriedades:
            result = await conn.execute(
                Propriedade.__table__.select().where(
                    (Propriedade.nome == prop["nome"]) & (Propriedade.produtor_id == prop["produtor_id"])
                )
            )
            if not result.first():
                await conn.execute(Propriedade.__table__.insert().values(**prop))
        
        # SAFRAS
        safras = [
            {"ano": 2021, "propriedade_id": 1},
            {"ano": 2022, "propriedade_id": 1},
            {"ano": 2021, "propriedade_id": 2},
            {"ano": 2022, "propriedade_id": 3},
        ]
        for safra in safras:
            result = await conn.execute(
                Safra.__table__.select().where(
                    (Safra.ano == safra["ano"]) & (Safra.propriedade_id == safra["propriedade_id"])
                )
            )
            if not result.first():
                await conn.execute(Safra.__table__.insert().values(**safra))
        
        # CULTURAS
        culturas = [
            {"nome": "Soja", "safra_id": 1, "propriedade_id": 1},
            {"nome": "Milho", "safra_id": 1, "propriedade_id": 1},
            {"nome": "Café", "safra_id": 3, "propriedade_id": 2},
            {"nome": "Soja", "safra_id": 4, "propriedade_id": 3},
            {"nome": "Milho", "safra_id": 2, "propriedade_id": 1},
        ]
        for cultura in culturas:
            result = await conn.execute(
                Cultura.__table__.select().where(
                    (Cultura.nome == cultura["nome"]) & (Cultura.safra_id == cultura["safra_id"]) & (Cultura.propriedade_id == cultura["propriedade_id"])
                )
            )
            if not result.first():
                await conn.execute(Cultura.__table__.insert().values(**cultura))

if __name__ == "__main__":
    asyncio.run(init_db()) 