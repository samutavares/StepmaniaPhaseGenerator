import difflib
import re

def extract_chart_data_only(file_path):
    """Extrai APENAS as linhas de chart data (0000, 0001, etc.) de cada nível"""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    blocks = re.split(r"(?=#NOTES:)", content, flags=re.IGNORECASE)
    chart_data_blocks = []
    
    for block in blocks:
        if block.strip().startswith("#NOTES:"):
            lines = block.strip().splitlines()
            
            # Extrai apenas as linhas de chart data (4 caracteres com 0/1, vírgulas, pontos e vírgulas)
            chart_lines = []
            for line in lines:
                line = line.strip()
                # Verifica se é linha de chart data: 4 dígitos 0/1, ou vírgula, ou ponto e vírgula
                if (len(line) == 4 and all(c in '01' for c in line)) or line in [',', ';']:
                    chart_lines.append(line)
            
            chart_data_blocks.append(chart_lines)
    
    return chart_data_blocks

def extract_difficulty_info(file_path):
    """Extrai informações sobre as dificuldades de cada nível"""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    blocks = re.split(r"(?=#NOTES:)", content, flags=re.IGNORECASE)
    difficulty_info = []
    
    for i, block in enumerate(blocks):
        if block.strip().startswith("#NOTES:"):
            lines = block.strip().splitlines()
            
            # Extrai informações do header
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
    
    return difficulty_info

def compare_chart_data(file1, file2, level_index1=0, level_index2=None, output="diff_result.txt"):
    """Compara apenas os dados de chart (linhas 0/1) entre dois arquivos SM"""
    if level_index2 is None:
        level_index2 = level_index1
        
    # Extrai dados e informações de dificuldade
    chart_data1 = extract_chart_data_only(file1)
    chart_data2 = extract_chart_data_only(file2)
    diff_info1 = extract_difficulty_info(file1)
    diff_info2 = extract_difficulty_info(file2)

    if not chart_data1 or not chart_data2:
        print("⚠️ Nenhum chart data encontrado em um dos arquivos.")
        return

    # Se level_index1 é um número, mas queremos comparar o mesmo tipo de dificuldade
    if isinstance(level_index1, int):
        # SÓ substitui se level_index1 for 0 (padrão) ou se especificamente solicitado
        if level_index1 == 0:
            # Encontra o nível Beginner em ambos os arquivos
            beginner_index1 = None
            beginner_index2 = None
            
            for info in diff_info1:
                if "Beginner" in info['difficulty']:
                    beginner_index1 = info['level_index']
                    break
                    
            for info in diff_info2:
                if "Beginner" in info['difficulty']:
                    beginner_index2 = info['level_index']
                    break
            
            # Se encontrou Beginner em ambos, usa esses índices
            if beginner_index1 is not None and beginner_index2 is not None:
                print(f"🎯 Comparando nível Beginner: arquivo1[{beginner_index1}] vs arquivo2[{beginner_index2}]")
                level_index1 = beginner_index1
                level_index2 = beginner_index2
            else:
                print(f"⚠️ Nível Beginner não encontrado, usando índices originais: {level_index1}, {level_index2}")
        else:
            # Usa os índices especificados pelo usuário
            print(f"🎯 Usando índices especificados: arquivo1[{level_index1}] vs arquivo2[{level_index2}]")

    if level_index1 >= len(chart_data1) or level_index2 >= len(chart_data2):
        print("⚠️ O índice de nível solicitado não existe em um dos arquivos.")
        return

    lines1 = chart_data1[level_index1]
    lines2 = chart_data2[level_index2]

    # Remove o suffix "_LearnMode" do nome do arquivo para melhor legibilidade
    file1_name = file1.replace("_LearnMode", "")
    file2_name = file2.replace("_LearnMode", " (LearnMode)")

    diff = difflib.unified_diff(
        lines1, lines2,
        fromfile=f"{file1_name} (chart data nivel {level_index1})",
        tofile=f"{file2_name} (chart data nivel {level_index2})",
        lineterm=""
    )

    diff_lines = list(diff)

    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    matching_blocks = matcher.get_matching_blocks()

    same_lines = sum(block.size for block in matching_blocks)
    total1 = len(lines1)
    total2 = len(lines2)
    different_lines = max(total1, total2) - same_lines
    similarity = matcher.ratio() * 100

    with open(output, "w", encoding="utf-8") as out:
        out.write("=== COMPARAÇÃO DE CHART DATA ===\n\n")
        out.write("Comparando apenas as linhas de notas (0000, 0001, etc.)\n")
        out.write("Ignorando metadados e headers\n\n")
        
        out.write("=== Diferenças encontradas ===\n\n")
        for line in diff_lines:
            out.write(line + "\n")

        out.write("\n=== Resumo ===\n")
        out.write(f"Total linhas chart original: {total1}\n")
        out.write(f"Total linhas chart modificado: {total2}\n")
        out.write(f"Linhas iguais: {same_lines}\n")
        out.write(f"Linhas diferentes: {different_lines}\n")
        out.write(f"Similaridade do chart data: {similarity:.2f}%\n")

    print(f"✅ Comparação de chart data salva em {output}")
    print(f"📊 Similaridade: {similarity:.2f}%")
    print(f"📈 Linhas iguais: {same_lines}/{max(total1, total2)}")

# Função para compatibilidade com código antigo
def compare_levels(file1, file2, level_index=0, output="diff_result.txt"):
    """Função de compatibilidade - redireciona para compare_chart_data"""
    print("ℹ️  Usando compare_chart_data (comparação apenas de dados de chart)")
    return compare_chart_data(file1, file2, level_index1=level_index, level_index2=level_index, output=output)

def test_extraction_example():
    """Função para testar e demonstrar como a extração funciona"""
    print("=== TESTE DE EXTRAÇÃO ===")
    example_content = """#TITLE:Test Song;
#NOTES:
     dance-single:
     :
     Beginner:
     1:
     0,0,0,0,0:
0000
0001
0010
,
1000
0100
;
"""
    
    # Simula arquivo temporário
    with open("temp_test.sm", "w", encoding="utf-8") as f:
        f.write(example_content)
    
    chart_data = extract_chart_data_only("temp_test.sm")
    
    if chart_data:
        print(f"📊 Chart data extraído: {len(chart_data)} níveis")
        print("🎵 Primeiras linhas do nível 0:")
        for i, line in enumerate(chart_data[0][:10]):
            print(f"  {i+1}: '{line}'")
    
    # Limpa arquivo temporário
    import os
    if os.path.exists("temp_test.sm"):
        os.remove("temp_test.sm")

# ========================================
# CONFIGURAÇÃO SIMPLES - APENAS 3 VARIÁVEIS
# ========================================

# 1. ARQUIVO 1 (Original)
Musica1 = r"C:\Games\Etterna\Songs\The Time (Dirty Bit)\Stepchart.sm"

# 2. ARQUIVO 2 (Modificado)
Musica2 = r"C:\Games\Etterna\Songs\The Time (Dirty Bit)\Stepchart_Beginner_LearnMode.sm"

# 3. NÍVEL PARA COMPARAR (0, 1, 2, etc.)
Nivel = 4  # 1 = Beginner, 2 = Easy, 3 = Medium, etc.

# ========================================
# EXECUÇÃO AUTOMÁTICA
# ========================================

if __name__ == "__main__":
    print("=== COMPARADOR DE CHARTS STEPMANIA ===")
    print(f"📁 Arquivo 1: {Musica1}")
    print(f"📁 Arquivo 2: {Musica2}")
    print(f"🎯 Nível: {Nivel}")
    print()
    
    # Verifica se os arquivos existem
    import os
    if not os.path.exists(Musica1):
        print(f"❌ Arquivo 1 não existe: {Musica1}")
        exit()
    if not os.path.exists(Musica2):
        print(f"❌ Arquivo 2 não existe: {Musica2}")
        exit()
    
    # Mostra informações dos arquivos
    size1 = os.path.getsize(Musica1)
    size2 = os.path.getsize(Musica2)
    print(f"📊 Tamanhos: {size1} vs {size2} bytes (diferença: {abs(size1 - size2)} bytes)")
    
    # Analisa níveis disponíveis
    try:
        chart_data1 = extract_chart_data_only(Musica1)
        chart_data2 = extract_chart_data_only(Musica2)
        diff_info1 = extract_difficulty_info(Musica1)
        diff_info2 = extract_difficulty_info(Musica2)
        
        print(f"\n📁 Níveis disponíveis:")
        for i, info in enumerate(diff_info1):
            if i < len(chart_data1):
                print(f"   Nível {i}: {info['difficulty']} ({info['rating']}) - {len(chart_data1[i])} linhas")
        
        # Verifica se o nível escolhido existe
        if Nivel >= len(chart_data1) or Nivel >= len(chart_data2):
            print(f"\n❌ Nível {Nivel} não existe! Máximo: {min(len(chart_data1), len(chart_data2))-1}")
            exit()
            
        # Mostra informações do nível escolhido
        nivel_info1 = diff_info1[Nivel] if Nivel < len(diff_info1) else {}
        nivel_info2 = diff_info2[Nivel] if Nivel < len(diff_info2) else {}
        print(f"\n🎯 Comparando nível {Nivel}:")
        print(f"   Arquivo 1: {nivel_info1.get('difficulty', 'N/A')} ({nivel_info1.get('rating', 'N/A')}) - {len(chart_data1[Nivel])} linhas")
        print(f"   Arquivo 2: {nivel_info2.get('difficulty', 'N/A')} ({nivel_info2.get('rating', 'N/A')}) - {len(chart_data2[Nivel])} linhas")
        
    except Exception as e:
        print(f"❌ Erro ao analisar arquivos: {e}")
        exit()
    
    # Executa a comparação
    print(f"\n🔄 Executando comparação...")
    try:
        compare_chart_data(Musica1, Musica2, level_index1=Nivel, level_index2=Nivel, output="resultado_comparacao.txt")
        print(f"✅ Comparação concluída!")
        print(f"📄 Resultado salvo em: resultado_comparacao.txt")
        
        # Mostra resumo
        try:
            with open("resultado_comparacao.txt", "r", encoding="utf-8") as f:
                content = f.read()
                if "Similaridade do chart data:" in content:
                    lines = content.split('\n')
                    for line in lines:
                        if "Similaridade do chart data:" in line or "Linhas diferentes:" in line:
                            print(f"   {line}")
        except:
            pass
            
    except Exception as e:
        print(f"❌ Erro durante comparação: {e}")
    
    print(f"\n🎵 Análise concluída! Verifique resultado_comparacao.txt para detalhes.")
