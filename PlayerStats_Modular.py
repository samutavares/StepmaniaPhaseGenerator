"""
PlayerStats - Sistema de Análise de Performance do StepMania

Este é o módulo principal que coordena a análise de performance do jogador
e gera charts modificados para facilitar o aprendizado.

Modules:
    - replay_extractor: Funções para extrair e analisar dados de replay
    - chart_extractor: Funções para manipular arquivos de chart (.sm)

Author: Generated for StepMania Analysis
"""

# import matplotlib.pyplot as plt
import pandas as pd
import json
import requests
import os

# Importa nossos módulos customizados
from replay_extractor import (
    get_latest_replay_data, 
    parse_replay_data, 
    analyze_performance
)
from chart_extractor import (
    parse_sm_difficulties,
    choose_difficulty,
    extract_chart_data,
    count_steps_by_track,
    save_modified_chart,
    read_file_with_encoding
)


# ======= CONFIGURAÇÕES - MODIFIQUE AQUI =======
SONG_FOLDER = r"C:\Games\Etterna\Songs\The Time (Dirty Bit)"
SM_FILENAME = "Stepchart.sm"
REPLAYS_DIR = r"C:\Games\Etterna\Save\ReplaysV2"

# Configuração da dificuldade (deixe vazio para escolher interativamente)
TARGET_DIFFICULTY = "Beginner"  # Ex: "Hard", "Medium", "Easy", "Beginner" ou deixe vazio para escolher

SM_FILE_PATH = os.path.join(SONG_FOLDER, SM_FILENAME)

# ======= CONFIGURAÇÃO DA API =======
FORCE_API_CALL = True  # Mude para False para usar arquivo local
# ===============================================

# ======= CONFIGURAÇÕES DA API =======
# Importa configurações do arquivo separado
try:
    from api_config import (
        API_CONFIG, 
        get_available_models, 
        get_active_api, 
        get_available_apis,
        set_active_api,
        set_model,
        show_config as show_api_config_detailed
    )
except ImportError:
    # Fallback se o arquivo não existir
    API_CONFIG = {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "key": "sk-8dd8d4577b9946029a85332e82e841b3",
        "model": "deepseek-chat",
        "timeout": 300,  # 5 minutos para dar tempo da API processar
        "max_tokens": 4000,
        "temperature": 0.7
    }
    print("⚠️ Arquivo api_config.py não encontrado, usando configurações padrão")
    
    # Funções fallback
    def get_available_models():
        return {"deepseek-chat": "Modelo padrão"}
    def get_active_api():
        return "deepseek"
    def get_available_apis():
        return ["deepseek"]
    def set_active_api(api_name):
        print(f"⚠️ Função não disponível sem api_config.py")
        return False
    def set_model(model_name):
        print(f"⚠️ Função não disponível sem api_config.py")
        return False
    def show_api_config_detailed():
        print("⚠️ Função não disponível sem api_config.py")
# ===============================================

# ======= PROMPT PARA IA - MODIFICAR AQUI =======
PROMPT_INSTRUCTIONS = """Você é um assistente que modifica o chart de StepMania para facilitar o aprendizado do jogador \
a partir do desempenho observado.

Contexto:
- Você receberá:
  - original_sm_file: texto completo do arquivo .sm original.
  - stats: lista com estatísticas de performance por nota/trilha (tracks 0=←, 1=↓, 2=↑, 3=→) e julgamentos.
- O objetivo é gerar um novo "corpo de notas" (apenas a parte de notas) da mesma música e duração, adequado ao nível \
do jogador.

Regras pedagógicas (use a taxa de acerto geral e por trilha):
- Se a acurácia geral > 85%: aumente levemente a dificuldade (no máximo +15% de densidade), priorizando padrões \
coerentes do estilo original.
- Se a acurácia geral ≤ 85%: reduza a dificuldade (até −20% de densidade), limpando trêmulos longos, alternâncias \
rápidas e repetições cansativas.
- Adapte por trilha: onde a acurácia estiver pior, reduza uso dessa trilha; onde estiver melhor, permita um pouco \
mais de incidência.
- Distribua as mudanças ao longo de toda a música (evite concentrar tudo no início ou fim).
- Preserve o "feeling" rítmico e os acentos principais da música.

Restrições técnicas (obrigatórias):
- NÃO altere BPM, OFFSET, STOPS, metadata, títulos, nem estruturas fora do corpo de notas.
- Mantenha o número de medidas e a duração total.
- Saída deve conter SOMENTE o corpo das notas, com este formato:
  - Linhas de 4 caracteres contendo apenas 0 ou 1 (ex.: 0000, 0101, 1000).
  - Vírgula (,) como separador de medida.
  - Ponto e vírgula (;) no final do chart.
- Evite jacks longos e streams excessivos em níveis fáceis; introduza variação simples e segura.

Estilo de modificação:
- Em facilitação: aumente espaçamentos entre notas, limpe padrões muito rápidos, mantenha combinações simples e \
repetíveis.
- Em dificuldade: introduza variações moderadas (ex.: alternâncias controladas), mantendo legibilidade e coerência \
musical.

Importante:
- Use o padrão rítmico do original como referência; ajuste densidade sem "desalfinar" o groove.
- Garanta consistência de medidas: se o original tem N medidas, a saída também deve ter N medidas.
- Não inclua explicações dentro do bloco de código; apenas as notas.

Saída:
- Retorne somente UM bloco de código com o corpo de notas, nada além disso dentro do bloco:
```
0000
0010
...
,
...
;
```
- Fora do bloco você pode listar 3–5 mudanças principais (opcional), mas o bloco deve vir primeiro."""
# ===============================================


def create_performance_visualization(df: pd.DataFrame) -> None:
    """
    Cria visualização gráfica da performance do jogador.
    
    Args:
        df (pd.DataFrame): DataFrame com dados de performance processados
        
    Returns:
        None: Exibe o gráfico diretamente
        
    Example:
        >>> create_performance_visualization(performance_df)
        # Exibe gráfico de dispersão dos offsets
    """
    # Comentado para evitar bloqueio da interface gráfica
    # plt.figure(figsize=(10, 6))
    # plt.scatter(df["row"], df["offset"], c="blue", alpha=0.7)
    # plt.axhline(0, color='gray', linestyle='--')
    # plt.title("Dispersão de Offsets por Nota")
    # plt.xlabel("Row (posição na música)")
    # plt.ylabel("Offset (s)")
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()
    
    print("📊 Visualização gráfica desabilitada para execução em terminal")
    print(f"   Total de notas analisadas: {len(df)}")
    print(f"   Média de offset: {df['offset'].mean():.3f}s")
    print(f"   Desvio padrão: {df['offset'].std():.3f}s")


def generate_performance_report(performance_stats: pd.DataFrame, step_counts: dict) -> None:
    """
    Gera relatório detalhado de performance do jogador.
    
    Args:
        performance_stats (pd.DataFrame): Estatísticas de performance por track
        step_counts (dict): Contagem de passos por track no chart
        
    Returns:
        None: Imprime o relatório no console
        
    Example:
        >>> generate_performance_report(stats_df, {0: 10, 1: 12, 2: 8, 3: 15})
        # Imprime relatório detalhado
    """
    track_names = {
        0: "Seta Esquerda",
        1: "Seta Baixo",
        2: "Seta Cima",
        3: "Seta Direita"
    }
    
    # Cria DataFrame com contagem de passos no chart
    df_steps = pd.DataFrame([
        {"track": t, "track_name": track_names[t], "steps_in_chart": c}
        for t, c in step_counts.items()
    ])
    
    # Junta com estatísticas de acertos por track
    df_totals_acertos = performance_stats.groupby(['track', 'track_name'])['count'].sum().reset_index(name='total_acertos')
    df_relatorio = df_steps.merge(df_totals_acertos, on=['track', 'track_name'], how='left')
    
    print("=== RELATÓRIO DE PERFORMANCE ===")
    print("\nPassos no chart e total de acertos por track:")
    print(df_relatorio)
    
    print("\nDetalhes por julgamento:")
    print(performance_stats.sort_values(['track', 'judgment']))


def call_ai_for_chart_improvement(chart_data: str, performance_stats: pd.DataFrame) -> str:
    """
    Chama API de IA para gerar versão melhorada do chart baseado na performance.
    
    Args:
        chart_data (str): Dados do chart original
        performance_stats (pd.DataFrame): Estatísticas de performance do jogador
        
    Returns:
        str: Resposta completa da IA com análise e chart modificado
        
    Raises:
        requests.RequestException: Se houver erro na chamada da API
        
    Example:
        >>> response = call_ai_for_chart_improvement(chart, stats)
        >>> print("IA respondeu com sucesso")
    """
    stats_dict = performance_stats.to_dict(orient="records")
    
    # Usa configurações globais da API
    API_URL = API_CONFIG["url"]
    API_KEY = API_CONFIG["key"]
    MODEL = API_CONFIG["model"]
    TIMEOUT = API_CONFIG["timeout"]
    TEMPERATURE = API_CONFIG["temperature"]
    
    # Determina o parâmetro correto para tokens baseado na API ativa
    try:
        active_api = get_active_api()
        if active_api == "openai":
            MAX_TOKENS = API_CONFIG.get("max_completion_tokens", 4000)
            tokens_param = "max_completion_tokens"
        else:
            MAX_TOKENS = API_CONFIG.get("max_tokens", 4000)
            tokens_param = "max_tokens"
    except:
        # Fallback se não conseguir determinar a API
        MAX_TOKENS = API_CONFIG.get("max_tokens", API_CONFIG.get("max_completion_tokens", 4000))
        tokens_param = "max_tokens"
    
    # Dados para enviar para a IA
    data = {
        "original_sm_file": chart_data,
        "stats": stats_dict,
        "instructions": PROMPT_INSTRUCTIONS
    }
    
    data_json = json.dumps(data, indent=2)
    
    print("🚀 Enviando dados para IA...")
    print(f"📊 Tamanho dos dados: {len(data_json)} caracteres")
    print(f"🔗 API URL: {API_URL}")
    print(f"🤖 Modelo: {MODEL}")
    print(f"⏱️ Timeout: {TIMEOUT}s")
    print(f"📝 Max Tokens: {MAX_TOKENS}")
    print(f"🌡️ Temperature: {TEMPERATURE}")
    
    try:
        print("📡 Iniciando requisição POST...")
        
        # Prepara payload da requisição
        request_payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": data_json}]
        }
        
        # Adiciona parâmetro de tokens correto baseado na API
        request_payload[tokens_param] = MAX_TOKENS
        
        # Adiciona temperature apenas para modelos que suportam
        if active_api == "openai" and MODEL == "gpt-5":
            # GPT-5 só suporta temperature = 1 (padrão)
            print("⚠️ GPT-5 usa temperature padrão (1.0)")
        else:
            request_payload["temperature"] = TEMPERATURE
        
        # Faz a requisição com timeout
        response = requests.post(
            API_URL,
            json=request_payload,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=TIMEOUT
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        # Verifica se a resposta foi bem-sucedida
        if response.status_code == 200:
            print("✅ Resposta 200 recebida, processando...")
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                content = response_data["choices"][0]["message"]["content"]
                print(f"✅ Resposta da IA recebida: {len(content)} caracteres")
                return content
            else:
                print("⚠️ Resposta da IA não contém choices válidos")
                print(f"📄 Resposta completa: {response_data}")
                raise requests.RequestException("Resposta da IA inválida")
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"📄 Resposta de erro: {response.text}")
            raise requests.RequestException(f"API Error {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout na requisição da API")
        raise requests.RequestException("Timeout na requisição da API")
    except requests.exceptions.SSLError as e:
        print(f"🔒 Erro SSL: {e}")
        raise requests.RequestException(f"Erro SSL: {e}")
    except requests.exceptions.ConnectionError:
        print("🌐 Erro de conexão com a API")
        raise requests.RequestException("Erro de conexão com a API")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        raise
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        raise requests.RequestException(f"Erro inesperado: {e}")


def test_api_connectivity():
    """
    Testa a conectividade com a API da IA.
    
    Returns:
        bool: True se a API estiver funcionando, False caso contrário
    """
    print("🔍 Testando conectividade com a API...")
    
    try:
        # Teste simples de conectividade
        response = requests.get(
            "https://httpbin.org/status/200",
            timeout=10
        )
        print("✅ Conectividade básica OK")
        
        # Teste da API real (sem enviar dados completos)
        test_response = requests.post(
            API_CONFIG["url"],
            json={
                "model": API_CONFIG["model"],
                "messages": [{"role": "user", "content": "Teste de conectividade"}],
                "max_tokens": 10
            },
            headers={
                "Authorization": f"Bearer {API_CONFIG['key']}",
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        if test_response.status_code == 200:
            print("✅ API da IA respondendo corretamente")
            return True
        else:
            print(f"⚠️ API da IA retornou status {test_response.status_code}")
            print(f"📄 Resposta: {test_response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout no teste de conectividade")
        return False
    except requests.exceptions.ConnectionError:
        print("🌐 Erro de conexão no teste")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado no teste: {e}")
        return False


def show_api_config():
    """
    Mostra as configurações atuais da API.
    """
    # Usa a função detalhada do api_config se disponível
    try:
        show_api_config_detailed()
    except:
        # Fallback para versão simples
        print("=== CONFIGURAÇÕES ATUAIS DA API ===")
        print(f"🔗 URL: {API_CONFIG['url']}")
        print(f"🔑 API Key: {API_CONFIG['key'][:10]}...{API_CONFIG['key'][-4:]}")
        print(f"🤖 Modelo: {API_CONFIG['model']}")
        print(f"⏱️ Timeout: {API_CONFIG['timeout']}s")
        print(f"📝 Max Tokens: {API_CONFIG['max_tokens']}")
        print(f"🌡️ Temperature: {API_CONFIG['temperature']}")
    
    # Mostra configuração de execução
    print(f"\n⚙️ CONFIGURAÇÃO DE EXECUÇÃO:")
    print(f"   API Forçada: {'✅ SIM' if FORCE_API_CALL else '❌ NÃO'}")
    print(f"   Modo: {'🚀 API' if FORCE_API_CALL else '📁 Arquivo Local'}")


def switch_api_model(new_model: str):
    """
    Altera o modelo da API para teste.
    
    Args:
        new_model (str): Nome do novo modelo
        
    Example:
        >>> switch_api_model("deepseek-coder")
        # Altera para o modelo deepseek-coder
    """
    global API_CONFIG
    old_model = API_CONFIG["model"]
    API_CONFIG["model"] = new_model
    print(f"🔄 Modelo alterado: {old_model} → {new_model}")


def extract_chart_from_ai_response(full_response: str) -> str:
    """
    Extrai conteúdo do chart da resposta da IA.
    
    Args:
        full_response (str): Resposta completa da IA
        
    Returns:
        str: Conteúdo do chart extraído
        
    Example:
        >>> chart = extract_chart_from_ai_response(ai_response)
        >>> print(f"Chart extraído: {len(chart)} caracteres")
    """
    print(f"🔍 Analisando resposta da IA ({len(full_response)} caracteres)...")
    
    if not full_response or len(full_response.strip()) == 0:
        print("❌ Resposta vazia da IA")
        return ""
    
    chart_content = ""
    
    # Método 1: Procurar por blocos de código markdown
    if "```" in full_response:
        print("📋 Detectados blocos de código markdown")
        # Procura por todos os blocos de código
        blocks = []
        start_pos = 0
        while True:
            start_marker = full_response.find("```", start_pos)
            if start_marker == -1:
                break
            
            # Pula o ``` e possível linguagem (ex: ```sm)
            content_start = full_response.find("\n", start_marker)
            if content_start == -1:
                content_start = start_marker + 3
            else:
                content_start += 1
                
            end_marker = full_response.find("```", content_start)
            if end_marker == -1:
                break
                
            block_content = full_response[content_start:end_marker].strip()
            blocks.append(block_content)
            start_pos = end_marker + 3
        
        print(f"📦 Encontrados {len(blocks)} blocos de código")
        
        # Analisa cada bloco para encontrar o chart
        for i, block in enumerate(blocks):
            lines = block.split('\n')
            note_lines = [line for line in lines if len(line.strip()) == 4 and all(c in '01234' for c in line.strip())]
            separators = [line for line in lines if line.strip() in [',', ';']]
            
            print(f"   Bloco {i+1}: {len(note_lines)} linhas de notas, {len(separators)} separadores")
            
            if len(note_lines) > 10 and len(separators) > 0:  # Parece ser um chart
                chart_content = block
                print(f"✅ Chart encontrado no bloco {i+1}")
                break
    
    # Método 2: Procurar por padrões de chart sem markdown
    if not chart_content:
        print("🔍 Procurando padrões de chart sem markdown...")
        lines = full_response.split('\n')
        chart_lines = []
        in_chart_section = False
        
        for line in lines:
            line_clean = line.strip()
            
            # Detecta início de seção de chart
            if len(line_clean) == 4 and all(c in '01234' for c in line_clean):
                in_chart_section = True
                chart_lines.append(line_clean)
            elif line_clean in [',', ';'] and in_chart_section:
                chart_lines.append(line_clean)
                if line_clean == ';':  # Fim do chart
                    break
            elif in_chart_section and line_clean == '':
                continue  # Ignora linhas vazias dentro do chart
            elif in_chart_section and line_clean:
                # Se encontrou texto que não é chart, pode ter terminado
                if len(chart_lines) > 10:  # Se já tem bastante conteúdo, para
                    break
        
        if chart_lines:
            chart_content = '\n'.join(chart_lines)
            print(f"✅ Chart encontrado por padrão: {len(chart_lines)} linhas")
    
    # Método 3: Procurar qualquer sequência que pareça um chart
    if not chart_content:
        print("🔍 Busca avançada por sequências de chart...")
        import re
        
        # Procura por sequências de linhas que parecem chart data
        pattern = r'(?:^|\n)([01]{4}(?:\n[01]{4})*(?:\n,)*(?:\n[01]{4})*)*\n;'
        matches = re.findall(pattern, full_response, re.MULTILINE)
        
        if matches:
            # Pega a maior sequência encontrada
            chart_content = max(matches, key=len)
            print(f"✅ Chart encontrado por regex: {len(chart_content)} caracteres")
    
    if chart_content:
        # Valida e limpa o chart extraído
        lines = chart_content.split('\n')
        valid_lines = []
        for line in lines:
            line = line.strip()
            if line and ((len(line) == 4 and all(c in '01234' for c in line)) or line in [',', ';']):
                valid_lines.append(line)
        
        chart_content = '\n'.join(valid_lines)
        print(f"✅ Chart final: {len(valid_lines)} linhas válidas")
        
        # Mostra primeiras linhas para debug
        preview_lines = valid_lines[:5]
        print(f"📝 Preview: {preview_lines}")
    else:
        print("❌ Nenhum chart encontrado na resposta")
        print("📄 Início da resposta:")
        print(full_response[:500] + "..." if len(full_response) > 500 else full_response)
    
    return chart_content


def main():
    """
    Função principal que executa todo o pipeline de análise e geração de charts.
    
    Returns:
        None: Executa o processo completo
        
    Example:
        >>> main()
        # Executa análise completa e gera chart modificado
    """
    try:
        print("=== SISTEMA DE ANÁLISE DE PERFORMANCE DO STEPMANIA ===\n")
        
        # 1. Extrair dados de replay
        print("1. Extraindo dados de replay...")
        data_str = get_latest_replay_data(REPLAYS_DIR)
        if not data_str:
            print("Erro: Não foi possível carregar dados de replay")
            return
        
        # 2. Processar dados de replay
        print("2. Processando dados de replay...")
        df = parse_replay_data(data_str)
        analysis_results = analyze_performance(df)
        
        # 3. Criar visualização
        print("3. Criando visualização de performance...")
        create_performance_visualization(analysis_results['dataframe'])
        
        # 4. Extrair dados do chart
        print("4. Extraindo dados do chart...")
        chart_data, difficulty_name, difficulty_data = extract_chart_data(SM_FILE_PATH, TARGET_DIFFICULTY)
        if not chart_data:
            print("Erro: Não foi possível extrair dados do chart")
            return
        
        print(f"Chart extraído: {difficulty_name}")
        
        # 5. Analisar passos do chart
        step_counts = count_steps_by_track(chart_data)
        
        # 6. Gerar relatório
        print("5. Gerando relatório de performance...")
        generate_performance_report(analysis_results['performance_stats'], step_counts)
        
        # 7. Chamar IA para melhoria
        print("6. Chamando IA para análise e melhoria...")
        
        # VERIFICA SE DEVE USAR API OU ARQUIVO LOCAL
        if FORCE_API_CALL:
            print("🚀 FORÇANDO CHAMADA DA API...")
            print(f"🔧 Configuração atual: FORCE_API_CALL = {FORCE_API_CALL}")
            
            try:
                print("📡 Iniciando chamada da API...")
                ai_response = call_ai_for_chart_improvement(chart_data, analysis_results['performance_stats'])
                print("✅ Resposta da IA recebida com sucesso!")
                print(f"📊 Tamanho da resposta: {len(ai_response)} caracteres")
                
                # Salva a resposta da API para debug
                with open("api_response_debug.txt", "w", encoding="utf-8") as f:
                    f.write(ai_response)
                print("💾 Resposta da API salva em api_response_debug.txt")
                
            except Exception as e:
                print(f"❌ Erro ao chamar API: {e}")
                print("⚠️ Tentando usar arquivo local como fallback...")
                try:
                    with open("generated_chart.sm", "r", encoding="utf-8", errors="ignore") as f:
                        ai_response = f.read()
                    print("✅ Usando arquivo generated_chart.sm como fallback")
                except:
                    print("❌ Falha total: nem API nem arquivo local funcionaram")
                    return
        else:
            print("📁 Usando arquivo local (API desabilitada)...")
            try:
                with open("generated_chart.sm", "r", encoding="utf-8", errors="ignore") as f:
                    ai_response = f.read()
                print("✅ Usando arquivo generated_chart.sm")
            except:
                print("❌ Arquivo local não encontrado, tentando API...")
                try:
                    ai_response = call_ai_for_chart_improvement(chart_data, analysis_results['performance_stats'])
                    print("✅ Resposta da IA recebida com sucesso!")
                except Exception as e:
                    print(f"❌ Falha total: {e}")
                    return
        
        # 8. Extrair chart modificado
        print("7. Extraindo chart modificado...")
        print(f"📄 Tamanho da resposta da IA: {len(ai_response)} caracteres")
        
        # Salva a resposta completa para debug
        try:
            with open("debug_ai_response.txt", "w", encoding="utf-8") as f:
                f.write(ai_response)
            print("💾 Resposta completa salva em debug_ai_response.txt")
        except Exception as e:
            print(f"⚠️ Erro ao salvar debug: {e}")
        
        modified_chart = extract_chart_from_ai_response(ai_response)
        
        if modified_chart:
            print(f"✅ Chart extraído com sucesso! ({len(modified_chart)} caracteres)")
            
            # 9. Salvar chart modificado
            print("8. Salvando chart modificado...")
            original_content = read_file_with_encoding(SM_FILE_PATH)
            saved_path = save_modified_chart(
                SM_FILE_PATH, 
                modified_chart, 
                difficulty_name, 
                difficulty_data, 
                original_content
            )
            
            print(f"✅ Chart modificado salvo em: {saved_path}")
            print("\n=== PREVIEW DO CHART MODIFICADO ===")
            preview_lines = modified_chart.split('\n')[:10]
            for i, line in enumerate(preview_lines):
                print(f"   {i+1}: {line}")
            chart_lines = modified_chart.split('\n')
            if len(chart_lines) > 10:
                print(f"   ... e mais {len(chart_lines) - 10} linhas")
        else:
            print("❌ Não foi possível extrair o conteúdo do chart da resposta")
            print(f"📄 Primeiros 1000 caracteres da resposta:")
            print("=" * 50)
            print(ai_response[:1000])
            print("=" * 50)
            if len(ai_response) > 1000:
                print(f"... e mais {len(ai_response) - 1000} caracteres")
            
            print("\n💡 Possíveis causas:")
            print("   - IA não gerou chart em formato esperado")
            print("   - Resposta não contém blocos de código ```")
            print("   - Chart não está no formato de linhas 0000/0001/etc.")
            print("   - Verifique o arquivo debug_ai_response.txt para análise completa")
            
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()


def test_ai_extraction():
    """Testa a extração da resposta da IA usando o arquivo generated_chart.sm"""
    print("=== TESTE DE EXTRAÇÃO DA RESPOSTA DA IA ===")
    
    try:
        # Lê o arquivo de exemplo da resposta da IA
        with open("generated_chart.sm", "r", encoding="utf-8", errors="ignore") as f:
            ai_response = f.read()
        
        print(f"📄 Resposta da IA tem {len(ai_response)} caracteres")
        print(f"🔍 Contém '```': {'```' in ai_response}")
        
        # Testa a extração
        extracted_chart = extract_chart_from_ai_response(ai_response)
        
        print(f"\n📊 Chart extraído: {len(extracted_chart)} caracteres")
        
        if extracted_chart:
            print("✅ Extração funcionou!")
            print("🎵 Primeiras 10 linhas extraídas:")
            lines = extracted_chart.split('\n')[:10]
            for i, line in enumerate(lines):
                print(f"   {i+1}: '{line}'")
                
            # Conta diferentes tipos de linhas
            all_lines = extracted_chart.split('\n')
            note_lines = [line for line in all_lines if len(line) == 4 and all(c in '01' for c in line)]
            comma_lines = [line for line in all_lines if line.strip() == ',']
            semicolon_lines = [line for line in all_lines if line.strip() == ';']
            
            print(f"\n📈 Estatísticas do chart extraído:")
            print(f"   Linhas de notas (0000, 0001, etc.): {len(note_lines)}")
            print(f"   Vírgulas (,): {len(comma_lines)}")
            print(f"   Ponto e vírgula (;): {len(semicolon_lines)}")
            print(f"   Total de linhas: {len(all_lines)}")
            
            return extracted_chart
            
        else:
            print("❌ Falha na extração!")
            print("📋 Primeira parte da resposta da IA:")
            print(ai_response[:500])
            return None
            
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return None

def test_section_detection():
    """Testa a detecção de seções no arquivo SM"""
    print("=== TESTE DE DETECÇÃO DE SEÇÕES ===")
    
    try:
        original_path = SM_FILE_PATH
        difficulties = parse_sm_difficulties(original_path)
        
        print(f"📁 Dificuldades encontradas: {len(difficulties)}")
        for name, data in difficulties.items():
            print(f"   {name}: {len(data.get('chart_data', ''))} chars de chart data")
            if 'raw_section' in data:
                print(f"      Raw section: {len(data['raw_section'])} chars")
                print(f"      Primeiros 150 chars: {data['raw_section'][:150]}")
                print()
        
        # Teste específico do Beginner
        chart_data, diff_name, difficulty_data = extract_chart_data(original_path, "Beginner")
        print(f"\n🎯 Teste específico do Beginner:")
        print(f"   Nome encontrado: {diff_name}")
        if difficulty_data:
            print(f"   Chart data: {len(difficulty_data.get('chart_data', ''))} chars")
            print(f"   Raw section: {len(difficulty_data.get('raw_section', ''))} chars")
            
            # Mostra como a seção seria substituída
            raw_section = difficulty_data.get('raw_section', '')
            if raw_section:
                original_content = read_file_with_encoding(original_path)
                section_start = original_content.find(raw_section)
                print(f"   Seção encontrada na posição: {section_start}")
                if section_start != -1:
                    print(f"   ✅ Seção localizável para substituição")
                else:
                    print(f"   ❌ Seção NÃO localizável - problema de matching!")
                    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def test_chart_saving():
    """Testa o salvamento do chart usando dados de exemplo"""
    print("\n=== TESTE DE SALVAMENTO DE CHART ===")
    
    # Primeiro testa a detecção de seções
    test_section_detection()
    
    # Primeiro extrai o chart modificado
    modified_chart = test_ai_extraction()
    
    if not modified_chart:
        print("❌ Não foi possível extrair chart para teste")
        return
    
    try:
        # Simula os parâmetros necessários
        original_path = SM_FILE_PATH
        difficulty_name = "Beginner"
        
        # Extrai dados da dificuldade original
        chart_data, diff_name, difficulty_data = extract_chart_data(original_path, "Beginner")
        original_content = read_file_with_encoding(original_path)
        
        print(f"\n🔧 Dados da dificuldade original:")
        print(f"   Nome: {diff_name}")
        print(f"   Dados disponíveis: {list(difficulty_data.keys()) if difficulty_data else 'None'}")
        
        # Testa o salvamento
        print(f"\n💾 Testando salvamento...")
        print(f"   Chart original: {len(chart_data)} caracteres")
        print(f"   Chart modificado: {len(modified_chart)} caracteres")
        
        # Cria um arquivo temporário para teste
        import tempfile
        import shutil
        
        # Cria cópia temporária
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, "test_chart.sm")
        shutil.copy2(original_path, temp_path)
        
        saved_path = save_modified_chart(
            temp_path, 
            modified_chart, 
            difficulty_name, 
            difficulty_data, 
            original_content
        )
        
        print(f"✅ Arquivo salvo em: {saved_path}")
        
        # Verifica se o arquivo foi realmente criado
        if os.path.exists(saved_path):
            print("✅ Arquivo criado com sucesso!")
            
            # Compara antes e depois
            from Similaridade import extract_chart_data_only, extract_difficulty_info
            
            # Original
            orig_data = extract_chart_data_only(temp_path)
            orig_info = extract_difficulty_info(temp_path)
            
            # Modificado  
            saved_data = extract_chart_data_only(saved_path)
            saved_info = extract_difficulty_info(saved_path)
            
            print(f"\n📊 COMPARAÇÃO:")
            print(f"   Original: {len(orig_info)} níveis")
            for i, info in enumerate(orig_info):
                print(f"      Nível {i}: {info['difficulty']} - {len(orig_data[i]) if i < len(orig_data) else 0} linhas")
                
            print(f"   Modificado: {len(saved_info)} níveis")  
            for i, info in enumerate(saved_info):
                print(f"      Nível {i}: {info['difficulty']} - {len(saved_data[i]) if i < len(saved_data) else 0} linhas")
            
        else:
            print("❌ Arquivo não foi criado!")
            
    except Exception as e:
        print(f"❌ Erro durante teste de salvamento: {e}")
        import traceback
        traceback.print_exc()

def test_chart_extraction():
    """Testa a extração de chart de diferentes formatos de resposta"""
    print("=== TESTE DE EXTRAÇÃO DE CHART ===")
    
    # Teste 1: Formato markdown
    test1 = """Análise do desempenho: O jogador teve boa performance.

Aqui está o chart modificado:

```
0000
0010
0000
0001
,
0000
1000
0100
0000
,
0010
0000
0001
0000
;
```

As principais mudanças foram: redução de densidade."""
    
    print("\n📋 Teste 1: Formato markdown")
    result1 = extract_chart_from_ai_response(test1)
    print(f"Resultado: {'✅ Sucesso' if result1 else '❌ Falha'}")
    
    # Teste 2: Formato sem markdown
    test2 = """O jogador precisa de um chart mais fácil.

0000
0010
0000
0001
,
0000
1000
0100
0000
;

Essas mudanças devem ajudar."""
    
    print("\n📋 Teste 2: Formato sem markdown")
    result2 = extract_chart_from_ai_response(test2)
    print(f"Resultado: {'✅ Sucesso' if result2 else '❌ Falha'}")
    
    # Teste 3: Arquivo de debug se existir
    try:
        with open("debug_ai_response.txt", "r", encoding="utf-8") as f:
            debug_response = f.read()
        
        if debug_response.strip():
            print("\n📋 Teste 3: Resposta real da API (debug_ai_response.txt)")
            result3 = extract_chart_from_ai_response(debug_response)
            print(f"Resultado: {'✅ Sucesso' if result3 else '❌ Falha'}")
        else:
            print("\n⚠️ Arquivo debug_ai_response.txt está vazio")
    except FileNotFoundError:
        print("\n⚠️ Arquivo debug_ai_response.txt não encontrado")

def clean_and_regenerate():
    """Remove arquivos LearnMode antigos e regenera"""
    print("=== LIMPEZA E REGENERAÇÃO ===")
    
    # Remove arquivo antigo se existir
    song_dir = os.path.dirname(SM_FILE_PATH)
    for file in os.listdir(song_dir):
        if "_LearnMode.sm" in file:
            old_path = os.path.join(song_dir, file)
            try:
                os.remove(old_path)
                print(f"🗑️ Arquivo antigo removido: {file}")
            except Exception as e:
                print(f"⚠️ Não foi possível remover {file}: {e}")
    
    print("🔄 Executando sistema completo...")
    main()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_ai_extraction()
        elif sys.argv[1] == "test_save":
            test_chart_saving()
        elif sys.argv[1] == "clean":
            clean_and_regenerate()
        elif sys.argv[1] == "test_api":
            test_api_connectivity()
        elif sys.argv[1] == "test_extract":
            test_chart_extraction()
        elif sys.argv[1] == "config":
            show_api_config()
        elif sys.argv[1] == "switch_model":
            if len(sys.argv) > 2:
                if set_model(sys.argv[2]):
                    print("✅ Modelo alterado com sucesso!")
                else:
                    print("❌ Falha ao alterar modelo")
            else:
                print("❌ Uso: python PlayerStats_Modular.py switch_model <nome_do_modelo>")
                print("📋 Modelos disponíveis para API atual:")
                for model, desc in get_available_models().items():
                    print(f"   - {model}: {desc}")
        elif sys.argv[1] == "switch_api":
            if len(sys.argv) > 2:
                if set_active_api(sys.argv[2]):
                    print("✅ API alterada com sucesso!")
                    show_api_config()
                else:
                    print("❌ Falha ao alterar API")
            else:
                print("❌ Uso: python PlayerStats_Modular.py switch_api <nome_da_api>")
                print("📋 APIs disponíveis:")
                for api in get_available_apis():
                    status = "✅" if api == get_active_api() else "  "
                    print(f"   {status} {api}")
        elif sys.argv[1] == "force_api":
            # Modifica a variável global
            globals()['FORCE_API_CALL'] = True
            print("🚀 API forçada para execução!")
        elif sys.argv[1] == "use_local":
            # Modifica a variável global
            globals()['FORCE_API_CALL'] = False
            print("📁 Arquivo local forçado para execução!")
        else:
            main()
    else:
        main()


# Analisar como a IA está respondendo a natureza do aluno.
# Separar o delay do miss.
# Considerar se o deepseek reconhece os níveis da fase.
# Eseba 7 a 9 anos.
# Objetivo: 12 a 13 anos.
# Associação todas as idades.

#PROVAR O OBJETIVO DO TRABALHO.

#Estágio Docência: CNN e LSTM e LLM