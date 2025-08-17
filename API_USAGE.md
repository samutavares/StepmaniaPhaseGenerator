# Guia de Uso da API - PlayerStats

## Visão Geral

O sistema PlayerStats foi atualizado com funcionalidades avançadas para gerenciar a API de IA, incluindo testes de conectividade, mudança de modelos e configurações flexíveis.

## Comandos Disponíveis

### 1. Testar Conectividade da API
```bash
python PlayerStats_Modular.py test_api
```
- Testa se a API está respondendo
- Verifica conectividade básica
- Testa a API real com uma requisição simples

### 2. Mostrar Configurações Atuais
```bash
python PlayerStats_Modular.py config
```
- Exibe todas as configurações da API
- Mostra modelos disponíveis
- Indica qual modelo está ativo

### 3. Alterar Modelo da API
```bash
python PlayerStats_Modular.py switch_model <nome_do_modelo>
```
Exemplos:
```bash
python PlayerStats_Modular.py switch_model deepseek-coder
python PlayerStats_Modular.py switch_model deepseek-math
```

### 4. Executar Sistema Completo
```bash
python PlayerStats_Modular.py
```
- Executa o pipeline completo de análise
- Usa o arquivo `generated_chart.sm` existente para teste
- Gera chart modificado

### 5. Testes Específicos
```bash
python PlayerStats_Modular.py test          # Testa extração da IA
python PlayerStats_Modular.py test_save     # Testa salvamento de chart
python PlayerStats_Modular.py clean         # Limpa e regenera
```

## Configuração da API

### Arquivo de Configuração (`api_config.py`)

O arquivo `api_config.py` contém todas as configurações da API:

```python
API_CONFIG = {
    "url": "https://api.deepseek.com/v1/chat/completions",
    "key": "sua_chave_aqui",
    "model": "deepseek-chat",
    "timeout": 60,
    "max_tokens": 4000,
    "temperature": 0.7
}
```

### Variáveis de Ambiente

Você pode configurar a API usando variáveis de ambiente:

```bash
# Windows (PowerShell)
$env:DEEPSEEK_API_KEY="sua_chave_aqui"
$env:DEEPSEEK_MODEL="deepseek-coder"

# Windows (CMD)
set DEEPSEEK_API_KEY=sua_chave_aqui
set DEEPSEEK_MODEL=deepseek-coder

# Linux/Mac
export DEEPSEEK_API_KEY="sua_chave_aqui"
export DEEPSEEK_MODEL="deepseek-coder"
```

## Modelos Disponíveis

- **deepseek-chat**: Modelo de chat geral (padrão)
- **deepseek-coder**: Modelo especializado em código
- **deepseek-math**: Modelo especializado em matemática

## Solução de Problemas

### 1. API não responde
```bash
python PlayerStats_Modular.py test_api
```
- Verifica conectividade
- Testa a API real
- Mostra erros específicos

### 2. Timeout na API
- Aumente o valor de `timeout` no `api_config.py`
- Verifique sua conexão com a internet
- Considere usar um modelo mais rápido

### 3. Erro de autenticação
- Verifique se a API key está correta
- Use variáveis de ambiente para maior segurança
- Teste a key diretamente na documentação da API

### 4. Modelo não encontrado
```bash
python PlayerStats_Modular.py config
```
- Verifica modelos disponíveis
- Confirma qual modelo está ativo

## Exemplos de Uso

### Fluxo Completo de Teste
```bash
# 1. Verificar configurações
python PlayerStats_Modular.py config

# 2. Testar conectividade
python PlayerStats_Modular.py test_api

# 3. Alterar modelo se necessário
python PlayerStats_Modular.py switch_model deepseek-coder

# 4. Executar sistema
python PlayerStats_Modular.py
```

### Configuração Personalizada
```python
# No arquivo api_config.py
API_CONFIG = {
    "url": "https://api.deepseek.com/v1/chat/completions",
    "key": "sua_chave_personalizada",
    "model": "deepseek-coder",
    "timeout": 120,  # 2 minutos
    "max_tokens": 8000,  # Mais tokens
    "temperature": 0.5  # Menos criativo
}
```

## Segurança

- **Nunca** commite sua API key no Git
- Use variáveis de ambiente para produção
- Considere usar um arquivo `.env` (não incluído no controle de versão)
- Rotacione suas chaves regularmente

## Suporte

Se encontrar problemas:
1. Execute `python PlayerStats_Modular.py test_api`
2. Verifique as configurações com `python PlayerStats_Modular.py config`
3. Teste com diferentes modelos
4. Verifique a documentação da API DeepSeek
