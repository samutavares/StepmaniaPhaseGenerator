#!/usr/bin/env python3
"""
Teste de autenticação da API DeepSeek
"""

import requests
import json

def test_auth():
    """Testa diferentes cenários de autenticação"""
    
    print("🔐 Teste de autenticação da API DeepSeek...")
    
    # Teste 1: Sem autenticação
    try:
        print("\n1️⃣ Teste sem autenticação...")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 5
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.text[:200]}")
    except Exception as e:
        print(f"   Erro: {e}")
    
    # Teste 2: Com API key inválida
    try:
        print("\n2️⃣ Teste com API key inválida...")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 5
            },
            headers={
                "Authorization": "Bearer sk-invalid-key",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.text[:200]}")
    except Exception as e:
        print(f"   Erro: {e}")
    
    # Teste 3: Com API key real
    try:
        print("\n3️⃣ Teste com API key real...")
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": "Hi"}],
                "max_tokens": 5
            },
            headers={
                "Authorization": "Bearer sk-8dd8d4577b9946029a85332e82e841b3",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.text[:200]}")
        
        if response.status_code == 200:
            print("   ✅ API funcionando!")
        elif response.status_code == 401:
            print("   ❌ API key inválida ou expirada")
        elif response.status_code == 429:
            print("   ⚠️ Limite de requisições atingido")
        else:
            print(f"   ⚠️ Status inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"   Erro: {e}")

if __name__ == "__main__":
    test_auth()
