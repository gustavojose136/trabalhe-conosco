import pytest
from httpx import AsyncClient
from modules.produtor.entities.produtor import Produtor
from modules.propriedade.entities.propriedade import Propriedade
from modules.safra.entities.safra import Safra
from modules.cultura.entities.cultura import Cultura

class TestDashboardEndpoints:
    """Test cases for dashboard endpoints."""
    
    @pytest.fixture
    async def setup_dashboard_data(self, db_session):
        """Setup test data for dashboard tests."""
        # Create produtores
        produtor1 = Produtor(cpf_cnpj="11111111111", nome="Produtor 1")
        produtor2 = Produtor(cpf_cnpj="22222222222", nome="Produtor 2")
        db_session.add(produtor1)
        db_session.add(produtor2)
        await db_session.commit()
        await db_session.refresh(produtor1)
        await db_session.refresh(produtor2)
        
        # Create propriedades
        propriedade1 = Propriedade(
            nome="Fazenda 1",
            cidade="Cidade 1",
            estado="SP",
            area_total=100.0,
            area_agricultavel=60.0,
            area_vegetacao=40.0,
            produtor_id=produtor1.id
        )
        propriedade2 = Propriedade(
            nome="Fazenda 2",
            cidade="Cidade 2",
            estado="MG",
            area_total=200.0,
            area_agricultavel=120.0,
            area_vegetacao=80.0,
            produtor_id=produtor2.id
        )
        db_session.add(propriedade1)
        db_session.add(propriedade2)
        await db_session.commit()
        await db_session.refresh(propriedade1)
        await db_session.refresh(propriedade2)
        
        # Create culturas
        cultura1 = Cultura(nome="Soja", descricao="Cultura de soja")
        cultura2 = Cultura(nome="Milho", descricao="Cultura de milho")
        db_session.add(cultura1)
        db_session.add(cultura2)
        await db_session.commit()
        await db_session.refresh(cultura1)
        await db_session.refresh(cultura2)
        
        # Create safras
        safra1 = Safra(
            ano=2023,
            area_plantada=50.0,
            produtividade=3.0,
            produtor_id=produtor1.id,
            propriedade_id=propriedade1.id,
            cultura_id=cultura1.id
        )
        safra2 = Safra(
            ano=2024,
            area_plantada=80.0,
            produtividade=3.5,
            produtor_id=produtor2.id,
            propriedade_id=propriedade2.id,
            cultura_id=cultura2.id
        )
        db_session.add(safra1)
        db_session.add(safra2)
        await db_session.commit()
        
        return {
            "produtores": [produtor1, produtor2],
            "propriedades": [propriedade1, propriedade2],
            "culturas": [cultura1, cultura2],
            "safras": [safra1, safra2]
        }
    
    @pytest.mark.asyncio
    async def test_dashboard_stats_empty(self, client: AsyncClient):
        """Test dashboard stats with empty database."""
        response = await client.get("/dashboard/stats")
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert "total_produtores" in data
        assert "total_propriedades" in data
        assert "total_safras" in data
        assert "total_culturas" in data
        assert "area_total_agricultavel" in data
        assert "area_total_vegetacao" in data
        
        # Check values are zero
        assert data["total_produtores"] == 0
        assert data["total_propriedades"] == 0
        assert data["total_safras"] == 0
        assert data["total_culturas"] == 0
        assert data["area_total_agricultavel"] == 0.0
        assert data["area_total_vegetacao"] == 0.0
    
    @pytest.mark.asyncio
    async def test_dashboard_stats_with_data(self, client: AsyncClient, setup_dashboard_data):
        """Test dashboard stats with test data."""
        await setup_dashboard_data
        
        response = await client.get("/dashboard/stats")
        assert response.status_code == 200
        data = response.json()
        
        # Check values match test data
        assert data["total_produtores"] == 2
        assert data["total_propriedades"] == 2
        assert data["total_safras"] == 2
        assert data["total_culturas"] == 2
        assert data["area_total_agricultavel"] == 180.0  # 60 + 120
        assert data["area_total_vegetacao"] == 120.0  # 40 + 80
    
    @pytest.mark.asyncio
    async def test_dashboard_produtores_por_estado(self, client: AsyncClient, setup_dashboard_data):
        """Test dashboard produtores por estado endpoint."""
        await setup_dashboard_data
        
        response = await client.get("/dashboard/produtores-por-estado")
        assert response.status_code == 200
        data = response.json()
        
        # Should have data for SP and MG
        assert len(data) == 2
        estados = [item["estado"] for item in data]
        assert "SP" in estados
        assert "MG" in estados
        
        # Check counts
        for item in data:
            if item["estado"] == "SP":
                assert item["total"] == 1
            elif item["estado"] == "MG":
                assert item["total"] == 1
    
    @pytest.mark.asyncio
    async def test_dashboard_safras_por_ano(self, client: AsyncClient, setup_dashboard_data):
        """Test dashboard safras por ano endpoint."""
        await setup_dashboard_data
        
        response = await client.get("/dashboard/safras-por-ano")
        assert response.status_code == 200
        data = response.json()
        
        # Should have data for 2023 and 2024
        assert len(data) == 2
        anos = [item["ano"] for item in data]
        assert 2023 in anos
        assert 2024 in anos
        
        # Check counts
        for item in data:
            if item["ano"] == 2023:
                assert item["total"] == 1
            elif item["ano"] == 2024:
                assert item["total"] == 1
    
    @pytest.mark.asyncio
    async def test_dashboard_culturas_mais_plantadas(self, client: AsyncClient, setup_dashboard_data):
        """Test dashboard culturas mais plantadas endpoint."""
        await setup_dashboard_data
        
        response = await client.get("/dashboard/culturas-mais-plantadas")
        assert response.status_code == 200
        data = response.json()
        
        # Should have data for both culturas
        assert len(data) == 2
        culturas = [item["cultura"] for item in data]
        assert "Soja" in culturas
        assert "Milho" in culturas
        
        # Check area plantada
        for item in data:
            if item["cultura"] == "Soja":
                assert item["area_plantada"] == 50.0
            elif item["cultura"] == "Milho":
                assert item["area_plantada"] == 80.0

class TestDashboardService:
    """Test cases for dashboard service layer."""
    
    @pytest.mark.asyncio
    async def test_dashboard_service_get_stats(self, db_session, setup_dashboard_data):
        """Test dashboard service get_stats method."""
        from modules.dashboard.services.dashboard_service import DashboardService
        
        await setup_dashboard_data
        
        service = DashboardService(db_session)
        stats = await service.get_stats()
        
        assert stats["total_produtores"] == 2
        assert stats["total_propriedades"] == 2
        assert stats["total_safras"] == 2
        assert stats["total_culturas"] == 2
        assert stats["area_total_agricultavel"] == 180.0
        assert stats["area_total_vegetacao"] == 120.0
    
    @pytest.mark.asyncio
    async def test_dashboard_service_get_produtores_por_estado(self, db_session, setup_dashboard_data):
        """Test dashboard service get_produtores_por_estado method."""
        from modules.dashboard.services.dashboard_service import DashboardService
        
        await setup_dashboard_data
        
        service = DashboardService(db_session)
        result = await service.get_produtores_por_estado()
        
        assert len(result) == 2
        estados = [item["estado"] for item in result]
        assert "SP" in estados
        assert "MG" in estados
    
    @pytest.mark.asyncio
    async def test_dashboard_service_get_safras_por_ano(self, db_session, setup_dashboard_data):
        """Test dashboard service get_safras_por_ano method."""
        from modules.dashboard.services.dashboard_service import DashboardService
        
        await setup_dashboard_data
        
        service = DashboardService(db_session)
        result = await service.get_safras_por_ano()
        
        assert len(result) == 2
        anos = [item["ano"] for item in result]
        assert 2023 in anos
        assert 2024 in anos
    
    @pytest.mark.asyncio
    async def test_dashboard_service_get_culturas_mais_plantadas(self, db_session, setup_dashboard_data):
        """Test dashboard service get_culturas_mais_plantadas method."""
        from modules.dashboard.services.dashboard_service import DashboardService
        
        await setup_dashboard_data
        
        service = DashboardService(db_session)
        result = await service.get_culturas_mais_plantadas()
        
        assert len(result) == 2
        culturas = [item["cultura"] for item in result]
        assert "Soja" in culturas
        assert "Milho" in culturas

class TestDashboardIntegration:
    """Integration tests for dashboard functionality."""
    
    @pytest.mark.asyncio
    async def test_dashboard_complete_flow(self, client: AsyncClient):
        """Test complete dashboard flow with data creation."""
        # Create produtor
        produtor_data = {"cpf_cnpj": "12345678901", "nome": "João Teste"}
        produtor_response = await client.post("/produtores/", json=produtor_data)
        produtor_id = produtor_response.json()["id"]
        
        # Create propriedade
        propriedade_data = {
            "nome": "Fazenda Teste",
            "cidade": "Cidade Teste",
            "estado": "SP",
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
        
        # Create safra
        safra_data = {
            "ano": 2024,
            "area_plantada": 50.0,
            "produtividade": 3.5,
            "produtor_id": produtor_id,
            "propriedade_id": propriedade_id,
            "cultura_id": cultura_id
        }
        await client.post("/safras/", json=safra_data)
        
        # Check dashboard stats
        stats_response = await client.get("/dashboard/stats")
        assert stats_response.status_code == 200
        stats = stats_response.json()
        
        assert stats["total_produtores"] == 1
        assert stats["total_propriedades"] == 1
        assert stats["total_safras"] == 1
        assert stats["total_culturas"] == 1
        assert stats["area_total_agricultavel"] == 60.0
        assert stats["area_total_vegetacao"] == 40.0 