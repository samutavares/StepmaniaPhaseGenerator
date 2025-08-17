# 🚀 Guia de APIs - PlayerStats

Sistema que permite alternar facilmente entre **DeepSeek** (padrão), **OpenAI (GPT)** e **Claude** para geração de charts.

> **💡 DeepSeek é a API padrão** - oferece boa qualidade com custo-benefício excelente!

## 🔧 **Como usar:**

### **1. Alternar API (3 métodos)**

#### **Método 1: Editar arquivo `api_config.py`**
```python
# Linha 13 do api_config.py
ACTIVE_API = "openai"    # Para usar GPT
ACTIVE_API = "deepseek"  # Para usar DeepSeek  
ACTIVE_API = "claude"    # Para usar Claude
```

#### **Método 2: Via linha de comando**
```bash
# Alterar para OpenAI (GPT)
python PlayerStats_Modular.py switch_api openai

# Alterar para DeepSeek
python PlayerStats_Modular.py switch_api deepseek

# Alterar para Claude
python PlayerStats_Modular.py switch_api claude
```

#### **Método 3: Via variável de ambiente**
```bash
# Windows
set ACTIVE_API=openai
python PlayerStats_Modular.py

# Linux/Mac
export ACTIVE_API=openai
python PlayerStats_Modular.py
```

### **2. Alterar modelo da API ativa**
```bash
# Ver modelos disponíveis
python PlayerStats_Modular.py switch_model

# Alterar modelo (exemplos)
python PlayerStats_Modular.py switch_model gpt-4o           # OpenAI
python PlayerStats_Modular.py switch_model deepseek-coder   # DeepSeek
python PlayerStats_Modular.py switch_model claude-3-5-sonnet-20241022  # Claude
```

### **3. Ver configuração atual**
```bash
python PlayerStats_Modular.py config
```

## 🔑 **Configuração de API Keys**

### **No arquivo `api_config.py`:**
- **DeepSeek**: Linha 19 - `"key": "sk-xxx..."`
- **OpenAI**: Linha 28 - `"key": "sk-proj-xxx..."`  
- **Claude**: Linha 37 - `"key": "sua_chave_claude_aqui"`

> **⚠️ Notas importantes**: 
> - OpenAI usa `max_completion_tokens` enquanto DeepSeek e Claude usam `max_tokens`. O sistema detecta automaticamente qual usar.
> - GPT-5 só suporta `temperature = 1.0` (padrão). O sistema ignora automaticamente o valor configurado para este modelo.

### **Via variáveis de ambiente (mais seguro):**
```bash
# Windows
set DEEPSEEK_API_KEY=sk-xxx...
set OPENAI_API_KEY=sk-proj-xxx...
set CLAUDE_API_KEY=sk-ant-xxx...

# Linux/Mac
export DEEPSEEK_API_KEY="sk-xxx..."
export OPENAI_API_KEY="sk-proj-xxx..."
export CLAUDE_API_KEY="sk-ant-xxx..."
```

## 📋 **Modelos disponíveis:**

### **🤖 DeepSeek:**
- `deepseek-chat` - Modelo de chat geral
- `deepseek-coder` - Especializado em código
- `deepseek-math` - Especializado em matemática

### **🧠 OpenAI (GPT):**
- `gpt-5` - GPT-5 (mais recente) ⚠️ *Só usa temperature padrão (1.0)*
- `gpt-4o` - GPT-4o 
- `gpt-4` - GPT-4 (modelo anterior)
- `gpt-3.5-turbo` - GPT-3.5 Turbo (mais rápido e barato)
- `gpt-4o-mini` - GPT-4o Mini 

### **🎭 Claude (Anthropic):**
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet (mais recente)
- `claude-3-sonnet-20240229` - Claude 3 Sonnet
- `claude-3-haiku-20240307` - Claude 3 Haiku (mais rápido)
- `claude-3-opus-20240229` - Claude 3 Opus (mais potente)

## 🎯 **Comandos úteis:**

```bash
# Ver todas as configurações
python PlayerStats_Modular.py config

# Testar conectividade
python PlayerStats_Modular.py test_api

# Listar APIs disponíveis
python PlayerStats_Modular.py switch_api

# Listar modelos da API atual
python PlayerStats_Modular.py switch_model

# Executar sistema com API ativa
python PlayerStats_Modular.py
```

## ⚡ **Exemplo prático:**

```bash
# 1. Alterar para GPT-4
python PlayerStats_Modular.py switch_api openai
python PlayerStats_Modular.py switch_model gpt-4o

# 2. Ver configuração
python PlayerStats_Modular.py config

# 3. Executar análise
python PlayerStats_Modular.py
```

## 🔄 **Alternar rapidamente:**

Para trocar rapidamente entre APIs, edite apenas a **linha 13** do `api_config.py`:

```python
ACTIVE_API = "deepseek"  # DeepSeek (PADRÃO - recomendado)
ACTIVE_API = "openai"    # OpenAI/GPT  
ACTIVE_API = "claude"    # Claude/Anthropic
```

Salve o arquivo e execute o sistema normalmente!
