# 🐳 Docker Setup - Trabalhe Conosco

Este projeto está configurado para rodar com Docker Compose, incluindo backend Python (FastAPI), frontend Angular e banco de dados PostgreSQL.

## 📋 Pré-requisitos

- Docker
- Docker Compose

## 🚀 Como Executar

### Produção
```bash
# Construir e iniciar todos os serviços
docker-compose up --build

# Executar em background
docker-compose up -d --build
```

### Desenvolvimento
```bash
# Usar configuração de desenvolvimento com hot-reload
docker-compose -f docker-compose.dev.yml up --build
```

## 🌐 Acessos

- **Frontend (Produção)**: http://localhost:80
- **Frontend (Desenvolvimento)**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **Banco de Dados**: localhost:5432

## 📁 Estrutura dos Serviços

### Backend (Python/FastAPI)
- **Porta**: 8000
- **Framework**: FastAPI
- **Banco**: PostgreSQL
- **Hot-reload**: Disponível no modo desenvolvimento

### Frontend (Angular)
- **Porta**: 80 (produção) / 4200 (desenvolvimento)
- **Framework**: Angular 20
- **Proxy**: Configurado para redirecionar `/api/*` para o backend
- **Hot-reload**: Disponível no modo desenvolvimento

### Banco de Dados (PostgreSQL)
- **Porta**: 5432
- **Database**: rural_db
- **Usuário**: postgres
- **Senha**: postgres

## 🔧 Comandos Úteis

```bash
# Ver logs dos serviços
docker-compose logs -f [service_name]

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (cuidado: apaga dados do banco)
docker-compose down -v

# Reconstruir um serviço específico
docker-compose build [service_name]

# Executar comandos dentro de um container
docker-compose exec backend python -c "print('Hello from backend')"
docker-compose exec frontend npm install

# Ver status dos serviços
docker-compose ps
```

## 🐛 Troubleshooting

### Problemas Comuns

1. **Porta já em uso**
   ```bash
   # Verificar o que está usando a porta
   netstat -ano | findstr :8000
   # ou
   lsof -i :8000
   ```

2. **Erro de permissão no entrypoint.sh**
   ```bash
   # O arquivo já está configurado com permissões corretas no Dockerfile
   ```

3. **Banco de dados não conecta**
   ```bash
   # Aguardar alguns segundos para o PostgreSQL inicializar
   # Verificar logs do banco
   docker-compose logs db
   ```

4. **Frontend não carrega**
   ```bash
   # Verificar se o build foi bem-sucedido
   docker-compose logs frontend
   ```

## 🔄 Desenvolvimento

### Modo Desenvolvimento
O arquivo `docker-compose.dev.yml` oferece:
- Hot-reload para backend e frontend
- Volumes montados para edição em tempo real
- Porta 4200 para o frontend (padrão Angular)

### Estrutura de Arquivos
```
├── docker-compose.yml          # Produção
├── docker-compose.dev.yml      # Desenvolvimento
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── src/
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── nginx.conf
│   └── src/
└── .gitignore
```

## 📝 Notas Importantes

- O frontend usa Nginx em produção para servir os arquivos estáticos
- O proxy do Nginx redireciona `/api/*` para o backend
- O backend aguarda o banco de dados estar pronto antes de iniciar
- Todos os serviços estão na mesma rede Docker para comunicação interna 