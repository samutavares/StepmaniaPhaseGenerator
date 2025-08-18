import re
import matplotlib.pyplot as plt
import statistics
import os

def parse_sm(file_path):
    """Extrai BPMs e blocos de notas de um arquivo .sm"""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Extrair BPMs
    bpm_match = re.search(r"#BPMS:([^;]*);", content, re.IGNORECASE)
    bpms = {}
    if bpm_match:
        for pair in bpm_match.group(1).split(","):
            beat, bpm = pair.split("=")
            bpms[float(beat)] = float(bpm)

    # Extrair blocos de notas (#NOTES:) com informações de dificuldade
    notes_blocks = []
    difficulty_info = []
    blocks = re.split(r"(?=#NOTES:)", content, flags=re.IGNORECASE)
    
    for i, block in enumerate(blocks):
        if block.strip().startswith("#NOTES:"):
            lines = block.strip().splitlines()
            
            # Extrai informações de dificuldade
            author = ""
            difficulty = ""
            rating = ""
            
            if len(lines) >= 3:
                author = lines[1].strip().rstrip(':')
                if len(lines) >= 4:
                    difficulty = lines[3].strip().rstrip(':')
                if len(lines) >= 5:
                    rating = lines[4].strip().rstrip(':')
            
            difficulty_info.append({
                'level_index': i,
                'author': author,
                'difficulty': difficulty,
                'rating': rating
            })
            
            # Extrai dados do chart (apenas linhas com notas)
            chart_data = []
            for line in lines:
                line = line.strip()
                # Verifica se é linha de chart data: 4 dígitos 0/1, ou vírgula, ou ponto e vírgula
                if (len(line) == 4 and all(c in '01' for c in line)) or line in [',', ';']:
                    chart_data.append(line)
            
            notes_blocks.append(chart_data)

    return bpms, notes_blocks, difficulty_info


def beats_to_seconds(bpms, beat):
    """Converte beats para segundos baseado nos BPMs"""
    if not bpms:
        return beat * (60.0 / 120.0)  # BPM padrão 120
    
    bpm_changes = sorted(bpms.items())
    time = 0.0
    last_beat = 0.0
    last_bpm = bpm_changes[0][1] if bpm_changes else 120.0

    for b, bpm in bpm_changes:
        if beat < b:
            break
        time += (b - last_beat) * (60.0 / last_bpm)
        last_beat, last_bpm = b, bpm

    time += (beat - last_beat) * (60.0 / last_bpm)
    return time


def calculate_nps(bpms, notes_block):
    """Calcula notas por segundo ao longo do chart"""
    notes_per_measure = []
    beat = 0
    
    # Processa o chart linha por linha, respeitando a estrutura de medidas
    current_measure_lines = []
    
    for line in notes_block:
        line = line.strip()
        
        if line == ',':
            # Fim da medida - processa as linhas acumuladas
            if current_measure_lines:
                measure_length = len(current_measure_lines)
                for i, measure_line in enumerate(current_measure_lines):
                    # Conta notas na linha (0=vazio, 1=nota, 2=hold_start, 3=hold_end, 4=mine)
                    notes = sum(1 for c in measure_line if c in "1234")
                    if notes > 0:
                        # Calcula posição temporal dentro da medida
                        current_beat = beat + (i / measure_length) * 4
                        second = beats_to_seconds(bpms, current_beat)
                        notes_per_measure.append((second, notes))
                
                current_measure_lines = []
                beat += 4
                
        elif line == ';':
            # Fim do chart
            break
            
        elif len(line) == 4 and all(c in '01234' for c in line):
            # Linha válida de notas
            current_measure_lines.append(line)
    
    # Processa última medida se não terminou com vírgula
    if current_measure_lines:
        measure_length = len(current_measure_lines)
        for i, measure_line in enumerate(current_measure_lines):
            notes = sum(1 for c in measure_line if c in "1234")
            if notes > 0:
                current_beat = beat + (i / measure_length) * 4
                second = beats_to_seconds(bpms, current_beat)
                notes_per_measure.append((second, notes))

    # Agrupar por segundo (com precisão de décimo)
    nps = {}
    for t, n in notes_per_measure:
        sec = round(t, 1)  # Precisão de 0.1s para melhor granularidade
        nps[sec] = nps.get(sec, 0) + n
    return nps


def summarize_chart(nps):
    """Gera estatísticas do chart"""
    if not nps:
        return {
            "Total de notas": 0,
            "Duração (s)": 0,
            "Média NPS": 0,
            "Pico NPS": 0,
            "Desvio padrão NPS": 0,
        }
    
    total_notes = sum(nps.values())
    duration = max(nps.keys()) if nps else 0
    values = list(nps.values()) if nps else [0]
    avg_nps = statistics.mean(values)
    max_nps = max(values)
    stdev_nps = statistics.pstdev(values) if len(values) > 1 else 0

    return {
        "Total de notas": total_notes,
        "Duração (s)": duration,
        "Média NPS": round(avg_nps, 2),
        "Pico NPS": max_nps,
        "Desvio padrão NPS": round(stdev_nps, 2),
    }


def plot_comparison(file1, file2, level_index=1):
    """Compara dois charts com validação e informações detalhadas"""
    
    print("=== COMPARADOR DE CHARTS STEPMANIA ===")
    print(f"📁 Arquivo 1: {os.path.basename(file1)}")
    print(f"📁 Arquivo 2: {os.path.basename(file2)}")
    print(f"🎯 Nível: {level_index}")
    print()
    
    # Verifica se os arquivos existem
    if not os.path.exists(file1):
        print(f"❌ Arquivo 1 não existe: {file1}")
        return
    if not os.path.exists(file2):
        print(f"❌ Arquivo 2 não existe: {file2}")
        return
    
    # Analisa os arquivos
    bpms1, notes1, diff_info1 = parse_sm(file1)
    bpms2, notes2, diff_info2 = parse_sm(file2)

    if not notes1 or not notes2:
        print("⚠️ Nenhum chart encontrado.")
        return

    # Mostra níveis disponíveis
    print("📁 Níveis disponíveis:")
    print("   ARQUIVO 1:")
    for i, info in enumerate(diff_info1):
        if i < len(notes1):
            print(f"      Nível {i}: {info['difficulty']} ({info['rating']}) - {len(notes1[i])} linhas")
    
    print("   ARQUIVO 2:")
    for i, info in enumerate(diff_info2):
        if i < len(notes2):
            print(f"      Nível {i}: {info['difficulty']} ({info['rating']}) - {len(notes2[i])} linhas")
    
    # Verifica se o nível escolhido existe
    if level_index >= len(notes1) or level_index >= len(notes2):
        print(f"\n❌ Nível {level_index} não existe!")
        print(f"   Arquivo 1: máximo nível {len(notes1)-1}")
        print(f"   Arquivo 2: máximo nível {len(notes2)-1}")
        return
    
    # Mostra informações do nível escolhido
    nivel_info1 = diff_info1[level_index] if level_index < len(diff_info1) else {}
    nivel_info2 = diff_info2[level_index] if level_index < len(diff_info2) else {}
    print(f"\n🎯 Comparando nível {level_index}:")
    print(f"   Arquivo 1: {nivel_info1.get('difficulty', 'N/A')} ({nivel_info1.get('rating', 'N/A')}) - {len(notes1[level_index])} linhas")
    print(f"   Arquivo 2: {nivel_info2.get('difficulty', 'N/A')} ({nivel_info2.get('rating', 'N/A')}) - {len(notes2[level_index])} linhas")
    
    # Calcula NPS
    nps1 = calculate_nps(bpms1, notes1[level_index])
    nps2 = calculate_nps(bpms2, notes2[level_index])

    stats1 = summarize_chart(nps1)
    stats2 = summarize_chart(nps2)

    # Mostrar estatísticas no console
    print("\n📊 Estatísticas do Chart Original:")
    for k, v in stats1.items():
        print(f"  {k}: {v}")

    print("\n📊 Estatísticas do Chart Modificado:")
    for k, v in stats2.items():
        print(f"  {k}: {v}")

    # Plotar comparação
    max_time = max(max(nps1.keys(), default=0), max(nps2.keys(), default=0))
    if max_time > 0:
        # Criar eixo x com precisão de 0.1s
        x = [round(i * 0.1, 1) for i in range(int(max_time * 10) + 1)]
        y1 = [nps1.get(t, 0) for t in x]
        y2 = [nps2.get(t, 0) for t in x]

        plt.figure(figsize=(12, 6))
        plt.plot(x, y1, label=f"Original - {nivel_info1.get('difficulty', 'N/A')}", alpha=0.7, linewidth=2)
        plt.plot(x, y2, label=f"Modificado - {nivel_info2.get('difficulty', 'N/A')}", alpha=0.7, linewidth=2)
        plt.xlabel("Tempo (segundos)")
        plt.ylabel("Notas por segundo (NPS)")
        plt.title(f"Comparação de Densidade de Notas - Nível {level_index}")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    else:
        print("⚠️ Não foi possível gerar o gráfico (duração = 0)")


# ========================================
# CONFIGURAÇÃO SIMPLES - APENAS 3 VARIÁVEIS
# ========================================

# 1. ARQUIVO 1 (Original)
Musica1 = r"C:\Games\Etterna\Songs\Hey, Soul Sister\Stepchart.sm"

# 2. ARQUIVO 2 (Modificado)
Musica2 = r"C:\Games\Etterna\Songs\Hey, Soul Sister\Stepchart_Beginner_LearnMode.sm"

# 3. NÍVEL PARA COMPARAR (0, 1, 2, etc.)
Nivel = 1

# ========================================
# EXECUÇÃO AUTOMÁTICA
# ========================================

if __name__ == "__main__":
    plot_comparison(Musica1, Musica2, level_index=Nivel)
