#!/usr/bin/env python3
"""
Script para executar testes da aplicação.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Executa um comando e exibe o resultado."""
    print(f"\n{'='*50}")
    print(f"Executando: {description}")
    print(f"Comando: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Sucesso!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Erro!")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Função principal do script."""
    # Mudar para o diretório da aplicação
    app_dir = Path(__file__).parent.parent
    os.chdir(app_dir)
    
    print("🧪 Executando Testes da Aplicação Rural")
    print(f"Diretório: {app_dir}")
    
    # Verificar se estamos no ambiente correto
    if not Path("requirements.txt").exists():
        print("❌ Arquivo requirements.txt não encontrado!")
        sys.exit(1)
    
    # Instalar dependências de teste se necessário
    print("\n📦 Verificando dependências...")
    run_command("pip install -r requirements.txt", "Instalando dependências")
    
    # Executar testes unitários
    print("\n🔬 Executando testes unitários...")
    success = run_command(
        "python -m pytest tests/ -v -m 'not integration' --tb=short",
        "Testes unitários"
    )
    
    if not success:
        print("❌ Testes unitários falharam!")
        sys.exit(1)
    
    # Executar testes de integração
    print("\n🔗 Executando testes de integração...")
    success = run_command(
        "python -m pytest tests/ -v -m integration --tb=short",
        "Testes de integração"
    )
    
    if not success:
        print("❌ Testes de integração falharam!")
        sys.exit(1)
    
    # Executar testes com cobertura
    print("\n📊 Executando testes com cobertura...")
    success = run_command(
        "python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html",
        "Testes com cobertura"
    )
    
    if success:
        print("\n📈 Relatório de cobertura gerado em htmlcov/index.html")
    
    # Executar todos os testes
    print("\n🎯 Executando todos os testes...")
    success = run_command(
        "python -m pytest tests/ -v --tb=short",
        "Todos os testes"
    )
    
    if success:
        print("\n✅ Todos os testes passaram com sucesso!")
    else:
        print("\n❌ Alguns testes falharam!")
        sys.exit(1)

if __name__ == "__main__":
    main() 