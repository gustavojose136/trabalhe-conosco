import pytest
from httpx import AsyncClient
from modules.propriedade.entities.propriedade import Propriedade
from modules.produtor.entities.produtor import Produtor

class TestPropriedadeEndpoints:
    """Test cases for propriedade endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_propriedade_success(self, client: AsyncClient, sample_propriedade_data):
        """Test successful propriedade creation."""
        # First create a produtor
        produtor_data = {"cpf_cnpj": "12345678901", "nome": "João Teste"}
        produtor_response = await client.post("/produtores/", json=produtor_data)
        produtor_id = produtor_response.json()["id"]
        
        # Create propriedade
        propriedade_data = sample_propriedade_data.copy()
        propriedade_data["produtor_id"] = produtor_id
        
        response = await client.post("/propriedades/", json=propriedade_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == propriedade_data["nome"]
        assert data["cidade"] == propriedade_data["cidade"]
        assert data["estado"] == propriedade_data["estado"]
        assert data["area_total"] == propriedade_data["area_total"]
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_create_propriedade_invalid_produtor(self, client: AsyncClient, sample_propriedade_data):
        """Test creating propriedade with invalid produtor_id."""
        propriedade_data = sample_propriedade_data.copy()
        propriedade_data["produtor_id"] = 999  # Non-existent produtor
        
        response = await client.post("/propriedades/", json=propriedade_data)
        assert response.status_code == 400
        assert "produtor" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_get_propriedades_empty(self, client: AsyncClient):
        """Test getting empty propriedades list."""
        response = await client.get("/propriedades/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    @pytest.mark.asyncio
    async def test_get_propriedades_with_data(self, client: AsyncClient, sample_propriedade_data):
        """Test getting propriedades list with data."""
        # Create produtor and propriedade
        produtor_data = {"cpf_cnpj": "12345678901", "nome": "João Teste"}
        produtor_response = await client.post("/produtores/", json=produtor_data)
        produtor_id = produtor_response.json()["id"]
        
        propriedade_data = sample_propriedade_data.copy()
        propriedade_data["produtor_id"] = produtor_id
        await client.post("/propriedades/", json=propriedade_data)
        
        # Get all propriedades
        response = await client.get("/propriedades/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["nome"] == propriedade_data["nome"]
    
    @pytest.mark.asyncio
    async def test_create_propriedade_invalid_data(self, client: AsyncClient):
        """Test creating propriedade with invalid data."""
        invalid_data = {
            "nome": "",
            "cidade": "",
            "estado": "",
            "area_total": -1,
            "area_agricultavel": -1,
            "area_vegetacao": -1,
            "produtor_id": 1
        }
        response = await client.post("/propriedades/", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_create_propriedade_missing_fields(self, client: AsyncClient):
        """Test creating propriedade with missing required fields."""
        incomplete_data = {"nome": "Fazenda"}
        response = await client.post("/propriedades/", json=incomplete_data)
        assert response.status_code == 422  # Validation error

class TestPropriedadeService:
    """Test cases for propriedade service layer."""
    
    @pytest.mark.asyncio
    async def test_propriedade_service_create(self, db_session):
        """Test propriedade service create method."""
        from modules.propriedade.services.propriedade_service import PropriedadeService
        
        # Create produtor first
        produtor = Produtor(cpf_cnpj="98765432100", nome="Maria Teste")
        db_session.add(produtor)
        await db_session.commit()
        await db_session.refresh(produtor)
        
        service = PropriedadeService(db_session)
        propriedade_data = {
            "nome": "Fazenda Teste Service",
            "cidade": "Cidade Teste",
            "estado": "TS",
            "area_total": 150.0,
            "area_agricultavel": 100.0,
            "area_vegetacao": 50.0,
            "produtor_id": produtor.id
        }
        
        result = await service.create(propriedade_data)
        assert result.nome == propriedade_data["nome"]
        assert result.cidade == propriedade_data["cidade"]
        assert result.area_total == propriedade_data["area_total"]
        assert result.id is not None
    
    @pytest.mark.asyncio
    async def test_propriedade_service_get_all(self, db_session):
        """Test propriedade service get_all method."""
        from modules.propriedade.services.propriedade_service import PropriedadeService
        
        # Create test data
        produtor = Produtor(cpf_cnpj="11111111111", nome="Produtor Teste")
        db_session.add(produtor)
        await db_session.commit()
        await db_session.refresh(produtor)
        
        propriedade1 = Propriedade(
            nome="Fazenda 1",
            cidade="Cidade 1",
            estado="TS",
            area_total=100.0,
            area_agricultavel=60.0,
            area_vegetacao=40.0,
            produtor_id=produtor.id
        )
        propriedade2 = Propriedade(
            nome="Fazenda 2",
            cidade="Cidade 2",
            estado="TS",
            area_total=200.0,
            area_agricultavel=120.0,
            area_vegetacao=80.0,
            produtor_id=produtor.id
        )
        
        db_session.add(propriedade1)
        db_session.add(propriedade2)
        await db_session.commit()
        
        service = PropriedadeService(db_session)
        result = await service.get_all()
        assert len(result) == 2
        assert any(p.nome == "Fazenda 1" for p in result)
        assert any(p.nome == "Fazenda 2" for p in result)

class TestPropriedadeValidation:
    """Test cases for propriedade validation logic."""
    
    @pytest.mark.asyncio
    async def test_area_validation(self, client: AsyncClient):
        """Test area validation logic."""
        # Create produtor first
        produtor_data = {"cpf_cnpj": "12345678901", "nome": "João Teste"}
        produtor_response = await client.post("/produtores/", json=produtor_data)
        produtor_id = produtor_response.json()["id"]
        
        # Test invalid area (agricultavel + vegetacao > total)
        invalid_data = {
            "nome": "Fazenda Inválida",
            "cidade": "Cidade",
            "estado": "TS",
            "area_total": 100.0,
            "area_agricultavel": 80.0,
            "area_vegetacao": 30.0,  # 80 + 30 = 110 > 100
            "produtor_id": produtor_id
        }
        response = await client.post("/propriedades/", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_estado_validation(self, client: AsyncClient):
        """Test estado validation."""
        # Create produtor first
        produtor_data = {"cpf_cnpj": "12345678901", "nome": "João Teste"}
        produtor_response = await client.post("/produtores/", json=produtor_data)
        produtor_id = produtor_response.json()["id"]
        
        # Test invalid estado (too long)
        invalid_data = {
            "nome": "Fazenda",
            "cidade": "Cidade",
            "estado": "TST",  # Should be 2 characters
            "area_total": 100.0,
            "area_agricultavel": 60.0,
            "area_vegetacao": 40.0,
            "produtor_id": produtor_id
        }
        response = await client.post("/propriedades/", json=invalid_data)
        assert response.status_code == 422  # Validation error 