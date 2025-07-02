#!/usr/bin/env python3
"""
Script para inicializar o banco de dados
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

def init_database():
    """Inicializa o banco de dados criando as tabelas necessárias"""
    try:
        # URL do banco de dados
        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/rural_db")
        
        # Cria o engine
        engine = create_engine(database_url)
        
        # Testa a conexão
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com o banco de dados estabelecida com sucesso!")
            
            # Verifica se as tabelas já existem
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            existing_tables = [row[0] for row in result]
            
            if existing_tables:
                print(f"📋 Tabelas existentes: {', '.join(existing_tables)}")
            else:
                print("📋 Nenhuma tabela encontrada. Execute as migrações se necessário.")
                
    except OperationalError as e:
        print(f"❌ Erro ao conectar com o banco de dados: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Inicializando banco de dados...")
    init_database()
    print("✅ Inicialização concluída!") 