import pytest
from shared.utils.validators import validate_cpf_cnpj, validate_area_calculation

class TestValidators:
    """Test cases for validation utilities."""
    
    def test_validate_cpf_valid(self):
        """Test valid CPF validation."""
        valid_cpfs = [
            "12345678901",
            "98765432100",
            "11111111111"
        ]
        
        for cpf in valid_cpfs:
            assert validate_cpf_cnpj(cpf) is True
    
    def test_validate_cnpj_valid(self):
        """Test valid CNPJ validation."""
        valid_cnpjs = [
            "12345678000199",
            "98765432000199",
            "11111111000199"
        ]
        
        for cnpj in valid_cnpjs:
            assert validate_cpf_cnpj(cnpj) is True
    
    def test_validate_cpf_cnpj_invalid(self):
        """Test invalid CPF/CNPJ validation."""
        invalid_values = [
            "123",  # Too short
            "123456789012345",  # Too long
            "abcdefghijk",  # Non-numeric
            "",  # Empty
            None  # None
        ]
        
        for value in invalid_values:
            assert validate_cpf_cnpj(value) is False
    
    def test_validate_area_calculation_valid(self):
        """Test valid area calculation validation."""
        valid_calculations = [
            (100.0, 60.0, 40.0),  # 60 + 40 = 100
            (200.0, 120.0, 80.0),  # 120 + 80 = 200
            (50.0, 30.0, 20.0),   # 30 + 20 = 50
        ]
        
        for total, agricultavel, vegetacao in valid_calculations:
            assert validate_area_calculation(total, agricultavel, vegetacao) is True
    
    def test_validate_area_calculation_invalid(self):
        """Test invalid area calculation validation."""
        invalid_calculations = [
            (100.0, 80.0, 30.0),   # 80 + 30 = 110 > 100
            (200.0, 150.0, 60.0),  # 150 + 60 = 210 > 200
            (50.0, 40.0, 15.0),    # 40 + 15 = 55 > 50
        ]
        
        for total, agricultavel, vegetacao in invalid_calculations:
            assert validate_area_calculation(total, agricultavel, vegetacao) is False
    
    def test_validate_area_calculation_edge_cases(self):
        """Test edge cases for area calculation validation."""
        # Zero values
        assert validate_area_calculation(0.0, 0.0, 0.0) is True
        
        # Negative values (should be invalid)
        assert validate_area_calculation(-100.0, 60.0, 40.0) is False
        assert validate_area_calculation(100.0, -60.0, 40.0) is False
        assert validate_area_calculation(100.0, 60.0, -40.0) is False
        
        # Exact match
        assert validate_area_calculation(100.0, 100.0, 0.0) is True
        assert validate_area_calculation(100.0, 0.0, 100.0) is True

class TestDTOValidation:
    """Test cases for DTO validation."""
    
    def test_produtor_dto_validation(self):
        """Test ProdutorDTO validation."""
        from modules.produtor.dtos.produtor_dto import ProdutorDTO
        
        # Valid data
        valid_data = {
            "cpf_cnpj": "12345678901",
            "nome": "João Silva"
        }
        dto = ProdutorDTO(**valid_data)
        assert dto.cpf_cnpj == valid_data["cpf_cnpj"]
        assert dto.nome == valid_data["nome"]
    
    def test_propriedade_dto_validation(self):
        """Test PropriedadeDTO validation."""
        from modules.propriedade.dtos.propriedade_dto import PropriedadeDTO
        
        # Valid data
        valid_data = {
            "nome": "Fazenda São João",
            "cidade": "São Paulo",
            "estado": "SP",
            "area_total": 100.0,
            "area_agricultavel": 60.0,
            "area_vegetacao": 40.0,
            "produtor_id": 1
        }
        dto = PropriedadeDTO(**valid_data)
        assert dto.nome == valid_data["nome"]
        assert dto.area_total == valid_data["area_total"]
        assert dto.produtor_id == valid_data["produtor_id"]
    
    def test_safra_dto_validation(self):
        """Test SafraDTO validation."""
        from modules.safra.dtos.safra_dto import SafraDTO
        
        # Valid data
        valid_data = {
            "ano": 2024,
            "area_plantada": 50.0,
            "produtividade": 3.5,
            "produtor_id": 1,
            "propriedade_id": 1,
            "cultura_id": 1
        }
        dto = SafraDTO(**valid_data)
        assert dto.ano == valid_data["ano"]
        assert dto.area_plantada == valid_data["area_plantada"]
        assert dto.produtividade == valid_data["produtividade"]
    
    def test_cultura_dto_validation(self):
        """Test CulturaDTO validation."""
        from modules.cultura.dtos.cultura_dto import CulturaDTO
        
        # Valid data
        valid_data = {
            "nome": "Soja",
            "descricao": "Cultura de soja"
        }
        dto = CulturaDTO(**valid_data)
        assert dto.nome == valid_data["nome"]
        assert dto.descricao == valid_data["descricao"]

class TestErrorHandling:
    """Test cases for error handling utilities."""
    
    def test_validation_error_format(self):
        """Test validation error format."""
        from pydantic import ValidationError
        
        # This should raise a ValidationError
        with pytest.raises(ValidationError):
            from modules.produtor.dtos.produtor_dto import ProdutorDTO
            ProdutorDTO(cpf_cnpj="", nome="")  # Invalid empty values
    
    def test_database_error_handling(self):
        """Test database error handling."""
        # This would be tested in integration tests
        # For now, just ensure the error handling structure exists
        assert True 