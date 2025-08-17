# 🔐 Configuração de Chaves de API

Este guia explica como configurar as chaves de API de forma segura usando arquivos `.env`.

## 🚀 Configuração Rápida

### 1. Criar arquivo .env

```bash
# Copie o template
cp env_template.txt .env
```

### 2. Editar suas chaves

Abra o arquivo `.env` e substitua pelas suas chaves reais:

```env
# Escolha da API ativa
ACTIVE_API=deepseek

# Suas chaves reais (substitua os valores)
DEEPSEEK_API_KEY=sk-sua-chave-deepseek-aqui
OPENAI_API_KEY=sk-sua-chave-openai-aqui
CLAUDE_API_KEY=sk-sua-chave-claude-aqui
```

### 3. Verificar configuração

```bash
python api_config.py
```

## ⚠️ Segurança

- ✅ **Arquivo `.env` está no `.gitignore`** - nunca será commitado
- ✅ **Chaves removidas do código** - não há mais credenciais hardcodadas
- ✅ **Template público** - `env_template.txt` pode ser commitado sem riscos

## 🔧 Configurações Avançadas

Você pode personalizar outros parâmetros no `.env`:

```env
# Modelo específico para cada API
DEEPSEEK_MODEL=deepseek-coder
OPENAI_MODEL=gpt-4o
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Parâmetros gerais
API_TIMEOUT=300
API_MAX_TOKENS=4000
API_TEMPERATURE=0.7
```

## 🐍 Dependências Opcionais

Para carregamento automático melhorado do `.env`:

```bash
pip install python-dotenv
```

> **Nota**: Funciona sem python-dotenv também, usando apenas `os.getenv()`

## 🔍 Verificação de Status

O sistema automaticamente:
- ✅ Carrega variáveis do `.env` 
- ✅ Valida se as chaves são válidas
- ✅ Avisa se alguma configuração está faltando
- ✅ Fornece instruções se necessário

## 📁 Estrutura de Arquivos

```
projeto/
├── .env                # ❌ Suas chaves (não committar)
├── .gitignore          # ✅ Inclui .env
├── env_template.txt    # ✅ Template público
├── api_config.py       # ✅ Carrega do .env automaticamente
└── SETUP_API_KEYS.md   # ✅ Este guia
```

## 🛠️ Comandos Úteis

```bash
# Verificar configuração atual
python api_config.py

# Trocar de API
python PlayerStats_Modular.py switch_api openai

# Trocar modelo
python PlayerStats_Modular.py switch_model gpt-4o

# Ver configuração no sistema principal
python PlayerStats_Modular.py config
```

## ❓ Solução de Problemas

### Erro: "Nenhuma chave válida encontrada"
1. Verifique se o arquivo `.env` existe
2. Confirme se as chaves estão corretas
3. Execute `python api_config.py` para diagnosticar

### Erro: "API Key inválida"  
1. Verifique se a chave tem pelo menos 20 caracteres
2. Confirme se não há espaços extras
3. Teste a chave diretamente na API

### Arquivo .env não carregado
1. Verifique se está na raiz do projeto
2. Instale python-dotenv: `pip install python-dotenv`
3. Reinicie o programa

---

🎯 **Objetivo alcançado**: Chaves de API agora são carregadas de forma segura, sem exposição no código!
