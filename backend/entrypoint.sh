#!/bin/bash
set -e

# Aguarda o banco de dados ficar pronto
until nc -z db 5432; do
  echo "Aguardando o banco de dados..."; sleep 1;
done

# Cria as tabelas
python shared/database/init_db.py

# Inicia o servidor FastAPI
exec uvicorn main:app --host 0.0.0.0 --port 8000 