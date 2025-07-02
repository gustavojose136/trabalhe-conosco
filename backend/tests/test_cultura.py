import pytest
from httpx import AsyncClient
from modules.cultura.entities.cultura import Cultura

class TestCulturaEndpoints:
    """Test cases for cultura endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_cultura_success(self, client: AsyncClient):
        """Test successful cultura creation."""
        cultura_data = {
            "nome": "Soja",
            "descricao": "Cultura de soja para produção de óleo"
        }
        
        response = await client.post("/culturas/", json=cultura_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == cultura_data["nome"]
        assert data["descricao"] == cultura_data["descricao"]
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_create_cultura_duplicate_name(self, client: AsyncClient):
        """Test creating cultura with duplicate name."""
        cultura_data = {
            "nome": "Milho",
            "descricao": "Cultura de milho"
        }
        
        # Create first cultura
        await client.post("/culturas/", json=cultura_data)
        
        # Try to create second with same name
        response = await client.post("/culturas/", json=cultura_data)
        assert response.status_code == 400
        assert "duplicate" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_get_culturas_empty(self, client: AsyncClient):
        """Test getting empty culturas list."""
        response = await client.get("/culturas/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    @pytest.mark.asyncio
    async def test_get_culturas_with_data(self, client: AsyncClient):
        """Test getting culturas list with data."""
        cultura_data = {
            "nome": "Trigo",
            "descricao": "Cultura de trigo"
        }
        
        # Create a cultura first
        await client.post("/culturas/", json=cultura_data)
        
        # Get all culturas
        response = await client.get("/culturas/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["nome"] == cultura_data["nome"]
    
    @pytest.mark.asyncio
    async def test_create_cultura_invalid_data(self, client: AsyncClient):
        """Test creating cultura with invalid data."""
        invalid_data = {
            "nome": "",  # Empty name
            "descricao": "Descrição válida"
        }
        response = await client.post("/culturas/", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_create_cultura_missing_fields(self, client: AsyncClient):
        """Test creating cultura with missing required fields."""
        incomplete_data = {"descricao": "Apenas descrição"}
        response = await client.post("/culturas/", json=incomplete_data)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_get_cultura_by_id(self, client: AsyncClient):
        """Test getting cultura by ID."""
        cultura_data = {
            "nome": "Arroz",
            "descricao": "Cultura de arroz"
        }
        
        # Create cultura
        create_response = await client.post("/culturas/", json=cultura_data)
        cultura_id = create_response.json()["id"]
        
        # Get by ID
        response = await client.get(f"/culturas/{cultura_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == cultura_id
        assert data["nome"] == cultura_data["nome"]
    
    @pytest.mark.asyncio
    async def test_get_cultura_by_id_not_found(self, client: AsyncClient):
        """Test getting cultura by non-existent ID."""
        response = await client.get("/culturas/999")
        assert response.status_code == 404

class TestCulturaService:
    """Test cases for cultura service layer."""
    
    @pytest.mark.asyncio
    async def test_cultura_service_create(self, db_session):
        """Test cultura service create method."""
        from modules.cultura.services.cultura_service import CulturaService
        
        service = CulturaService(db_session)
        cultura_data = {
            "nome": "Feijão",
            "descricao": "Cultura de feijão"
        }
        
        result = await service.create(cultura_data)
        assert result.nome == cultura_data["nome"]
        assert result.descricao == cultura_data["descricao"]
        assert result.id is not None
    
    @pytest.mark.asyncio
    async def test_cultura_service_get_all(self, db_session):
        """Test cultura service get_all method."""
        from modules.cultura.services.cultura_service import CulturaService
        
        # Create test data
        cultura1 = Cultura(nome="Cultura 1", descricao="Descrição 1")
        cultura2 = Cultura(nome="Cultura 2", descricao="Descrição 2")
        
        db_session.add(cultura1)
        db_session.add(cultura2)
        await db_session.commit()
        
        service = CulturaService(db_session)
        result = await service.get_all()
        assert len(result) == 2
        assert any(c.nome == "Cultura 1" for c in result)
        assert any(c.nome == "Cultura 2" for c in result)
    
    @pytest.mark.asyncio
    async def test_cultura_service_get_by_id(self, db_session):
        """Test cultura service get_by_id method."""
        from modules.cultura.services.cultura_service import CulturaService
        
        # Create test data
        cultura = Cultura(nome="Cultura Teste", descricao="Descrição teste")
        db_session.add(cultura)
        await db_session.commit()
        await db_session.refresh(cultura)
        
        service = CulturaService(db_session)
        result = await service.get_by_id(cultura.id)
        assert result is not None
        assert result.nome == "Cultura Teste"
        assert result.id == cultura.id
    
    @pytest.mark.asyncio
    async def test_cultura_service_get_by_id_not_found(self, db_session):
        """Test cultura service get_by_id with non-existent ID."""
        from modules.cultura.services.cultura_service import CulturaService
        
        service = CulturaService(db_session)
        result = await service.get_by_id(999)
        assert result is None

class TestCulturaValidation:
    """Test cases for cultura validation logic."""
    
    @pytest.mark.asyncio
    async def test_nome_validation_length(self, client: AsyncClient):
        """Test nome length validation."""
        # Test very long name
        long_nome = "A" * 101  # More than 100 characters
        invalid_data = {
            "nome": long_nome,
            "descricao": "Descrição válida"
        }
        response = await client.post("/culturas/", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_descricao_validation_length(self, client: AsyncClient):
        """Test descricao length validation."""
        # Test very long description
        long_descricao = "A" * 501  # More than 500 characters
        invalid_data = {
            "nome": "Nome válido",
            "descricao": long_descricao
        }
        response = await client.post("/culturas/", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_nome_validation_special_chars(self, client: AsyncClient):
        """Test nome with special characters (should be valid)."""
        special_nome = "Soja-Genética (Transgênica)"
        valid_data = {
            "nome": special_nome,
            "descricao": "Descrição válida"
        }
        response = await client.post("/culturas/", json=valid_data)
        assert response.status_code == 200 