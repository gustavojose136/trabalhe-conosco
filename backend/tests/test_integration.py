import pytest
from httpx import AsyncClient

class TestIntegrationFlow:
    """Integration tests for complete application flow."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_complete_crud_flow(self, client: AsyncClient):
        """Test complete CRUD flow for all entities."""
        
        # 1. Create Cultura
        cultura_data = {"nome": "Soja", "descricao": "Cultura de soja"}
        cultura_response = await client.post("/culturas/", json=cultura_data)
        assert cultura_response.status_code == 200
        cultura_id = cultura_response.json()["id"]
        
        # 2. Create Produtor
        produtor_data = {"cpf_cnpj": "12345678901", "nome": "João Silva"}
        produtor_response = await client.post("/produtores/", json=produtor_data)
        assert produtor_response.status_code == 200
        produtor_id = produtor_response.json()["id"]
        
        # 3. Create Propriedade
        propriedade_data = {
            "nome": "Fazenda São João",
            "cidade": "São Paulo",
            "estado": "SP",
            "area_total": 100.0,
            "area_agricultavel": 60.0,
            "area_vegetacao": 40.0,
            "produtor_id": produtor_id
        }
        propriedade_response = await client.post("/propriedades/", json=propriedade_data)
        assert propriedade_response.status_code == 200
        propriedade_id = propriedade_response.json()["id"]
        
        # 4. Create Safra
        safra_data = {
            "ano": 2024,
            "area_plantada": 50.0,
            "produtividade": 3.5,
            "produtor_id": produtor_id,
            "propriedade_id": propriedade_id,
            "cultura_id": cultura_id
        }
        safra_response = await client.post("/safras/", json=safra_data)
        assert safra_response.status_code == 200
        safra_id = safra_response.json()["id"]
        
        # 5. Verify all entities were created
        culturas = await client.get("/culturas/")
        assert culturas.status_code == 200
        assert len(culturas.json()) == 1
        
        produtores = await client.get("/produtores/")
        assert produtores.status_code == 200
        assert len(produtores.json()) == 1
        
        propriedades = await client.get("/propriedades/")
        assert propriedades.status_code == 200
        assert len(propriedades.json()) == 1
        
        safras = await client.get("/safras/")
        assert safras.status_code == 200
        assert len(safras.json()) == 1
        
        # 6. Check dashboard stats
        dashboard_stats = await client.get("/dashboard/stats")
        assert dashboard_stats.status_code == 200
        stats = dashboard_stats.json()
        assert stats["total_produtores"] == 1
        assert stats["total_propriedades"] == 1
        assert stats["total_safras"] == 1
        assert stats["total_culturas"] == 1
        assert stats["area_total_agricultavel"] == 60.0
        assert stats["area_total_vegetacao"] == 40.0
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_data_relationships(self, client: AsyncClient):
        """Test that data relationships are properly maintained."""
        
        # Create multiple entities with relationships
        cultura1 = await client.post("/culturas/", json={"nome": "Soja", "descricao": "Soja"})
        cultura2 = await client.post("/culturas/", json={"nome": "Milho", "descricao": "Milho"})
        
        produtor1 = await client.post("/produtores/", json={"cpf_cnpj": "11111111111", "nome": "João"})
        produtor2 = await client.post("/produtores/", json={"cpf_cnpj": "22222222222", "nome": "Maria"})
        
        propriedade1 = await client.post("/propriedades/", json={
            "nome": "Fazenda 1", "cidade": "SP", "estado": "SP",
            "area_total": 100.0, "area_agricultavel": 60.0, "area_vegetacao": 40.0,
            "produtor_id": produtor1.json()["id"]
        })
        propriedade2 = await client.post("/propriedades/", json={
            "nome": "Fazenda 2", "cidade": "MG", "estado": "MG",
            "area_total": 200.0, "area_agricultavel": 120.0, "area_vegetacao": 80.0,
            "produtor_id": produtor2.json()["id"]
        })
        
        # Create safras with different relationships
        safra1 = await client.post("/safras/", json={
            "ano": 2023, "area_plantada": 40.0, "produtividade": 3.0,
            "produtor_id": produtor1.json()["id"],
            "propriedade_id": propriedade1.json()["id"],
            "cultura_id": cultura1.json()["id"]
        })
        safra2 = await client.post("/safras/", json={
            "ano": 2024, "area_plantada": 80.0, "produtividade": 3.5,
            "produtor_id": produtor2.json()["id"],
            "propriedade_id": propriedade2.json()["id"],
            "cultura_id": cultura2.json()["id"]
        })
        
        # Verify relationships in dashboard
        produtores_por_estado = await client.get("/dashboard/produtores-por-estado")
        assert produtores_por_estado.status_code == 200
        estados_data = produtores_por_estado.json()
        assert len(estados_data) == 2
        
        safras_por_ano = await client.get("/dashboard/safras-por-ano")
        assert safras_por_ano.status_code == 200
        anos_data = safras_por_ano.json()
        assert len(anos_data) == 2
        
        culturas_mais_plantadas = await client.get("/dashboard/culturas-mais-plantadas")
        assert culturas_mais_plantadas.status_code == 200
        culturas_data = culturas_mais_plantadas.json()
        assert len(culturas_data) == 2
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_error_handling_flow(self, client: AsyncClient):
        """Test error handling in complete flow."""
        
        # Try to create propriedade with non-existent produtor
        propriedade_data = {
            "nome": "Fazenda",
            "cidade": "Cidade",
            "estado": "SP",
            "area_total": 100.0,
            "area_agricultavel": 60.0,
            "area_vegetacao": 40.0,
            "produtor_id": 999  # Non-existent
        }
        response = await client.post("/propriedades/", json=propriedade_data)
        assert response.status_code == 400
        
        # Try to create safra with non-existent entities
        safra_data = {
            "ano": 2024,
            "area_plantada": 50.0,
            "produtividade": 3.5,
            "produtor_id": 999,
            "propriedade_id": 999,
            "cultura_id": 999
        }
        response = await client.post("/safras/", json=safra_data)
        assert response.status_code == 400
        
        # Try to create duplicate produtor
        produtor_data = {"cpf_cnpj": "12345678901", "nome": "João"}
        await client.post("/produtores/", json=produtor_data)
        response = await client.post("/produtores/", json=produtor_data)
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_validation_flow(self, client: AsyncClient):
        """Test validation rules in complete flow."""
        
        # Test invalid CPF/CNPJ
        invalid_produtor = {"cpf_cnpj": "123", "nome": "João"}
        response = await client.post("/produtores/", json=invalid_produtor)
        assert response.status_code == 422
        
        # Test invalid area calculations
        invalid_propriedade = {
            "nome": "Fazenda",
            "cidade": "Cidade",
            "estado": "SP",
            "area_total": 100.0,
            "area_agricultavel": 80.0,
            "area_vegetacao": 30.0,  # 80 + 30 = 110 > 100
            "produtor_id": 1
        }
        response = await client.post("/propriedades/", json=invalid_propriedade)
        assert response.status_code == 422
        
        # Test invalid year
        invalid_safra = {
            "ano": -1,
            "area_plantada": 50.0,
            "produtividade": 3.5,
            "produtor_id": 1,
            "propriedade_id": 1,
            "cultura_id": 1
        }
        response = await client.post("/safras/", json=invalid_safra)
        assert response.status_code == 422

class TestPerformanceIntegration:
    """Performance integration tests."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_bulk_operations(self, client: AsyncClient):
        """Test performance with bulk operations."""
        
        # Create multiple entities quickly
        for i in range(10):
            cultura_data = {"nome": f"Cultura {i}", "descricao": f"Descrição {i}"}
            await client.post("/culturas/", json=cultura_data)
            
            produtor_data = {"cpf_cnpj": f"1234567890{i}", "nome": f"Produtor {i}"}
            await client.post("/produtores/", json=produtor_data)
        
        # Verify all were created
        culturas = await client.get("/culturas/")
        assert len(culturas.json()) == 10
        
        produtores = await client.get("/produtores/")
        assert len(produtores.json()) == 10
        
        # Check dashboard performance
        dashboard_stats = await client.get("/dashboard/stats")
        assert dashboard_stats.status_code == 200
        stats = dashboard_stats.json()
        assert stats["total_produtores"] == 10
        assert stats["total_culturas"] == 10 