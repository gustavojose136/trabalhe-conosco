import pytest
from httpx import AsyncClient
from modules.safra.entities.safra import Safra
from modules.produtor.entities.produtor import Produtor
from modules.propriedade.entities.propriedade import Propriedade
from modules.cultura.entities.cultura import Cultura

class TestSafraEndpoints:
    """Test cases for safra endpoints."""
    
    @pytest.fixture
    async def setup_test_data(self, client: AsyncClient):
        """Setup test data for safra tests."""
        # Create produtor
        produtor_data = {"cpf_cnpj": "12345678901", "nome": "João Teste"}
        produtor_response = await client.post("/produtores/", json=produtor_data)
        produtor_id = produtor_response.json()["id"]
        
        # Create propriedade
        propriedade_data = {
            "nome": "Fazenda Teste",
            "cidade": "Cidade Teste",
            "estado": "TS",
            "area_total": 100.0,
            "area_agricultavel": 60.0,
            "area_vegetacao": 40.0,
            "produtor_id": produtor_id
        }
        propriedade_response = await client.post("/propriedades/", json=propriedade_data)
        propriedade_id = propriedade_response.json()["id"]
        
        # Create cultura
        cultura_data = {"nome": "Soja", "descricao": "Cultura de soja"}
        cultura_response = await client.post("/culturas/", json=cultura_data)
        cultura_id = cultura_response.json()["id"]
        
        return {
            "produtor_id": produtor_id,
            "propriedade_id": propriedade_id,
            "cultura_id": cultura_id
        }
    
    @pytest.mark.asyncio
    async def test_create_safra_success(self, client: AsyncClient, setup_test_data):
        """Test successful safra creation."""
        test_data = await setup_test_data
        
        safra_data = {
            "ano": 2024,
            "area_plantada": 50.0,
            "produtividade": 3.5,
            "produtor_id": test_data["produtor_id"],
            "propriedade_id": test_data["propriedade_id"],
            "cultura_id": test_data["cultura_id"]
        }
        
        response = await client.post("/safras/", json=safra_data)
        assert response.status_code == 200
        data = response.json()
        assert data["ano"] == safra_data["ano"]
        assert data["area_plantada"] == safra_data["area_plantada"]
        assert data["produtividade"] == safra_data["produtividade"]
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_create_safra_invalid_produtor(self, client: AsyncClient, setup_test_data):
        """Test creating safra with invalid produtor_id."""
        test_data = await setup_test_data
        
        safra_data = {
            "ano": 2024,
            "area_plantada": 50.0,
            "produtividade": 3.5,
            "produtor_id": 999,  # Non-existent produtor
            "propriedade_id": test_data["propriedade_id"],
            "cultura_id": test_data["cultura_id"]
        }
        
        response = await client.post("/safras/", json=safra_data)
        assert response.status_code == 400
        assert "produtor" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_get_safras_empty(self, client: AsyncClient):
        """Test getting empty safras list."""
        response = await client.get("/safras/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    @pytest.mark.asyncio
    async def test_get_safras_with_data(self, client: AsyncClient, setup_test_data):
        """Test getting safras list with data."""
        test_data = await setup_test_data
        
        safra_data = {
            "ano": 2024,
            "area_plantada": 50.0,
            "produtividade": 3.5,
            "produtor_id": test_data["produtor_id"],
            "propriedade_id": test_data["propriedade_id"],
            "cultura_id": test_data["cultura_id"]
        }
        
        await client.post("/safras/", json=safra_data)
        
        response = await client.get("/safras/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["ano"] == safra_data["ano"]
    
    @pytest.mark.asyncio
    async def test_create_safra_invalid_data(self, client: AsyncClient, setup_test_data):
        """Test creating safra with invalid data."""
        test_data = await setup_test_data
        
        invalid_data = {
            "ano": -1,  # Invalid year
            "area_plantada": -1,  # Invalid area
            "produtividade": -1,  # Invalid productivity
            "produtor_id": test_data["produtor_id"],
            "propriedade_id": test_data["propriedade_id"],
            "cultura_id": test_data["cultura_id"]
        }
        
        response = await client.post("/safras/", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_create_safra_missing_fields(self, client: AsyncClient):
        """Test creating safra with missing required fields."""
        incomplete_data = {"ano": 2024}
        response = await client.post("/safras/", json=incomplete_data)
        assert response.status_code == 422  # Validation error

class TestSafraService:
    """Test cases for safra service layer."""
    
    @pytest.mark.asyncio
    async def test_safra_service_create(self, db_session):
        """Test safra service create method."""
        from modules.safra.services.safra_service import SafraService
        
        # Create dependencies
        produtor = Produtor(cpf_cnpj="98765432100", nome="Maria Teste")
        db_session.add(produtor)
        await db_session.commit()
        await db_session.refresh(produtor)
        
        propriedade = Propriedade(
            nome="Fazenda Teste",
            cidade="Cidade",
            estado="TS",
            area_total=100.0,
            area_agricultavel=60.0,
            area_vegetacao=40.0,
            produtor_id=produtor.id
        )
        db_session.add(propriedade)
        await db_session.commit()
        await db_session.refresh(propriedade)
        
        cultura = Cultura(nome="Soja", descricao="Cultura de soja")
        db_session.add(cultura)
        await db_session.commit()
        await db_session.refresh(cultura)
        
        service = SafraService(db_session)
        safra_data = {
            "ano": 2024,
            "area_plantada": 50.0,
            "produtividade": 3.5,
            "produtor_id": produtor.id,
            "propriedade_id": propriedade.id,
            "cultura_id": cultura.id
        }
        
        result = await service.create(safra_data)
        assert result.ano == safra_data["ano"]
        assert result.area_plantada == safra_data["area_plantada"]
        assert result.produtividade == safra_data["produtividade"]
        assert result.id is not None
    
    @pytest.mark.asyncio
    async def test_safra_service_get_all(self, db_session):
        """Test safra service get_all method."""
        from modules.safra.services.safra_service import SafraService
        
        # Create test data
        produtor = Produtor(cpf_cnpj="11111111111", nome="Produtor Teste")
        db_session.add(produtor)
        await db_session.commit()
        await db_session.refresh(produtor)
        
        propriedade = Propriedade(
            nome="Fazenda",
            cidade="Cidade",
            estado="TS",
            area_total=100.0,
            area_agricultavel=60.0,
            area_vegetacao=40.0,
            produtor_id=produtor.id
        )
        db_session.add(propriedade)
        await db_session.commit()
        await db_session.refresh(propriedade)
        
        cultura = Cultura(nome="Soja", descricao="Cultura de soja")
        db_session.add(cultura)
        await db_session.commit()
        await db_session.refresh(cultura)
        
        safra1 = Safra(
            ano=2023,
            area_plantada=40.0,
            produtividade=3.0,
            produtor_id=produtor.id,
            propriedade_id=propriedade.id,
            cultura_id=cultura.id
        )
        safra2 = Safra(
            ano=2024,
            area_plantada=50.0,
            produtividade=3.5,
            produtor_id=produtor.id,
            propriedade_id=propriedade.id,
            cultura_id=cultura.id
        )
        
        db_session.add(safra1)
        db_session.add(safra2)
        await db_session.commit()
        
        service = SafraService(db_session)
        result = await service.get_all()
        assert len(result) == 2
        assert any(s.ano == 2023 for s in result)
        assert any(s.ano == 2024 for s in result)

class TestSafraValidation:
    """Test cases for safra validation logic."""
    
    @pytest.mark.asyncio
    async def test_ano_validation(self, client: AsyncClient, setup_test_data):
        """Test year validation."""
        test_data = await setup_test_data
        
        # Test future year (should be valid)
        future_data = {
            "ano": 2030,
            "area_plantada": 50.0,
            "produtividade": 3.5,
            "produtor_id": test_data["produtor_id"],
            "propriedade_id": test_data["propriedade_id"],
            "cultura_id": test_data["cultura_id"]
        }
        response = await client.post("/safras/", json=future_data)
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_produtividade_validation(self, client: AsyncClient, setup_test_data):
        """Test productivity validation."""
        test_data = await setup_test_data
        
        # Test zero productivity (should be invalid)
        invalid_data = {
            "ano": 2024,
            "area_plantada": 50.0,
            "produtividade": 0.0,
            "produtor_id": test_data["produtor_id"],
            "propriedade_id": test_data["propriedade_id"],
            "cultura_id": test_data["cultura_id"]
        }
        response = await client.post("/safras/", json=invalid_data)
        assert response.status_code == 422  # Validation error 