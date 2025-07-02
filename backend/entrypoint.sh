#!/bin/bash
set -e

until nc -z db 5432; do
  echo "Aguardando o banco de dados..."; sleep 1;
done

python shared/database/init_db.py

exec uvicorn main:app --host 0.0.0.0 --port 8000 