import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from modules.produtor.entities.produtor import Produtor
from modules.propriedade.entities.propriedade import Propriedade
from modules.cultura.entities.cultura import Cultura
from modules.safra.entities.safra import Safra
from shared.database.session import async_session
from sqlalchemy import text, select

async def seed_database():
    """Insere dados de teste no banco de dados"""
    # URL do banco de dados
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/rural_db")
    
    # Converter para async URL
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
    
    # Criar engine
    engine = create_async_engine(database_url, echo=True)
    
    # Criar sessão
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    
    async with session_factory() as session:
        try:
            # Criar culturas
            culturas = [
                Cultura(nome="Soja", descricao="Cultura de soja"),
                Cultura(nome="Milho", descricao="Cultura de milho"),
                Cultura(nome="Arroz", descricao="Cultura de arroz"),
                Cultura(nome="Feijão", descricao="Cultura de feijão"),
                Cultura(nome="Trigo", descricao="Cultura de trigo"),
                Cultura(nome="Café", descricao="Cultura de café"),
                Cultura(nome="Cana-de-açúcar", descricao="Cultura de cana-de-açúcar"),
                Cultura(nome="Algodão", descricao="Cultura de algodão")
            ]
            
            for cultura in culturas:
                exists = await session.execute(select(Cultura).where(Cultura.nome == cultura.nome))
                if not exists.scalars().first():
                    session.add(cultura)
            
            await session.commit()
            print("✅ Culturas criadas com sucesso!")
            
            # Criar produtores
            produtores = [
                Produtor(cpf_cnpj="123.456.789-01", nome="João Silva"),
                Produtor(cpf_cnpj="987.654.321-02", nome="Maria Santos"),
                Produtor(cpf_cnpj="456.789.123-03", nome="Pedro Oliveira"),
                Produtor(cpf_cnpj="789.123.456-04", nome="Ana Costa"),
                Produtor(cpf_cnpj="321.654.987-05", nome="Carlos Ferreira"),
                Produtor(cpf_cnpj="654.987.321-06", nome="Lucia Pereira"),
                Produtor(cpf_cnpj="147.258.369-07", nome="Roberto Lima"),
                Produtor(cpf_cnpj="258.369.147-08", nome="Fernanda Souza"),
                Produtor(cpf_cnpj="369.147.258-09", nome="Marcos Alves"),
                Produtor(cpf_cnpj="951.753.852-10", nome="Juliana Martins")
            ]
            
            for produtor in produtores:
                exists = await session.execute(select(Produtor).where(Produtor.cpf_cnpj == produtor.cpf_cnpj))
                if not exists.scalars().first():
                    session.add(produtor)
                    
            await session.commit()
            print("✅ Produtores criados com sucesso!")
            
            # Buscar produtores e culturas para usar nos relacionamentos
            produtores_db = await session.execute(text("SELECT id FROM produtores"))
            produtores_ids = [row[0] for row in produtores_db.fetchall()]
            
            culturas_db = await session.execute(text("SELECT id FROM culturas"))
            culturas_ids = [row[0] for row in culturas_db.fetchall()]
            
            # Criar propriedades
            propriedades = [
                Propriedade(
                    nome="Fazenda São João",
                    estado="SP",
                    municipio="Campinas",
                    area_total=1500.0,
                    area_agricultavel=1200.0,
                    area_vegetacao=300.0,
                    produtor_id=produtores_ids[0]
                ),
                Propriedade(
                    nome="Sítio Boa Vista",
                    estado="MG",
                    municipio="Uberlândia",
                    area_total=800.0,
                    area_agricultavel=600.0,
                    area_vegetacao=200.0,
                    produtor_id=produtores_ids[1]
                ),
                Propriedade(
                    nome="Rancho Alegre",
                    estado="GO",
                    municipio="Goiânia",
                    area_total=2000.0,
                    area_agricultavel=1600.0,
                    area_vegetacao=400.0,
                    produtor_id=produtores_ids[2]
                ),
                Propriedade(
                    nome="Fazenda Santa Clara",
                    estado="PR",
                    municipio="Londrina",
                    area_total=1200.0,
                    area_agricultavel=900.0,
                    area_vegetacao=300.0,
                    produtor_id=produtores_ids[3]
                ),
                Propriedade(
                    nome="Sítio Primavera",
                    estado="RS",
                    municipio="Porto Alegre",
                    area_total=600.0,
                    area_agricultavel=450.0,
                    area_vegetacao=150.0,
                    produtor_id=produtores_ids[4]
                ),
                Propriedade(
                    nome="Fazenda Nova Esperança",
                    estado="MT",
                    municipio="Cuiabá",
                    area_total=3000.0,
                    area_agricultavel=2400.0,
                    area_vegetacao=600.0,
                    produtor_id=produtores_ids[5]
                ),
                Propriedade(
                    nome="Rancho São Pedro",
                    estado="MS",
                    municipio="Campo Grande",
                    area_total=1800.0,
                    area_agricultavel=1400.0,
                    area_vegetacao=400.0,
                    produtor_id=produtores_ids[6]
                ),
                Propriedade(
                    nome="Fazenda Bela Vista",
                    estado="BA",
                    municipio="Salvador",
                    area_total=900.0,
                    area_agricultavel=700.0,
                    area_vegetacao=200.0,
                    produtor_id=produtores_ids[7]
                ),
                Propriedade(
                    nome="Sítio dos Ipês",
                    estado="TO",
                    municipio="Palmas",
                    area_total=2500.0,
                    area_agricultavel=2000.0,
                    area_vegetacao=500.0,
                    produtor_id=produtores_ids[8]
                ),
                Propriedade(
                    nome="Fazenda Progresso",
                    estado="PA",
                    municipio="Belém",
                    area_total=3500.0,
                    area_agricultavel=2800.0,
                    area_vegetacao=700.0,
                    produtor_id=produtores_ids[9]
                )
            ]
            
            for propriedade in propriedades:
                session.add(propriedade)
            
            await session.commit()
            print("✅ Propriedades criadas com sucesso!")
            
            # Buscar propriedades para usar nos relacionamentos
            propriedades_db = await session.execute(text("SELECT id FROM propriedades"))
            propriedades_ids = [row[0] for row in propriedades_db.fetchall()]
            
            # Criar safras
            safras = [
                Safra(
                    ano=2023,
                    descricao="Safra 2023/2024",
                    propriedade_id=propriedades_ids[0],
                    cultura_id=culturas_ids[0]  # Soja
                ),
                Safra(
                    ano=2023,
                    descricao="Safra 2023/2024",
                    propriedade_id=propriedades_ids[1],
                    cultura_id=culturas_ids[1]  # Milho
                ),
                Safra(
                    ano=2023,
                    descricao="Safra 2023/2024",
                    propriedade_id=propriedades_ids[2],
                    cultura_id=culturas_ids[2]  # Arroz
                ),
                Safra(
                    ano=2023,
                    descricao="Safra 2023/2024",
                    propriedade_id=propriedades_ids[3],
                    cultura_id=culturas_ids[3]  # Feijão
                ),
                Safra(
                    ano=2023,
                    descricao="Safra 2023/2024",
                    propriedade_id=propriedades_ids[4],
                    cultura_id=culturas_ids[4]  # Trigo
                ),
                Safra(
                    ano=2024,
                    descricao="Safra 2024/2025",
                    propriedade_id=propriedades_ids[5],
                    cultura_id=culturas_ids[5]  # Café
                ),
                Safra(
                    ano=2024,
                    descricao="Safra 2024/2025",
                    propriedade_id=propriedades_ids[6],
                    cultura_id=culturas_ids[6]  # Cana-de-açúcar
                ),
                Safra(
                    ano=2024,
                    descricao="Safra 2024/2025",
                    propriedade_id=propriedades_ids[7],
                    cultura_id=culturas_ids[7]  # Algodão
                ),
                Safra(
                    ano=2024,
                    descricao="Safra 2024/2025",
                    propriedade_id=propriedades_ids[8],
                    cultura_id=culturas_ids[0]  # Soja
                ),
                Safra(
                    ano=2024,
                    descricao="Safra 2024/2025",
                    propriedade_id=propriedades_ids[9],
                    cultura_id=culturas_ids[1]  # Milho
                )
            ]
            
            for safra in safras:
                session.add(safra)
            
            await session.commit()
            print("✅ Safras criadas com sucesso!")
            
            print("🎉 Todos os dados de teste foram inseridos com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inserir dados: {e}")
            await session.rollback()
            raise

if __name__ == "__main__":
    asyncio.run(seed_database()) 