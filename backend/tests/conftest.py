import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from shared.database.base import Base
from shared.database.session import get_session
from main import app

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_rural_db"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_db_setup():
    """Create test database tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session(test_db_setup):
    """Create a test database session."""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session):
    """Create a test client with dependency override."""
    async def override_get_session():
        yield db_session
    
    app.dependency_overrides[get_session] = override_get_session
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
def sample_produtor_data():
    """Sample data for testing produtor endpoints."""
    return {
        "cpf_cnpj": "12345678901",
        "nome": "João Teste"
    }

@pytest.fixture
def sample_propriedade_data():
    """Sample data for testing propriedade endpoints."""
    return {
        "nome": "Fazenda Teste",
        "cidade": "Teste City",
        "estado": "TS",
        "area_total": 100.0,
        "area_agricultavel": 60.0,
        "area_vegetacao": 40.0,
        "produtor_id": 1
    } 