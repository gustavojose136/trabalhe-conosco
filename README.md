# Sistema de Gestão de Produtores Rurais

Sistema completo para gestão de produtores rurais, propriedades, culturas e safras, desenvolvido com FastAPI (back-end) e Angular (front-end).

## 🚀 Tecnologias

- **Back-end**: FastAPI, SQLAlchemy, PostgreSQL
- **Front-end**: Angular 17, Bootstrap 5, Bootstrap Icons
- **Infraestrutura**: Docker, Docker Compose

## 📋 Pré-requisitos

- Docker
- Docker Compose

## 🏃‍♂️ Como executar

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd teste
```

### 2. Execute com Docker Compose
```bash
docker-compose up --build
```

### 3. Acesse a aplicação
- **Front-end**: http://localhost
- **Back-end API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

## 📁 Estrutura do Projeto

```
teste/
├── app/                    # Back-end FastAPI
│   ├── src/
│   │   ├── modules/        # Módulos da aplicação
│   │   └── shared/         # Utilitários compartilhados
│   ├── Dockerfile
│   └── docker-compose.yml
├── frontend/               # Front-end Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── features/   # Módulos das entidades
│   │   │   ├── core/       # Serviços e utilitários
│   │   │   └── shared/     # Componentes compartilhados
│   │   └── styles.scss
│   ├── Dockerfile
│   └── nginx.conf
└── docker-compose.yml      # Orquestração principal
```

## 🔧 Funcionalidades

### Back-end (FastAPI)
- ✅ CRUD completo para Produtores
- ✅ CRUD completo para Propriedades
- ✅ CRUD completo para Culturas
- ✅ CRUD completo para Safras
- ✅ Dashboard com estatísticas
- ✅ Validações de negócio (CPF/CNPJ, áreas)
- ✅ Banco de dados PostgreSQL

### Front-end (Angular)
- ✅ Interface responsiva com Bootstrap
- ✅ Navegação global com navbar
- ✅ Dashboard com métricas
- ✅ Formulários reativos com validação
- ✅ Tabelas com ordenação e filtros
- ✅ Ícones modernos com Bootstrap Icons

## 🛠️ Desenvolvimento

### Back-end
```bash
cd app
docker-compose up
```

### Front-end
```bash
cd frontend
npm install
npm start
```

## 📊 Endpoints da API

- `GET /produtores/` - Listar produtores
- `POST /produtores/` - Criar produtor
- `GET /propriedades/` - Listar propriedades
- `POST /propriedades/` - Criar propriedade
- `GET /culturas/` - Listar culturas
- `POST /culturas/` - Criar cultura
- `GET /safras/` - Listar safras
- `POST /safras/` - Criar safra
- `GET /dashboard/stats` - Estatísticas do dashboard

## 🐳 Docker

O projeto usa Docker Compose para orquestrar:
- **backend**: FastAPI na porta 8000
- **frontend**: Angular com Nginx na porta 80
- **db**: PostgreSQL na porta 5432

## 📝 Licença

Este projeto foi desenvolvido como parte de um desafio técnico.

## Como rodar o projeto (Docker Compose)

### Subir tudo (backend, frontend e banco de dados)

```sh
# Na raiz do projeto

docker-compose up -d
```

### Resetar o ambiente (apagar banco e dados)

```sh
docker-compose down -v
docker-compose up -d
```

### Build sem cache (garantir que tudo será reconstruído)

```sh
docker-compose build --no-cache
docker-compose up -d
```

## O que acontece automaticamente?
- O backend aguarda o banco de dados, cria as tabelas e popula com dados de exemplo automaticamente (via entrypoint.sh).
- Não é necessário rodar scripts manualmente.

## Acessando o sistema
- Frontend: http://localhost:4200
- Backend (API): http://localhost:8000/docs (Swagger)

## Observações
- Se precisar rodar o seed manualmente, use:
  ```sh
  docker-compose exec backend python shared/database/seed_data.py
  ```
- Para logs do backend:
  ```sh
  docker-compose logs backend
  ``` 