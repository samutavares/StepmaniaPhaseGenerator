# 🎵 StepMania Phase Generator

Sistema inteligente de análise de performance e geração de charts adaptativos para StepMania, utilizando IA para criar versões personalizadas baseadas no desempenho do jogador.

## 🚀 Funcionalidades

- **Análise de Performance**: Extrai e analisa dados de replay do StepMania
- **Geração de Charts Adaptativos**: IA modifica charts baseado no desempenho observado
- **Suporte Multi-API**: DeepSeek, OpenAI GPT e Claude
- **Comparação de Charts**: Análise estatística detalhada entre versões
- **Configuração Segura**: Chaves de API protegidas via arquivo .env

## 📁 Estrutura do Projeto

```
Stepmania_Gen/
├── PlayerStats_Modular.py    # Sistema principal de análise
├── api_config.py             # Configurações de API
├── chart_extractor.py        # Manipulação de arquivos .sm
├── replay_extractor.py       # Análise de dados de replay
├── Comparativo.py            # Comparação de charts
├── .env                      # Chaves de API (não committar)
├── .gitignore               # Protege arquivos sensíveis
├── env_template.txt         # Template para configuração
└── SETUP_API_KEYS.md        # Guia de configuração
```

## 🛠️ Instalação e Configuração

### 1. Configurar Chaves de API
```bash
# Copiar template
cp env_template.txt .env

# Editar com suas chaves
# ACTIVE_API=deepseek
# DEEPSEEK_API_KEY=sk-sua-chave-aqui
# OPENAI_API_KEY=sk-sua-chave-aqui
# CLAUDE_API_KEY=sk-sua-chave-aqui
```

### 2. Verificar Configuração
```bash
python api_config.py
```

### 3. Executar Sistema Principal
```bash
python PlayerStats_Modular.py
```

## 🎯 Comandos Úteis

```bash
# Ver configuração atual
python PlayerStats_Modular.py config

# Trocar de API
python PlayerStats_Modular.py switch_api openai

# Trocar modelo
python PlayerStats_Modular.py switch_model gpt-4o

# Testar extração de chart
python PlayerStats_Modular.py test_extract

# Testar salvamento
python PlayerStats_Modular.py test_save
```

## 📊 Como Funciona

1. **Extração de Replay**: Sistema analisa dados de performance do jogador
2. **Análise de Performance**: Calcula acurácia por trilha e julgamentos
3. **Geração de Chart**: IA modifica chart original baseado no desempenho
4. **Comparação**: Estatísticas detalhadas entre versão original e modificada

## 🔧 Configurações

### APIs Suportadas
- **DeepSeek**: Modelos de chat e código
- **OpenAI**: GPT-4, GPT-5, GPT-4o
- **Claude**: Claude 3 Sonnet, Haiku, Opus

### Parâmetros Configuráveis
- Timeout da API
- Número máximo de tokens
- Temperature para geração
- Modelo específico por API

## 📈 Estatísticas Geradas

- **NPS (Notas por Segundo)**: Densidade temporal de notas
- **Acurácia por Trilha**: Performance em cada direção (←↓↑→)
- **Julgamentos**: Flawless, Perfect, Great, Good, Miss
- **Comparação**: Estatísticas entre chart original e modificado

---

## 📋 TBD - To Be Done

### 🔄 **1. Ajustar para as outras APIs (OPENAI e Claude)**
- [ ] Implementar suporte completo para OpenAI GPT
- [ ] Implementar suporte completo para Claude
- [ ] Testar compatibilidade de parâmetros entre APIs
- [ ] Ajustar formatação de prompts para cada API
- [ ] Validar respostas específicas de cada modelo

### 🎯 **2. Ajustar o prompt para dificultar mais**
- [ ] Modificar `PROMPT_INSTRUCTIONS` em `PlayerStats_Modular.py`
- [ ] Aumentar limites de dificuldade (atualmente +15% máximo)
- [ ] Adicionar opções de dificuldade configurável
- [ ] Implementar níveis de dificuldade (Fácil, Médio, Difícil, Expert)
- [ ] Ajustar regras pedagógicas para desafios maiores

### 🗄️ **3. Adicionar o histórico (Banco de dados) para uso no prompt**
- [ ] Implementar sistema de banco de dados (SQLite/PostgreSQL)
- [ ] Armazenar histórico de performances por usuário
- [ ] Salvar evolução de charts gerados
- [ ] Integrar histórico no prompt da IA
- [ ] Criar sistema de progressão baseado em histórico

### 📊 **4. Ajustar o Comparativo com mais estatísticas**
- [ ] Adicionar análise de padrões rítmicos
- [ ] Implementar métricas de complexidade
- [ ] Adicionar gráficos de distribuição de notas
- [ ] Incluir análise de transições entre trilhas
- [ ] Criar relatórios comparativos detalhados

### 👤 **5. Salvar o nome do usuário**
- [ ] Implementar sistema de identificação de usuário
- [ ] Salvar preferências por usuário
- [ ] Criar perfis de dificuldade personalizados
- [ ] Armazenar histórico individual
- [ ] Interface para gerenciar usuários

---

## 📝 Licença

Este projeto é desenvolvido para análise educacional e de performance no StepMania.

## 🔗 Links Úteis

- [StepMania](https://www.stepmania.com/)
- [Etterna](https://etternaonline.com/)
- [Documentação das APIs](SETUP_API_KEYS.md)

---

**Status**: 🚧 Em desenvolvimento ativo

*Última atualização: Agosto 2025*
