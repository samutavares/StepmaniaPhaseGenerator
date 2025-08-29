import matplotlib.pyplot as plt
import pandas as pd
import json
import requests 
import os
import glob
from pathlib import Path
from datetime import datetime
import getpass

# ======= CONFIGURAÇÕES - MODIFIQUE AQUI =======
SONG_FOLDER = r"C:\Games\Etterna\Songs\Loca"
SM_FILENAME = "Stepchart.sm"
REPLAYS_DIR = r"C:\Games\Etterna\Save\ReplaysV2"

# Configuração da dificuldade (deixe vazio para escolher interativamente)
TARGET_DIFFICULTY = "Beginner"  # Ex: "Hard", "Medium", "Easy", "Beginner" ou deixe vazio para escolher

# Configuração do nome do usuário
USERNAME = "Samuel"  # Modifique aqui para o nome desejado

SM_FILE_PATH = os.path.join(SONG_FOLDER, SM_FILENAME)
# ===============================================


def create_ai_responses_folder():
    """Cria pasta para salvar respostas da AI com nome do usuário, timestamp e modelo"""
    username = USERNAME
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ai_model = "deepseek-chat"  # Modelo usado na API
    
    folder_name = f"AI_Responses_{ai_model}"
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    # Cria a pasta se não existir
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Pasta criada: {folder_path}")
    
    return folder_path

def save_ai_response(response_content, folder_path):
    """Salva a resposta da AI em um arquivo na pasta criada"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ai_response_{timestamp}.txt"
    filepath = os.path.join(folder_path, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(response_content)
    
    print(f"Resposta da AI salva em: {filepath}")
    return filepath

def rename_latest_replay_file():
    """Renomeia o último arquivo de replay com nome do usuário e timestamp"""
    username = USERNAME
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Pega todos os arquivos da pasta
    all_files = glob.glob(os.path.join(REPLAYS_DIR, "*"))
    
    if not all_files:
        print("Nenhum arquivo de replay encontrado!")
        return None
    
    # Pega o arquivo mais recente
    latest_file = max(all_files, key=os.path.getctime)
    
    # Obtém a extensão do arquivo original
    file_ext = os.path.splitext(latest_file)[1]
    
    # Cria o novo nome do arquivo
    new_filename = f"{username}_{timestamp}{file_ext}"
    new_filepath = os.path.join(REPLAYS_DIR, new_filename)
    
    try:
        # Renomeia o arquivo
        os.rename(latest_file, new_filepath)
        print(f"Arquivo de replay renomeado: {os.path.basename(latest_file)} -> {new_filename}")
        return new_filepath
    except Exception as e:
        print(f"Erro ao renomear arquivo: {e}")
        return latest_file


def get_latest_replay_data():
    # Pega todos os arquivos da pasta
    all_files = glob.glob(os.path.join(REPLAYS_DIR, "*"))
    
    # Pega o arquivo mais recente
    latest_file = max(all_files, key=os.path.getctime)
    
    # Lê o arquivo
    with open(latest_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content

# Renomeia o último arquivo de replay antes de processá-lo
print("Renomeando arquivo de replay...")
renamed_replay_file = rename_latest_replay_file()

data_str = get_latest_replay_data()

# Debug: mostrar as primeiras linhas do arquivo para entender o formato
print("Primeiras linhas do arquivo de replay:")
print(data_str[:500])
print("=" * 50)

rows = []
for line_num, line in enumerate(data_str.strip().splitlines(), 1):
    try:
        parts = line.split()
        if len(parts) < 3:  # Precisa ter pelo menos 3 partes: row, offset, e pelo menos uma track
            print(f"Linha {line_num} ignorada - formato inválido: {line}")
            continue
            
        # Valida se a primeira parte é um número
        if not parts[0].replace('-', '').replace('.', '').isdigit():
            print(f"Linha {line_num} ignorada - row não é numérico: {parts[0]}")
            continue
            
        # Valida se a segunda parte é um número
        if not parts[1].replace('-', '').replace('.', '').isdigit():
            print(f"Linha {line_num} ignorada - offset não é numérico: {parts[1]}")
            continue
            
        row_index = int(parts[0])
        offset = float(parts[1])
        
        # Valida as tracks
        valid_tracks = []
        for track_str in parts[2:]:
            if track_str.isdigit():
                track_num = int(track_str)
                if 0 <= track_num <= 3:  # Tracks válidas são 0-3
                    valid_tracks.append(track_num)
                else:
                    print(f"Linha {line_num} - track inválida ignorada: {track_num}")
            else:
                print(f"Linha {line_num} - track não numérica ignorada: {track_str}")
        
        for track in valid_tracks:
            rows.append({"row": row_index, "offset": offset, "track": track})
            
    except (ValueError, IndexError) as e:
        print(f"Erro ao processar linha {line_num}: {line}")
        print(f"Erro: {e}")
        continue

print(f"Total de linhas processadas com sucesso: {len(rows)}")

# Verifica se temos dados válidos
if len(rows) == 0:
    print("ERRO: Nenhum dado válido encontrado no arquivo de replay!")
    print("Verifique se o arquivo está no formato correto:")
    print("Formato esperado: <row> <offset> <track1> <track2> ...")
    print("Exemplo: 100 0.023 0 2")
    exit(1)

df = pd.DataFrame(rows)

def classify_judgment(offset):
    abs_offset = abs(offset)
    if abs_offset <= 0.0225:
        return "W1 (Flawless)"
    elif abs_offset <= 0.045:
        return "W2 (Perfect)"
    elif abs_offset <= 0.090:
        return "W3 (Great)"
    elif abs_offset <= 0.135:
        return "W4 (Good)"
    elif abs_offset <= 0.180:
        return "W5 (Boo)"
    else:
        return "Miss"

df["judgment"] = df["offset"].apply(classify_judgment)

judgment_counts = df["judgment"].value_counts().sort_index()

plt.figure(figsize=(10, 6))
plt.scatter(df["row"], df["offset"], c="blue", alpha=0.7)
plt.axhline(0, color='gray', linestyle='--')
plt.title("Dispersão de Offsets por Nota")
plt.xlabel("Row (posição na música)")
plt.ylabel("Offset (s)")
plt.grid(True)
plt.tight_layout()


df.head(), judgment_counts


# Mapeamento de nomes para as tracks
track_names = {
    0: "Seta Esquerda",
    1: "Seta Baixo",
    2: "Seta Cima",
    3: "Seta Direita"
}

counts = df.groupby(['track', 'judgment']).size().reset_index(name='count')

totals = df.groupby('track').size().reset_index(name='total')

counts = counts.merge(totals, on='track')

counts['percentage'] = counts['count'] / counts['total'] * 100

counts['percentage'] = counts['percentage'].round(2)

counts['track_name'] = counts['track'].map(track_names)

percentual_acertos_por_movimento = counts[['track', 'track_name', 'judgment', 'count', 'total', 'percentage']]

print(percentual_acertos_por_movimento)


import pandas as pd

# --- Seu DataFrame percentual_acertos_por_movimento já definido ---
# Exemplo resumido para teste:
# percentual_acertos_por_movimento = pd.DataFrame({
#     'track': [0, 0, 1, 1, 2, 2, 3, 3],
#     'track_name': ["Seta Esquerda", "Seta Esquerda", "Seta Baixo", "Seta Baixo",
#                    "Seta Cima", "Seta Cima", "Seta Direita", "Seta Direita"],
#     'judgment': ["W1 (Flawless)", "W2 (Perfect)", "W1 (Flawless)", "Miss",
#                  "W1 (Flawless)", "W2 (Perfect)", "Miss", "W3 (Great)"],
#     'count': [9, 1, 7, 1, 7, 4, 7, 5],
#     'total': [14, 14, 13, 13, 15, 15, 13, 13],
#     'percentage': [64.29, 7.14, 53.85, 7.69, 46.67, 26.67, 53.85, 38.46]
# })

def parse_sm_difficulties():
    """Parse all difficulties from SM file and return them as a dictionary"""
    content = read_file_with_encoding(SM_FILE_PATH)
    
    difficulties = {}
    notes_sections = []
    
    start = 0
    while True:
        notes_start = content.find('#NOTES:', start)
        if notes_start == -1:
            break
        
        next_notes = content.find('#NOTES:', notes_start + 1)
        if next_notes == -1:
            notes_section = content[notes_start:]
        else:
            notes_section = content[notes_start:next_notes]
        
        notes_sections.append(notes_section)
        start = notes_start + 1
    
    for i, section in enumerate(notes_sections):
        lines = section.split('\n')
        metadata = []
        chart_data = []
        
        parsing_metadata = True
        for line in lines[1:]:  # Skip #NOTES: line
            line = line.strip()
            if parsing_metadata and ':' in line:
                metadata.append(line.strip(':').strip())
                if len(metadata) >= 5:  # We have all metadata
                    parsing_metadata = False
            elif not parsing_metadata:
                if line and (len(line) == 4 and all(c in '0123' for c in line)) or line in [',', ';']:
                    chart_data.append(line)
        
        if len(metadata) >= 3:
            game_type = metadata[0] if metadata[0] else "dance-single"
            author = metadata[1] if metadata[1] else ""
            difficulty = metadata[2] if metadata[2] else f"Difficulty_{i+1}"
            level = metadata[3] if len(metadata) > 3 else "0"
            
            display_name = f"{difficulty}"
            if author:
                display_name = f"{difficulty} ({author})"
            
            difficulties[display_name] = {
                'metadata': metadata,
                'chart_data': '\n'.join(chart_data),
                'raw_section': section
            }
    
    return difficulties

def choose_difficulty():
    """Let user choose which difficulty to modify"""
    global TARGET_DIFFICULTY
    
    difficulties = parse_sm_difficulties()
    
    if not difficulties:
        print("No difficulties found in the SM file!")
        return None, None
    
    if TARGET_DIFFICULTY:
        for key in difficulties.keys():
            if TARGET_DIFFICULTY.lower() in key.lower():
                print(f"Using specified difficulty: {key}")
                return key, difficulties[key]
        print(f"Difficulty '{TARGET_DIFFICULTY}' not found. Available difficulties:")
    
    print("\nAvailable difficulties:")
    diff_list = list(difficulties.keys())
    for i, diff in enumerate(diff_list, 1):
        print(f"{i}. {diff}")
    
    while True:
        try:
            choice = input(f"\nChoose difficulty (1-{len(diff_list)}): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(diff_list):
                    selected = diff_list[idx]
                    print(f"Selected: {selected}")
                    return selected, difficulties[selected]
            print("Invalid choice. Please try again.")
        except (ValueError, KeyboardInterrupt):
            print("Invalid input or cancelled.")
            return None, None

def get_chart_data_from_sm():
    """Extract chart data from selected difficulty"""
    difficulty_name, difficulty_data = choose_difficulty()
    
    if not difficulty_data:
        return ""
    
    global SELECTED_DIFFICULTY_NAME, SELECTED_DIFFICULTY_DATA
    SELECTED_DIFFICULTY_NAME = difficulty_name
    SELECTED_DIFFICULTY_DATA = difficulty_data
    
    return difficulty_data['chart_data']

def read_file_with_encoding(file_path):
    """Read file with multiple encoding attempts"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"Successfully read {file_path} with {encoding} encoding")
            return content
        except UnicodeDecodeError:
            continue
    
    raise Exception(f"Could not read file {file_path} with any supported encoding")

# Global variables to store selected difficulty info
SELECTED_DIFFICULTY_NAME = ""
SELECTED_DIFFICULTY_DATA = {}

chart_data = get_chart_data_from_sm()

lines = [line.strip() for line in chart_data.replace(',', '').replace(';', '').splitlines() if line.strip()]

step_counts = {0: 0, 1: 0, 2: 0, 3: 0}
for line in lines:
    if len(line) == 4:
        for i, char in enumerate(line):
            if char == '1':
                step_counts[i] += 1

track_names = {
    0: "Seta Esquerda",
    1: "Seta Baixo",
    2: "Seta Cima",
    3: "Seta Direita"
}

df_steps = pd.DataFrame([
    {"track": t, "track_name": track_names[t], "steps_in_chart": c}
    for t, c in step_counts.items()
])

df_totals_acertos = percentual_acertos_por_movimento.groupby(['track', 'track_name'])['count'].sum().reset_index(name='total_acertos')

df_relatorio = df_steps.merge(df_totals_acertos, on=['track', 'track_name'], how='left')

print("Passos no chart e total de acertos por track:")
print(df_relatorio)

print("\nDetalhes por julgamento:")
print(percentual_acertos_por_movimento.sort_values(['track', 'judgment']))

stats_dict = percentual_acertos_por_movimento.to_dict(orient="records")
stats_json_str = percentual_acertos_por_movimento.to_json(orient="records")

print("Tipo do objeto:", type(percentual_acertos_por_movimento))
print("Convertido para dict:",type(stats_dict))
print("Convertido para JSON:",type(stats_json_str))
print("DF:",percentual_acertos_por_movimento)


stats_dict = percentual_acertos_por_movimento.to_dict(orient="records")

data = {
    "original_sm_file": chart_data,  # Seu arquivo SM original (texto ou base64)
    "stats": stats_dict,  # Já é uma lista de dicionários (não precisa de json.loads)
    "instructions": "Analise o desempenho do player e diga suas impressões sobre o desempenho do player, e  depois gere\
    uma nova versão para facilitar o aprendizado do player,dificultando ou facilitando os movimentos"
}

# Chamar a API do DeepSeek
#response = requests.post(
#    "https://api.deepseek.com/v1/stepmania/generate",
#    json=data,  # `json=` serializa automaticamente para JSON
#    headers={"Authorization": "sk-8dd8d4577b9946029a85332e82e841b3"}
#)

# Salvar o novo arquivo SM
# new_sm_content = response.json()["generated_sm_file"]
# with open("new_chart.sm", "w") as f:
#    f.write(new_sm_content)


data_json = json.dumps(data, indent=2)

print("About to make API call...")
print(f"Data JSON length: {len(data_json)}")
print(f"First 500 chars of data_json: {data_json[:500]}")

response = requests.post(
    "https://api.deepseek.com/v1/chat/completions",  # Endpoint geral
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": data_json}],
        "temperature": 0.7
    },
    headers={"Authorization": "Bearer sk-8dd8d4577b9946029a85332e82e841b3"}
)

print(f"Status Code: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Response Text: {response.text}")

if response.status_code == 200:
    full_response = response.json()["choices"][0]["message"]["content"]
    
    # Cria pasta para salvar respostas da AI
    print("Criando pasta para respostas da AI...")
    ai_folder = create_ai_responses_folder()
    
    # Salva a resposta da AI
    ai_response_file = save_ai_response(full_response, ai_folder)
    
    chart_content = ""
    if "```" in full_response:
        start_marker = full_response.find("```")
        if start_marker != -1:
            start_marker = full_response.find("\n", start_marker) + 1
            end_marker = full_response.find("```", start_marker)
            if end_marker != -1:
                chart_content = full_response[start_marker:end_marker].strip()
    else:
        lines = full_response.split('\n')
        chart_lines = []
        for line in lines:
            line = line.strip()
            if line and (len(line) == 4 and all(c in '01' for c in line)) or line in [',', ';']:
                chart_lines.append(line)
        chart_content = '\n'.join(chart_lines)
    
    if chart_content:
        original_dir = os.path.dirname(SM_FILE_PATH)
        original_name = os.path.splitext(os.path.basename(SM_FILE_PATH))[0]
        
        safe_difficulty = SELECTED_DIFFICULTY_NAME.replace('(', '').replace(')', '').replace(' ', '_')
        new_filename = f"{original_name}_{safe_difficulty}_LearnMode.sm"
        new_filepath = os.path.join(original_dir, new_filename)
        
        original_content = read_file_with_encoding(SM_FILE_PATH)
        
        # Find and replace only the selected difficulty section
        if SELECTED_DIFFICULTY_DATA and 'raw_section' in SELECTED_DIFFICULTY_DATA:
            raw_section = SELECTED_DIFFICULTY_DATA['raw_section']
            
            # Find the position of this specific difficulty in the original file
            section_start = original_content.find(raw_section)
            if section_start != -1:
                section_end = section_start + len(raw_section)
                
                # Reconstruct the chart data section with metadata
                metadata_lines = []
                metadata_lines.append("#NOTES:")
                for meta in SELECTED_DIFFICULTY_DATA['metadata']:
                    metadata_lines.append(f"     {meta}:")
                
                new_section = '\n'.join(metadata_lines) + '\n' + chart_content + '\n'
                
                # Replace only this section
                new_content = (original_content[:section_start] + 
                              new_section + 
                              original_content[section_end:])
            else:
                print("Warning: Could not find the selected difficulty section in original file")
                new_content = original_content
        else:
            original_title = ""
            original_artist = ""
            original_music = ""
            original_offset = "0.000"
            original_bpms = "0.000=120.000"
            
            for line in original_content.split('\n'):
                line = line.strip()
                if line.startswith('#TITLE:'):
                    original_title = line.split(':', 1)[1].strip(';')
                elif line.startswith('#ARTIST:'):
                    original_artist = line.split(':', 1)[1].strip(';')
                elif line.startswith('#MUSIC:'):
                    original_music = line.split(':', 1)[1].strip(';')
                elif line.startswith('#OFFSET:'):
                    original_offset = line.split(':', 1)[1].strip(';')
                elif line.startswith('#BPMS:'):
                    original_bpms = line.split(':', 1)[1].strip(';')
            
            # Fallback: create basic  with original metadata
            new_content = f"""#TITLE:{original_title} - Learn Mode;
#ARTIST:{original_artist};
#MUSIC:{original_music};
#OFFSET:{original_offset};
#BPMS:{original_bpms};

#NOTES:
     dance-single:
     :
     Beginner:
     1:
     0,0,0,0,0:
{chart_content}
"""
        
        # Salvar o novo arquivo
        with open(new_filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Chart modificado salvo em: {new_filepath}")
        print(f"Resposta da AI salva em: {ai_response_file}")
        print("Texto completo da resposta:")
        print(full_response)
    else:
        print("Não foi possível extrair o conteúdo do chart da resposta")
        print("Resposta completa:")
        print(full_response)
        print(f"Resposta da AI salva em: {ai_response_file}")
else:
    print(f"Error {response.status_code}: {response.text}")
    if 'ai_response_file' in locals():
        print(f"Resposta da AI salva em: {ai_response_file}")