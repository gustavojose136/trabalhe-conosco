import pytest
from httpx import AsyncClient
from modules.produtor.entities.produtor import Produtor

class TestProdutorEndpoints:
    """Test cases for produtor endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_produtor_success(self, client: AsyncClient, sample_produtor_data):
        """Test successful produtor creation."""
        response = await client.post("/produtores/", json=sample_produtor_data)
        assert response.status_code == 200
        data = response.json()
        assert data["cpf_cnpj"] == sample_produtor_data["cpf_cnpj"]
        assert data["nome"] == sample_produtor_data["nome"]
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_create_produtor_duplicate_cpf(self, client: AsyncClient, sample_produtor_data):
        """Test creating produtor with duplicate CPF."""
        # Create first produtor
        await client.post("/produtores/", json=sample_produtor_data)
        
        # Try to create second with same CPF
        response = await client.post("/produtores/", json=sample_produtor_data)
        assert response.status_code == 400
        assert "duplicate" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_get_produtores_empty(self, client: AsyncClient):
        """Test getting empty produtores list."""
        response = await client.get("/produtores/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    @pytest.mark.asyncio
    async def test_get_produtores_with_data(self, client: AsyncClient, sample_produtor_data):
        """Test getting produtores list with data."""
        # Create a produtor first
        await client.post("/produtores/", json=sample_produtor_data)
        
        # Get all produtores
        response = await client.get("/produtores/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["cpf_cnpj"] == sample_produtor_data["cpf_cnpj"]
    
    @pytest.mark.asyncio
    async def test_create_produtor_invalid_data(self, client: AsyncClient):
        """Test creating produtor with invalid data."""
        invalid_data = {"cpf_cnpj": "", "nome": ""}
        response = await client.post("/produtores/", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_create_produtor_missing_fields(self, client: AsyncClient):
        """Test creating produtor with missing required fields."""
        incomplete_data = {"nome": "João"}
        response = await client.post("/produtores/", json=incomplete_data)
        assert response.status_code == 422  # Validation error

class TestProdutorService:
    """Test cases for produtor service layer."""
    
    @pytest.mark.asyncio
    async def test_produtor_service_create(self, db_session):
        """Test produtor service create method."""
        from modules.produtor.services.produtor_service import ProdutorService
        
        service = ProdutorService(db_session)
        produtor_data = {
            "cpf_cnpj": "98765432100",
            "nome": "Maria Teste"
        }
        
        result = await service.create(produtor_data)
        assert result.cpf_cnpj == produtor_data["cpf_cnpj"]
        assert result.nome == produtor_data["nome"]
        assert result.id is not None
    
    @pytest.mark.asyncio
    async def test_produtor_service_get_all(self, db_session):
        """Test produtor service get_all method."""
        from modules.produtor.services.produtor_service import ProdutorService
        
        service = ProdutorService(db_session)
        
        # Create test data
        produtor1 = Produtor(cpf_cnpj="11111111111", nome="Produtor 1")
        produtor2 = Produtor(cpf_cnpj="22222222222", nome="Produtor 2")
        
        db_session.add(produtor1)
        db_session.add(produtor2)
        await db_session.commit()
        
        # Get all
        result = await service.get_all()
        assert len(result) == 2
        assert any(p.cpf_cnpj == "11111111111" for p in result)
        assert any(p.cpf_cnpj == "22222222222" for p in result)

class TestProdutorValidation:
    """Test cases for produtor validation logic."""
    
    @pytest.mark.asyncio
    async def test_cpf_validation_valid(self, client: AsyncClient):
        """Test valid CPF format."""
        valid_data = {
            "cpf_cnpj": "12345678901",
            "nome": "João Válido"
        }
        response = await client.post("/produtores/", json=valid_data)
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_cnpj_validation_valid(self, client: AsyncClient):
        """Test valid CNPJ format."""
        valid_data = {
            "cpf_cnpj": "12345678000199",
            "nome": "Empresa Válida"
        }
        response = await client.post("/produtores/", json=valid_data)
        assert response.status_code == 200 