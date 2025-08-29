#!/usr/bin/env python3
"""
Arquivo de teste para demonstrar as novas funcionalidades implementadas:
1. Criação de pasta para respostas da AI
2. Renomeação de arquivos de replay
"""

import os
import sys
from datetime import datetime
import getpass

# Adiciona o diretório atual ao path para importar as funções
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa as funções do PlayerStats.py
from PlayerStats import (
    get_username, 
    create_ai_responses_folder, 
    save_ai_response, 
    rename_latest_replay_file
)

def test_username():
    """Testa a função de obter nome do usuário"""
    print("=== Teste: Obter nome do usuário ===")
    username = get_username()
    print(f"Nome do usuário: {username}")
    print()

def test_create_ai_folder():
    """Testa a criação da pasta para respostas da AI"""
    print("=== Teste: Criar pasta para respostas da AI ===")
    folder_path = create_ai_responses_folder()
    print(f"Pasta criada: {folder_path}")
    print(f"Pasta existe: {os.path.exists(folder_path)}")
    print()

def test_save_ai_response():
    """Testa o salvamento de resposta da AI"""
    print("=== Teste: Salvar resposta da AI ===")
    folder_path = create_ai_responses_folder()
    
    # Simula uma resposta da AI
    ai_response = f"""
Resposta simulada da AI
Timestamp: {datetime.now()}
Modelo: deepseek-chat
Conteúdo: Esta é uma resposta de teste da API da AI.
"""
    
    file_path = save_ai_response(ai_response, folder_path)
    print(f"Arquivo salvo: {file_path}")
    print(f"Arquivo existe: {os.path.exists(file_path)}")
    print()

def test_rename_replay():
    """Testa a renomeação de arquivo de replay"""
    print("=== Teste: Renomear arquivo de replay ===")
    try:
        renamed_file = rename_latest_replay_file()
        if renamed_file:
            print(f"Arquivo renomeado: {renamed_file}")
        else:
            print("Nenhum arquivo de replay encontrado para renomear")
    except Exception as e:
        print(f"Erro ao renomear: {e}")
    print()

def main():
    """Função principal para executar todos os testes"""
    print("Iniciando testes das novas funcionalidades...")
    print("=" * 50)
    print()
    
    test_username()
    test_create_ai_folder()
    test_save_ai_response()
    test_rename_replay()
    
    print("=" * 50)
    print("Testes concluídos!")

if __name__ == "__main__":
    main()
