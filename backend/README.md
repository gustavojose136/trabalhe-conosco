# Sistema de Cadastro de Produtores Rurais

## Proposta
Aplicação para gerenciar o cadastro de produtores rurais, propriedades, safras e culturas, com dashboard de indicadores.

## Tecnologias
- Python 3.11+
- FastAPI
- PostgreSQL
- Docker
- SQLAlchemy
- Pydantic

## Estrutura de Pastas
```
back-end/
  src/
    modules/
      produtor/
        controllers/
        services/
        repositories/
        dtos/
        entities/
      propriedade/
        controllers/
        services/
        repositories/
        dtos/
        entities/
      safra/
        controllers/
        services/
        repositories/
        dtos/
        entities/
      cultura/
        controllers/
        services/
        repositories/
        dtos/
        entities/
      dashboard/
        controllers/
        services/
    shared/
      common/
      exceptions/
      utils/
      database/
  Dockerfile
  docker-compose.yml
  requirements.txt
  README.md
```

## Como rodar
Veja o docker-compose para rodar localmente.

## Documentação
Acesse `/docs` após subir o projeto para ver a documentação OpenAPI. 

# Aplicação de Gestão de Produtores Rurais - Backend

Sistema de gestão de produtores rurais desenvolvido com FastAPI, PostgreSQL e arquitetura em camadas.

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas bem definida:

```
src/
├── modules/           # Módulos da aplicação
│   ├── produtor/      # Gestão de produtores
│   ├── propriedade/   # Gestão de propriedades
│   ├── safra/         # Gestão de safras
│   ├── cultura/       # Gestão de culturas
│   └── dashboard/     # Dashboard e relatórios
├── shared/            # Código compartilhado
│   ├── database/      # Configuração do banco
│   ├── exceptions/    # Exceções customizadas
│   └── utils/         # Utilitários
└── tests/             # Testes unitários e de integração
```

## 🚀 Como Executar

### Pré-requisitos

- Docker e Docker Compose
- Python 3.8+
- PostgreSQL

### Execução com Docker (Recomendado)

1. **Clone o repositório e navegue até a pasta:**
```bash
cd app
```

2. **Execute com Docker Compose:**
```bash
docker-compose up --build
```

3. **Acesse a aplicação:**
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs

### Execução Local

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Configure as variáveis de ambiente:**
```bash
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/rural_db"
```

3. **Execute a aplicação:**
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 🧪 Testes

### Executando Testes

#### Testes Unitários e de Integração
```bash
# Todos os testes
python -m pytest tests/ -v

# Apenas testes unitários
python -m pytest tests/ -v -m "not integration"

# Apenas testes de integração
python -m pytest tests/ -v -m integration

# Testes com cobertura
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
```

#### Usando o Script de Testes
```bash
python scripts/run_tests.py
```

#### Testes com Docker
```bash
# Executar testes em container isolado
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

### Tipos de Testes

#### 1. Testes Unitários (`test_*.py`)
- **Localização**: `tests/`
- **Cobertura**: Camadas de serviço, repositórios e utilitários
- **Exemplos**:
  - Validação de CPF/CNPJ
  - Cálculos de área
  - Lógica de negócio dos serviços

#### 2. Testes de Integração (`test_integration.py`)
- **Localização**: `tests/test_integration.py`
- **Cobertura**: Fluxos completos da aplicação
- **Exemplos**:
  - CRUD completo de todas as entidades
  - Relacionamentos entre entidades
  - Dashboard e relatórios

#### 3. Testes End-to-End
- **Localização**: `tests/test_*.py` (métodos com `@pytest.mark.integration`)
- **Cobertura**: APIs REST completas
- **Exemplos**:
  - Criação de produtor → propriedade → safra
  - Validação de regras de negócio
  - Tratamento de erros

### Estrutura dos Testes

```
tests/
├── conftest.py              # Configuração e fixtures do pytest
├── test_produtor.py         # Testes do módulo produtor
├── test_propriedade.py      # Testes do módulo propriedade
├── test_safra.py           # Testes do módulo safra
├── test_cultura.py         # Testes do módulo cultura
├── test_dashboard.py       # Testes do módulo dashboard
├── test_integration.py     # Testes de integração end-to-end
└── test_utils.py           # Testes de utilitários
```

### Configuração de Testes

#### Banco de Dados de Teste
- **URL**: `postgresql+asyncpg://postgres:postgres@localhost:5432/test_rural_db`
- **Porta**: 5433 (para não conflitar com o banco principal)
- **Isolamento**: Cada teste roda em transação separada

#### Fixtures Disponíveis
- `client`: Cliente HTTP para testes de API
- `db_session`: Sessão do banco de dados
- `sample_produtor_data`: Dados de exemplo para produtores
- `sample_propriedade_data`: Dados de exemplo para propriedades

### Exemplo de Teste

```python
@pytest.mark.asyncio
async def test_create_produtor_success(client: AsyncClient, sample_produtor_data):
    """Test successful produtor creation."""
    response = await client.post("/produtores/", json=sample_produtor_data)
    assert response.status_code == 200
    data = response.json()
    assert data["cpf_cnpj"] == sample_produtor_data["cpf_cnpj"]
    assert data["nome"] == sample_produtor_data["nome"]
    assert "id" in data
```

## 📊 Cobertura de Testes

### Relatórios
- **Terminal**: `--cov-report=term-missing`
- **HTML**: `--cov-report=html` (gerado em `htmlcov/index.html`)
- **Mínimo**: 80% de cobertura obrigatória

### Métricas
- **Testes Unitários**: 90%+
- **Testes de Integração**: 85%+
- **Cobertura Total**: 80%+

## 🔧 Desenvolvimento

### Adicionando Novos Testes

1. **Teste Unitário**:
```python
def test_nova_funcionalidade():
    # Arrange
    # Act
    # Assert
    pass
```

2. **Teste de Integração**:
```python
@pytest.mark.asyncio
@pytest.mark.integration
async def test_nova_integracao(client: AsyncClient):
    # Teste completo da funcionalidade
    pass
```

3. **Teste End-to-End**:
```python
@pytest.mark.asyncio
async def test_fluxo_completo(client: AsyncClient):
    # Simula uso real da aplicação
    pass
```

### Boas Práticas

1. **Nomenclatura**: `test_<modulo>_<funcionalidade>`
2. **Organização**: Um arquivo por módulo
3. **Isolamento**: Cada teste deve ser independente
4. **Dados**: Usar fixtures para dados de teste
5. **Assertions**: Assertivas claras e específicas

## 🐛 Debugging de Testes

### Executar Teste Específico
```bash
python -m pytest tests/test_produtor.py::TestProdutorEndpoints::test_create_produtor_success -v -s
```

### Executar com Logs Detalhados
```bash
python -m pytest tests/ -v -s --log-cli-level=DEBUG
```

### Executar Testes Falhados
```bash
python -m pytest tests/ --lf -v
```

## 📈 Monitoramento

### Métricas de Qualidade
- **Cobertura de Código**: 80%+
- **Tempo de Execução**: < 30s para todos os testes
- **Taxa de Sucesso**: 100% em CI/CD

### Integração Contínua
- Testes executados automaticamente em cada commit
- Relatórios de cobertura enviados para o time
- Falhas bloqueiam merge de PRs

## 🚀 Próximos Passos

- [ ] Testes de performance
- [ ] Testes de segurança
- [ ] Testes de carga
- [ ] Automação de testes E2E
- [ ] Integração com ferramentas de qualidade de código 