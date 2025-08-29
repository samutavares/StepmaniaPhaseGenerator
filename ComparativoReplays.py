import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
from datetime import datetime
import numpy as np

# ======= CONFIGURAÇÕES - MODIFIQUE AQUI =======
SONG_FOLDER = r"C:\Games\Etterna\Songs\Loca"
SM_FILENAME = "Stepchart.sm"
REPLAYS_DIR = r"C:\Games\Etterna\Save\ReplaysV2"

# Configuração do nome do usuário
USERNAME = "Samuel"  # Modifique aqui para o nome desejado

# Configuração para comparação de músicas
MUSICA1_FOLDER = r"C:\Games\Etterna\Songs\Loca"
MUSICA1_FILENAME = "Stepchart.sm"

MUSICA2_FOLDER = r"C:\Games\Etterna\Songs\Loca"
MUSICA2_FILENAME = "Stepchart.sm"

SM_FILE_PATH = os.path.join(SONG_FOLDER, SM_FILENAME)
MUSICA1_PATH = os.path.join(MUSICA1_FOLDER, MUSICA1_FILENAME)
MUSICA2_PATH = os.path.join(MUSICA2_FOLDER, MUSICA2_FILENAME)
# ===============================================

def parse_sm_file(file_path):
    """Parse de arquivo SM para extrair dados do chart"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extrai seções #NOTES:
        import re
        notes_sections = re.findall(r'#NOTES:.*?(?=#NOTES:|$)', content, re.DOTALL | re.IGNORECASE)
        
        charts = []
        for section in notes_sections:
            lines = section.strip().split('\n')
            
            # Extrai metadados
            metadata = []
            chart_data = []
            parsing_metadata = True
            
            for line in lines[1:]:  # Pula #NOTES:
                line = line.strip()
                if parsing_metadata and ':' in line:
                    metadata.append(line.rstrip(':').strip())
                    if len(metadata) >= 5:  # Temos todos os metadados
                        parsing_metadata = False
                elif not parsing_metadata:
                    if line and (len(line) == 4 and all(c in '0123' for c in line)) or line in [',', ';']:
                        chart_data.append(line)
            
            if len(metadata) >= 3:
                charts.append({
                    'metadata': metadata,
                    'chart_data': chart_data,
                    'difficulty': metadata[2] if len(metadata) > 2 else 'Unknown',
                    'level': metadata[3] if len(metadata) > 3 else '0'
                })
        
        return charts
    except Exception as e:
        print(f"Erro ao ler arquivo SM {file_path}: {e}")
        return []

def analyze_sm_chart(charts, difficulty_index=0):
    """Analisa um chart SM específico"""
    if not charts or difficulty_index >= len(charts):
        return {}
    
    chart = charts[difficulty_index]
    chart_data = chart['chart_data']
    
    # Conta notas por track
    track_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    total_notes = 0
    
    for line in chart_data:
        if len(line) == 4 and all(c in '01' for c in line):
            for i, char in enumerate(line):
                if char == '1':
                    track_counts[i] += 1
                    total_notes += 1
    
    # Calcula densidade de notas
    note_density = total_notes / len(chart_data) if chart_data else 0
    
    return {
        'difficulty': chart['difficulty'],
        'level': chart['level'],
        'total_notes': total_notes,
        'track_counts': track_counts,
        'note_density': note_density,
        'chart_length': len(chart_data)
    }

def compare_sm_files(file1_path, file2_path, difficulty_index=0):
    """Compara dois arquivos SM"""
    print(f"🎵 Comparando arquivos SM:")
    print(f"   Música 1: {os.path.basename(file1_path)}")
    print(f"   Música 2: {os.path.basename(file2_path)}")
    print("=" * 60)
    
    # Parse dos arquivos
    charts1 = parse_sm_file(file1_path)
    charts2 = parse_sm_file(file2_path)
    
    if not charts1:
        print(f"❌ Erro ao ler {file1_path}")
        return None
    if not charts2:
        print(f"❌ Erro ao ler {file2_path}")
        return None
    
    # Mostra dificuldades disponíveis
    print(f"\n📁 Dificuldades disponíveis:")
    print(f"   Música 1 ({os.path.basename(file1_path)}):")
    for i, chart in enumerate(charts1):
        print(f"      {i}: {chart['difficulty']} (Nível {chart['level']})")
    
    print(f"   Música 2 ({os.path.basename(file2_path)}):")
    for i, chart in enumerate(charts2):
        print(f"      {i}: {chart['difficulty']} (Nível {chart['level']})")
    
    # Analisa as dificuldades escolhidas
    analysis1 = analyze_sm_chart(charts1, difficulty_index)
    analysis2 = analyze_sm_chart(charts2, difficulty_index)
    
    if not analysis1 or not analysis2:
        print("❌ Erro na análise dos charts")
        return None
    
    return {
        'music1': {
            'filename': os.path.basename(file1_path),
            'analysis': analysis1
        },
        'music2': {
            'filename': os.path.basename(file2_path),
            'analysis': analysis2
        }
    }

def plot_sm_comparison(sm_comparison):
    """Cria gráficos comparativos dos arquivos SM"""
    if not sm_comparison:
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Comparação de Charts SM', fontsize=16)
    
    music1 = sm_comparison['music1']
    music2 = sm_comparison['music2']
    
    # 1.1 - Total de notas por música
    ax1 = axes[0, 0]
    musics = [music1['filename'], music2['filename']]
    totals = [music1['analysis']['total_notes'], music2['analysis']['total_notes']]
    
    bars = ax1.bar(musics, totals, color=['skyblue', 'lightcoral'])
    ax1.set_title('Total de Notas por Música')
    ax1.set_ylabel('Número de Notas')
    
    # Adiciona valores nas barras
    for bar, total in zip(bars, totals):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01*max(totals),
                f'{total}', ha='center', va='bottom')
    
    # 1.2 - Distribuição por track
    ax2 = axes[0, 1]
    track_names = ['Esquerda', 'Baixo', 'Cima', 'Direita']
    x = np.arange(len(track_names))
    width = 0.35
    
    track_counts1 = list(music1['analysis']['track_counts'].values())
    track_counts2 = list(music2['analysis']['track_counts'].values())
    
    bars1 = ax2.bar(x - width/2, track_counts1, width, label=music1['filename'], color='skyblue')
    bars2 = ax2.bar(x + width/2, track_counts2, width, label=music2['filename'], color='lightcoral')
    
    ax2.set_title('Distribuição de Notas por Track')
    ax2.set_ylabel('Número de Notas')
    ax2.set_xticks(x)
    ax2.set_xticklabels(track_names)
    ax2.legend()
    
    # 1.3 - Densidade de notas
    ax3 = axes[1, 0]
    densities = [music1['analysis']['note_density'], music2['analysis']['note_density']]
    
    bars = ax3.bar(musics, densities, color=['skyblue', 'lightcoral'])
    ax3.set_title('Densidade de Notas')
    ax3.set_ylabel('Notas por linha')
    
    for bar, density in zip(bars, densities):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01*max(densities),
                f'{density:.2f}', ha='center', va='bottom')
    
    # 1.4 - Comparação de dificuldade
    ax4 = axes[1, 1]
    levels = [int(music1['analysis']['level']), int(music2['analysis']['level'])]
    
    bars = ax4.bar(musics, levels, color=['skyblue', 'lightcoral'])
    ax4.set_title('Nível de Dificuldade')
    ax4.set_ylabel('Nível')
    
    for bar, level in zip(bars, levels):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1*max(levels),
                f'{level}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

def generate_sm_report(sm_comparison):
    """Gera relatório da comparação SM"""
    if not sm_comparison:
        return
    
    print("\n" + "=" * 60)
    print("📋 RELATÓRIO DE COMPARAÇÃO DE MÚSICAS")
    print("=" * 60)
    
    music1 = sm_comparison['music1']
    music2 = sm_comparison['music2']
    
    print(f"\n🎵 MÚSICA 1: {music1['filename']}")
    print(f"   Dificuldade: {music1['analysis']['difficulty']}")
    print(f"   Nível: {music1['analysis']['level']}")
    print(f"   Total de notas: {music1['analysis']['total_notes']}")
    print(f"   Densidade: {music1['analysis']['note_density']:.2f} notas/linha")
    print(f"   Comprimento: {music1['analysis']['chart_length']} linhas")
    
    print(f"\n🎵 MÚSICA 2: {music2['filename']}")
    print(f"   Dificuldade: {music2['analysis']['difficulty']}")
    print(f"   Nível: {music2['analysis']['level']}")
    print(f"   Total de notas: {music2['analysis']['total_notes']}")
    print(f"   Densidade: {music2['analysis']['note_density']:.2f} notas/linha")
    print(f"   Comprimento: {music2['analysis']['chart_length']} linhas")
    
    # Comparação
    print(f"\n📊 COMPARAÇÃO:")
    print("-" * 40)
    
    notes_diff = music2['analysis']['total_notes'] - music1['analysis']['total_notes']
    density_diff = music2['analysis']['note_density'] - music1['analysis']['note_density']
    level_diff = int(music2['analysis']['level']) - int(music1['analysis']['level'])
    
    print(f"   Diferença em notas: {notes_diff:+d}")
    print(f"   Diferença em densidade: {density_diff:+.2f}")
    print(f"   Diferença em nível: {level_diff:+d}")
    
    # Recomendações
    print(f"\n💡 RECOMENDAÇÕES:")
    if abs(level_diff) <= 1:
        print(f"   ✅ Níveis similares - boa progressão!")
    elif level_diff > 1:
        print(f"   ⚠️ Música 2 é mais difícil - pratique mais a Música 1 primeiro")
    else:
        print(f"   ✅ Música 2 é mais fácil - boa para relaxar")
    
    if density_diff > 0.5:
        print(f"   ⚠️ Música 2 tem mais notas por linha - mais intensa")
    elif density_diff < -0.5:
        print(f"   ✅ Música 2 tem menos notas por linha - mais relaxante")
    else:
        print(f"   ✅ Densidades similares - boa consistência")

def get_username():
    """Obtém o nome do usuário da configuração"""
    return USERNAME

def get_latest_replay_files(num_files=2):
    """Obtém os últimos arquivos de replay"""
    all_files = glob.glob(os.path.join(REPLAYS_DIR, "*"))
    
    if len(all_files) < num_files:
        print(f"⚠️ Apenas {len(all_files)} arquivo(s) de replay encontrado(s). Necessário {num_files}.")
        return all_files
    
    # Ordena por data de criação (mais recente primeiro)
    sorted_files = sorted(all_files, key=os.path.getctime, reverse=True)
    return sorted_files[:num_files]

def parse_replay_data(file_path):
    """Parse dos dados do arquivo de replay"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        rows = []
        for line_num, line in enumerate(content.strip().splitlines(), 1):
            try:
                parts = line.split()
                if len(parts) < 3:
                    continue
                    
                # Valida se as partes são numéricas
                if not parts[0].replace('-', '').replace('.', '').isdigit():
                    continue
                if not parts[1].replace('-', '').replace('.', '').isdigit():
                    continue
                    
                row_index = int(parts[0])
                offset = float(parts[1])
                
                # Valida as tracks
                valid_tracks = []
                for track_str in parts[2:]:
                    if track_str.isdigit():
                        track_num = int(track_str)
                        if 0 <= track_num <= 3:
                            valid_tracks.append(track_num)
                
                for track in valid_tracks:
                    rows.append({"row": row_index, "offset": offset, "track": track})
                    
            except (ValueError, IndexError) as e:
                continue
        
        return pd.DataFrame(rows)
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}")
        return pd.DataFrame()

def classify_judgment(offset):
    """Classifica o julgamento baseado no offset"""
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

def analyze_replay_performance(df):
    """Analisa o desempenho de um replay"""
    if df.empty:
        return {}
    
    df["judgment"] = df["offset"].apply(classify_judgment)
    
    # Estatísticas gerais
    total_notes = len(df)
    avg_offset = df["offset"].mean()
    std_offset = df["offset"].std()
    
    # Contagem por julgamento
    judgment_counts = df["judgment"].value_counts()
    
    # Análise por track
    track_names = {0: "Seta Esquerda", 1: "Seta Baixo", 2: "Seta Cima", 3: "Seta Direita"}
    df["track_name"] = df["track"].map(track_names)
    
    track_stats = df.groupby(['track', 'track_name']).agg({
        'offset': ['count', 'mean', 'std'],
        'judgment': lambda x: x.value_counts().to_dict()
    }).round(4)
    
    # Análise temporal (por row)
    temporal_stats = df.groupby('row').agg({
        'offset': ['count', 'mean', 'std'],
        'judgment': lambda x: x.value_counts().to_dict()
    }).round(4)
    
    return {
        "total_notes": total_notes,
        "avg_offset": avg_offset,
        "std_offset": std_offset,
        "judgment_counts": judgment_counts.to_dict(),
        "track_stats": track_stats,
        "temporal_stats": temporal_stats,
        "raw_data": df
    }

def compare_replays(replay_files):
    """Compara múltiplos replays"""
    if len(replay_files) < 2:
        print("❌ Necessário pelo menos 2 arquivos de replay para comparação")
        return
    
    print(f"📊 Comparando {len(replay_files)} replays...")
    print("=" * 60)
    
    performances = {}
    
    for i, file_path in enumerate(replay_files, 1):
        filename = os.path.basename(file_path)
        print(f"\n🎵 Analisando Replay {i}: {filename}")
        
        df = parse_replay_data(file_path)
        if df.empty:
            print(f"❌ Erro ao processar {filename}")
            continue
        
        performance = analyze_replay_performance(df)
        performances[f"replay_{i}"] = {
            "filename": filename,
            "performance": performance
        }
        
        # Mostra estatísticas básicas
        if performance:
            print(f"   Total de notas: {performance['total_notes']}")
            print(f"   Offset médio: {performance['avg_offset']:.4f}s")
            print(f"   Desvio padrão: {performance['std_offset']:.4f}s")
            print(f"   Julgamentos: {dict(performance['judgment_counts'])}")
    
    return performances

def plot_comparison(performances):
    """Cria gráficos comparativos"""
    if not performances or len(performances) < 2:
        print("❌ Dados insuficientes para comparação")
        return
    
    # Gráfico 1: Comparação de julgamentos
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Comparação de Desempenho entre Replays', fontsize=16)
    
    # 1.1 - Julgamentos por replay
    ax1 = axes[0, 0]
    judgment_data = {}
    labels = []
    
    for key, data in performances.items():
        if data['performance']:
            judgment_counts = data['performance']['judgment_counts']
            labels.append(data['filename'])
            judgment_data[key] = judgment_counts
    
    if judgment_data:
        judgment_df = pd.DataFrame(judgment_data).fillna(0)
        judgment_df.plot(kind='bar', ax=ax1, width=0.8)
        ax1.set_title('Distribuição de Julgamentos')
        ax1.set_ylabel('Quantidade')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.tick_params(axis='x', rotation=45)
    
    # 1.2 - Offset médio por track
    ax2 = axes[0, 1]
    track_data = {}
    
    for key, data in performances.items():
        if data['performance'] and not data['performance']['track_stats'].empty:
            track_stats = data['performance']['track_stats']
            if 'offset' in track_stats.columns:
                track_data[key] = track_stats[('offset', 'mean')]
    
    if track_data:
        track_df = pd.DataFrame(track_data)
        track_df.plot(kind='bar', ax=ax2, width=0.8)
        ax2.set_title('Offset Médio por Track')
        ax2.set_ylabel('Offset (segundos)')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.tick_params(axis='x', rotation=45)
    
    # 1.3 - Evolução temporal do offset
    ax3 = axes[1, 0]
    for key, data in performances.items():
        if data['performance']:
            df = data['performance']['raw_data']
            ax3.scatter(df['row'], df['offset'], alpha=0.6, label=data['filename'], s=20)
    
    ax3.set_title('Evolução do Offset ao Longo da Música')
    ax3.set_xlabel('Row (posição na música)')
    ax3.set_ylabel('Offset (segundos)')
    ax3.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 1.4 - Histograma de offsets
    ax4 = axes[1, 1]
    for key, data in performances.items():
        if data['performance']:
            df = data['performance']['raw_data']
            ax4.hist(df['offset'], bins=30, alpha=0.6, label=data['filename'])
    
    ax4.set_title('Distribuição de Offsets')
    ax4.set_xlabel('Offset (segundos)')
    ax4.set_ylabel('Frequência')
    ax4.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def generate_report(performances):
    """Gera relatório detalhado da comparação"""
    if not performances or len(performances) < 2:
        print("❌ Dados insuficientes para relatório")
        return
    
    print("\n" + "=" * 60)
    print("📋 RELATÓRIO DETALHADO DE COMPARAÇÃO")
    print("=" * 60)
    
    # Comparação geral
    print("\n🎯 COMPARAÇÃO GERAL:")
    print("-" * 40)
    
    for key, data in performances.items():
        if data['performance']:
            perf = data['performance']
            print(f"\n📁 {data['filename']}:")
            print(f"   Total de notas: {perf['total_notes']}")
            print(f"   Offset médio: {perf['avg_offset']:.4f}s")
            print(f"   Desvio padrão: {perf['std_offset']:.4f}s")
            
            # Calcula precisão (W1 + W2)
            judgment_counts = perf['judgment_counts']
            flawless = judgment_counts.get('W1 (Flawless)', 0)
            perfect = judgment_counts.get('W2 (Perfect)', 0)
            total = perf['total_notes']
            accuracy = ((flawless + perfect) / total * 100) if total > 0 else 0
            print(f"   Precisão (W1+W2): {accuracy:.2f}%")
    
    # Análise por track
    print("\n🎵 ANÁLISE POR TRACK:")
    print("-" * 40)
    
    track_names = {0: "Seta Esquerda", 1: "Seta Baixo", 2: "Seta Cima", 3: "Seta Direita"}
    
    for track_num in range(4):
        track_name = track_names[track_num]
        print(f"\n   {track_name}:")
        
        for key, data in performances.items():
            if data['performance']:
                perf = data['performance']
                track_stats = perf['track_stats']
                
                if not track_stats.empty and track_num in track_stats.index:
                    track_data = track_stats.loc[track_num]
                    count = track_data[('offset', 'count')]
                    mean_offset = track_data[('offset', 'mean')]
                    std_offset = track_data[('offset', 'std')]
                    
                    print(f"     {data['filename']}: {count} notas, offset médio: {mean_offset:.4f}s (±{std_offset:.4f}s)")
    
    # Melhorias/Regressões
    print("\n📈 ANÁLISE DE PROGRESSO:")
    print("-" * 40)
    
    if len(performances) >= 2:
        keys = list(performances.keys())
        perf1 = performances[keys[0]]['performance']
        perf2 = performances[keys[1]]['performance']
        
        if perf1 and perf2:
            # Compara precisão
            acc1 = ((perf1['judgment_counts'].get('W1 (Flawless)', 0) + 
                    perf1['judgment_counts'].get('W2 (Perfect)', 0)) / perf1['total_notes'] * 100)
            acc2 = ((perf2['judgment_counts'].get('W1 (Flawless)', 0) + 
                    perf2['judgment_counts'].get('W2 (Perfect)', 0)) / perf2['total_notes'] * 100)
            
            acc_diff = acc2 - acc1
            print(f"   Precisão: {acc1:.2f}% → {acc2:.2f}% ({acc_diff:+.2f}%)")
            
            # Compara offset médio
            offset_diff = perf2['avg_offset'] - perf1['avg_offset']
            print(f"   Offset médio: {perf1['avg_offset']:.4f}s → {perf2['avg_offset']:.4f}s ({offset_diff:+.4f}s)")
            
            # Compara consistência
            std_diff = perf2['std_offset'] - perf1['std_offset']
            print(f"   Consistência: {perf1['std_offset']:.4f}s → {perf2['std_offset']:.4f}s ({std_diff:+.4f}s)")
            
            # Recomendações
            print(f"\n💡 RECOMENDAÇÕES:")
            if acc_diff > 0:
                print(f"   ✅ Melhoria na precisão! Continue praticando.")
            elif acc_diff < 0:
                print(f"   ⚠️ Redução na precisão. Revise sua técnica.")
            
            if abs(offset_diff) < 0.01:
                print(f"   ✅ Timing consistente entre as tentativas.")
            else:
                print(f"   ⚠️ Variação no timing. Foque na consistência.")
            
            if std_diff < 0:
                print(f"   ✅ Melhoria na consistência!")
            elif std_diff > 0:
                print(f"   ⚠️ Redução na consistência. Pratique mais.")

def main():
    """Função principal"""
    print("🎮 COMPARADOR DE REPLAYS E MÚSICAS - STEPMANIA")
    print("=" * 60)
    
    # Menu de opções
    print("\n📋 Escolha uma opção:")
    print("1. Comparar dois últimos replays")
    print("2. Comparar duas músicas (arquivos SM)")
    print("3. Comparar replays E músicas")
    
    try:
        choice = input("\nDigite sua escolha (1-3): ").strip()
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada pelo usuário")
        return
    
    if choice == "1":
        # Compara apenas replays
        compare_replays_only()
    elif choice == "2":
        # Compara apenas músicas
        compare_musics_only()
    elif choice == "3":
        # Compara ambos
        compare_both()
    else:
        print("❌ Opção inválida!")

def compare_replays_only():
    """Compara apenas os replays"""
    print("\n🎵 COMPARAÇÃO DE REPLAYS")
    print("=" * 40)
    
    # Obtém os últimos arquivos de replay
    replay_files = get_latest_replay_files(2)
    
    if len(replay_files) < 2:
        print("❌ Necessário pelo menos 2 arquivos de replay para comparação")
        return
    
    print(f"📁 Arquivos encontrados:")
    for i, file_path in enumerate(replay_files, 1):
        filename = os.path.basename(file_path)
        creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        print(f"   {i}. {filename} (criado em {creation_time.strftime('%d/%m/%Y %H:%M:%S')})")
    
    # Compara os replays
    performances = compare_replays(replay_files)
    
    if performances:
        # Gera gráficos
        plot_comparison(performances)
        
        # Gera relatório
        generate_report(performances)
        
        print(f"\n✅ Análise de replays concluída! {len(performances)} replays comparados.")
    else:
        print("❌ Erro na análise dos replays")

def compare_musics_only():
    """Compara apenas as músicas"""
    print("\n🎵 COMPARAÇÃO DE MÚSICAS")
    print("=" * 40)
    
    # Verifica se os arquivos existem
    if not os.path.exists(MUSICA1_PATH):
        print(f"❌ Arquivo não encontrado: {MUSICA1_PATH}")
        return
    
    if not os.path.exists(MUSICA2_PATH):
        print(f"❌ Arquivo não encontrado: {MUSICA2_PATH}")
        return
    
    print(f"📁 Arquivos encontrados:")
    print(f"   1. {os.path.basename(MUSICA1_PATH)}")
    print(f"   2. {os.path.basename(MUSICA2_PATH)}")
    
    # Compara as músicas
    sm_comparison = compare_sm_files(MUSICA1_PATH, MUSICA2_PATH, difficulty_index=0)
    
    if sm_comparison:
        # Gera gráficos
        plot_sm_comparison(sm_comparison)
        
        # Gera relatório
        generate_sm_report(sm_comparison)
        
        print(f"\n✅ Análise de músicas concluída!")
    else:
        print("❌ Erro na análise das músicas")

def compare_both():
    """Compara replays e músicas"""
    print("\n🎵 COMPARAÇÃO COMPLETA")
    print("=" * 40)
    
    # Primeiro compara as músicas
    print("\n📊 PARTE 1: COMPARAÇÃO DE MÚSICAS")
    compare_musics_only()
    
    # Depois compara os replays
    print("\n📊 PARTE 2: COMPARAÇÃO DE REPLAYS")
    compare_replays_only()
    
    print(f"\n✅ Análise completa concluída!")

if __name__ == "__main__":
    main()
