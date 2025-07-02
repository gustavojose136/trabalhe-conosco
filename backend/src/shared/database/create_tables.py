#!/usr/bin/env python3
"""
Script para criar as tabelas no banco de dados
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

def create_tables():
    """Cria as tabelas no banco de dados"""
    try:
        # URL do banco de dados
        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/rural_db")
        
        # Cria o engine
        engine = create_engine(database_url)
        
        # Testa a conexão
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com o banco de dados estabelecida com sucesso!")
            
            # Criar tabelas
            print("🏗️ Criando tabelas...")
            
            # Tabela produtores
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS produtores (
                    id SERIAL PRIMARY KEY,
                    cpf_cnpj VARCHAR(18) UNIQUE NOT NULL,
                    nome VARCHAR(100) NOT NULL
                )
            """))
            
            # Tabela propriedades
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS propriedades (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(200) UNIQUE NOT NULL,
                    estado VARCHAR(2) NOT NULL,
                    cidade VARCHAR(100) NOT NULL,
                    area_total DECIMAL(10,2) NOT NULL,
                    area_agricultavel DECIMAL(10,2) NOT NULL,
                    area_vegetacao DECIMAL(10,2) NOT NULL,
                    produtor_id INTEGER REFERENCES produtores(id)
                )
            """))
            
            # Tabela safras
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS safras (
                    id SERIAL PRIMARY KEY,
                    ano INTEGER NOT NULL,
                    descricao TEXT,
                    propriedade_id INTEGER REFERENCES propriedades(id)
                )
            """))
            
            # Tabela culturas
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS culturas (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) UNIQUE NOT NULL,
                    descricao TEXT,
                    safra_id INTEGER REFERENCES safras(id),
                    propriedade_id INTEGER REFERENCES propriedades(id)
                )
            """))
            
            conn.commit()
            print("✅ Tabelas criadas com sucesso!")
                
    except OperationalError as e:
        print(f"❌ Erro ao conectar com o banco de dados: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Criando tabelas no banco de dados...")
    create_tables()
    print("✅ Criação de tabelas concluída!") 