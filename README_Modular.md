# Sistema de Análise de Performance do StepMania

Este sistema analisa a performance do jogador em arquivos de replay do Etterna/StepMania e gera versões modificadas dos charts para facilitar o aprendizado.

## 📁 Estrutura do Projeto

```
├── PlayerStats_Modular.py    # Arquivo principal
├── replay_extractor.py       # Módulo para extrair dados de replay
├── chart_extractor.py        # Módulo para manipular charts SM
└── README_Modular.md         # Este arquivo
```

## 🚀 Como Usar

### 1. Configuração

Edite as variáveis no início do `PlayerStats_Modular.py`:

```python
# ======= CONFIGURAÇÕES - MODIFIQUE AQUI =======
SONG_FOLDER = r"C:\Games\Etterna\Songs\Telephone"
SM_FILENAME = "Stepchart.sm"
REPLAYS_DIR = r"C:\Games\Etterna\Save\ReplaysV2"
TARGET_DIFFICULTY = "Beginner"  # ou deixe vazio para escolher interativamente
# ===============================================
```

### 2. Execução

```bash
python PlayerStats_Modular.py
```

### 3. Processo Automático

O sistema executará:

1. ✅ **Extração de Replay** - Pega o arquivo mais recente da pasta de replays
2. 📊 **Análise de Performance** - Calcula estatísticas de acertos/erros
3. 📈 **Visualização** - Gera gráfico de dispersão dos offsets
4. 🎵 **Extração de Chart** - Lê o arquivo SM e permite escolher dificuldade
5. 📋 **Relatório** - Mostra performance detalhada por track
6. 🤖 **IA Analysis** - Chama DeepSeek AI para analisar e melhorar o chart
7. 💾 **Salvamento** - Cria arquivo modificado na pasta original

## 📚 Módulos

### `replay_extractor.py`

**Funções principais:**
- `get_latest_replay_data()` - Extrai dados do replay mais recente
- `parse_replay_data()` - Converte dados brutos em DataFrame
- `classify_judgment()` - Classifica offsets em categorias (W1, W2, etc.)
- `analyze_performance()` - Gera estatísticas completas de performance

### `chart_extractor.py`

**Funções principais:**
- `parse_sm_difficulties()` - Extrai todas as dificuldades do arquivo SM
- `choose_difficulty()` - Interface para escolher dificuldade específica
- `read_file_with_encoding()` - Lê arquivos com múltiplos encodings
- `count_steps_by_track()` - Conta passos por track no chart
- `save_modified_chart()` - Salva versão modificada preservando metadados

### `PlayerStats_Modular.py`

**Arquivo principal que coordena:**
- Fluxo completo de análise
- Integração entre módulos
- Interface com API de IA
- Geração de relatórios e visualizações

## 🎯 Recursos

### ✨ **Multi-Dificuldade**
- Detecta automaticamente todas as dificuldades no arquivo SM
- Permite escolher qual dificuldade analisar/modificar
- Preserva outras dificuldades intactas

### 🌍 **Suporte a Encodings**
- Lê arquivos SM com caracteres especiais
- Suporta UTF-8, Latin-1, CP1252, ISO-8859-1

### 📊 **Análise Detalhada**
- Classifica timing em W1/W2/W3/W4/W5/Miss
- Analisa performance por track (setas)
- Gera visualizações gráficas

### 🤖 **IA Integrada**
- Análise inteligente da performance
- Sugestões personalizadas de melhoria
- Geração automática de charts adaptativos

### 💾 **Preservação de Dados**
- Mantém todos os metadados originais (BPMs, offset, etc.)
- Nomeia arquivos com dificuldade específica
- Preserva estrutura completa do arquivo SM

## 📋 Exemplo de Saída

```
=== SISTEMA DE ANÁLISE DE PERFORMANCE DO STEPMANIA ===

1. Extraindo dados de replay...
Replay carregado: C:\Games\Etterna\Save\ReplaysV2\latest.replay

2. Processando dados de replay...
Dados processados: 156 notas analisadas

3. Criando visualização de performance...
[Gráfico exibido]

4. Extraindo dados do chart...
Dificuldades disponíveis:
1. Hard
2. Medium
3. Easy
4. Beginner

Usando dificuldade especificada: Beginner
Chart extraído: Beginner

5. Gerando relatório de performance...
=== RELATÓRIO DE PERFORMANCE ===
[Tabelas detalhadas]

6. Chamando IA para análise e melhoria...
Enviando dados para IA...

7. Extraindo chart modificado...
8. Salvando chart modificado...
✅ Chart modificado salvo em: C:\Games\Etterna\Songs\Telephone\Stepchart_Beginner_LearnMode.sm
```

## 🔧 Dependências

```bash
pip install pandas matplotlib requests
```

## 🎵 Formatos Suportados

- **Arquivos SM**: StepMania/Etterna chart files
- **Replays**: Arquivos de replay do Etterna
- **Dificuldades**: Hard, Medium, Easy, Beginner, etc.
- **Encodings**: UTF-8, Latin-1, CP1252, ISO-8859-1

## 🚨 Troubleshooting

### Erro de Encoding
```
UnicodeDecodeError: 'utf-8' codec can't decode...
```
**Solução**: O sistema tenta automaticamente múltiplos encodings

### Dificuldade não encontrada
```
Difficulty 'Expert' not found
```
**Solução**: Verifique as dificuldades disponíveis ou deixe `TARGET_DIFFICULTY = ""`

### Arquivo SM não encontrado
```
FileNotFoundError: SM file not found
```
**Solução**: Verifique os caminhos em `SONG_FOLDER` e `SM_FILENAME`