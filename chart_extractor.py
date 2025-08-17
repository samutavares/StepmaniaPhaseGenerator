"""
Chart Extractor Module

Este módulo contém funções para extrair, processar e manipular arquivos
de chart do StepMania (.sm).

Author: Generated for StepMania Analysis
"""

import os
import re
from typing import Dict, List, Tuple, Optional, Any


def read_file_with_encoding(file_path: str) -> str:
    """
    Lê arquivo tentando múltiplos encodings para compatibilidade.
    
    Args:
        file_path (str): Caminho para o arquivo a ser lido
        
    Returns:
        str: Conteúdo do arquivo
        
    Raises:
        Exception: Se não conseguir ler com nenhum encoding suportado
        
    Example:
        >>> content = read_file_with_encoding("chart.sm")
        >>> print(f"Arquivo lido com sucesso: {len(content)} caracteres")
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"Arquivo lido com encoding {encoding}: {file_path}")
            return content
        except UnicodeDecodeError:
            continue
    
    raise Exception(f"Não foi possível ler o arquivo {file_path} com nenhum encoding suportado")


def parse_sm_difficulties(sm_file_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Analisa arquivo SM e extrai todas as dificuldades disponíveis.
    
    Args:
        sm_file_path (str): Caminho para o arquivo .sm
        
    Returns:
        Dict[str, Dict[str, Any]]: Dicionário com dificuldades e seus dados
            Formato: {
                "difficulty_name": {
                    "metadata": [...],
                    "chart_data": "...",
                    "raw_section": "..."
                }
            }
            
    Raises:
        FileNotFoundError: Se o arquivo não existir
        
    Example:
        >>> difficulties = parse_sm_difficulties("song.sm")
        >>> print(list(difficulties.keys()))
        ['Hard', 'Medium', 'Easy', 'Beginner']
    """
    content = read_file_with_encoding(sm_file_path)
    
    difficulties = {}
    notes_sections = []
    
    # Encontra todas as seções #NOTES:
    start = 0
    while True:
        notes_start = content.find('#NOTES:', start)
        if notes_start == -1:
            break
        
        # Encontra o fim desta seção de notas
        next_notes = content.find('#NOTES:', notes_start + 1)
        if next_notes == -1:
            notes_section = content[notes_start:]
        else:
            notes_section = content[notes_start:next_notes]
        
        notes_sections.append(notes_section)
        start = notes_start + 1
    
    # Processa cada seção de notas
    for i, section in enumerate(notes_sections):
        lines = section.split('\n')
        metadata = []
        chart_data = []
        
        # Extrai metadados (primeiras 6 linhas após #NOTES:)
        parsing_metadata = True
        for line in lines[1:]:  # Pula linha #NOTES:
            line = line.strip()
            if parsing_metadata and ':' in line:
                metadata.append(line.strip(':').strip())
                if len(metadata) >= 5:  # Temos todos os metadados
                    parsing_metadata = False
            elif not parsing_metadata:
                # Estes são dados do chart
                if line and (len(line) == 4 and all(c in '0123' for c in line)) or line in [',', ';']:
                    chart_data.append(line)
        
        # Extrai informações da dificuldade
        if len(metadata) >= 3:
            game_type = metadata[0] if metadata[0] else "dance-single"
            author = metadata[1] if metadata[1] else ""
            difficulty = metadata[2] if metadata[2] else f"Difficulty_{i+1}"
            level = metadata[3] if len(metadata) > 3 else "0"
            
            # Cria nome legível
            display_name = f"{difficulty}"
            if author:
                display_name = f"{difficulty} ({author})"
            
            difficulties[display_name] = {
                'metadata': metadata,
                'chart_data': '\n'.join(chart_data),
                'raw_section': section
            }
    
    return difficulties


def choose_difficulty(difficulties: Dict[str, Dict], target_difficulty: str = "") -> Tuple[Optional[str], Optional[Dict]]:
    """
    Permite ao usuário escolher uma dificuldade específica.
    
    Args:
        difficulties (Dict[str, Dict]): Dicionário de dificuldades disponíveis
        target_difficulty (str, optional): Dificuldade específica para buscar
        
    Returns:
        Tuple[Optional[str], Optional[Dict]]: Nome da dificuldade escolhida e seus dados
        
    Example:
        >>> difficulties = parse_sm_difficulties("song.sm")
        >>> name, data = choose_difficulty(difficulties, "Hard")
        >>> print(f"Selecionado: {name}")
    """
    if not difficulties:
        print("Nenhuma dificuldade encontrada no arquivo SM!")
        return None, None
    
    if target_difficulty:
        # Tenta encontrar a dificuldade especificada
        for key in difficulties.keys():
            if target_difficulty.lower() in key.lower():
                print(f"Usando dificuldade especificada: {key}")
                return key, difficulties[key]
        print(f"Dificuldade '{target_difficulty}' não encontrada. Dificuldades disponíveis:")
    
    # Mostra dificuldades disponíveis
    print("\nDificuldades disponíveis:")
    diff_list = list(difficulties.keys())
    for i, diff in enumerate(diff_list, 1):
        print(f"{i}. {diff}")
    
    # Obtém escolha do usuário
    while True:
        try:
            choice = input(f"\nEscolha a dificuldade (1-{len(diff_list)}): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(diff_list):
                    selected = diff_list[idx]
                    print(f"Selecionado: {selected}")
                    return selected, difficulties[selected]
            print("Escolha inválida. Tente novamente.")
        except (ValueError, KeyboardInterrupt):
            print("Entrada inválida ou cancelado.")
            return None, None


def extract_chart_data(sm_file_path: str, target_difficulty: str = "") -> Tuple[str, str, Dict]:
    """
    Extrai dados de chart de uma dificuldade específica.
    
    Args:
        sm_file_path (str): Caminho para o arquivo .sm
        target_difficulty (str, optional): Dificuldade alvo
        
    Returns:
        Tuple[str, str, Dict]: Chart data, nome da dificuldade, dados da dificuldade
        
    Example:
        >>> chart, name, data = extract_chart_data("song.sm", "Hard")
        >>> print(f"Chart extraído para {name}")
    """
    difficulties = parse_sm_difficulties(sm_file_path)
    difficulty_name, difficulty_data = choose_difficulty(difficulties, target_difficulty)
    
    if not difficulty_data:
        return "", "", {}
    
    return difficulty_data['chart_data'], difficulty_name, difficulty_data


def count_steps_by_track(chart_data: str) -> Dict[int, int]:
    """
    Conta o número de passos por track no chart.
    
    Args:
        chart_data (str): Dados do chart no formato SM
        
    Returns:
        Dict[int, int]: Dicionário com contagem {track_id: count}
        
    Example:
        >>> counts = count_steps_by_track(chart_data)
        >>> print(counts)
        {0: 15, 1: 12, 2: 18, 3: 14}
    """
    lines = [line.strip() for line in chart_data.replace(',', '').replace(';', '').splitlines() if line.strip()]
    
    step_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    for line in lines:
        if len(line) == 4:
            for i, char in enumerate(line):
                if char == '1':
                    step_counts[i] += 1
    
    return step_counts


def extract_original_metadata(sm_content: str) -> Dict[str, str]:
    """
    Extrai metadados originais do arquivo SM.
    
    Args:
        sm_content (str): Conteúdo completo do arquivo SM
        
    Returns:
        Dict[str, str]: Dicionário com metadados extraídos
        
    Example:
        >>> metadata = extract_original_metadata(sm_content)
        >>> print(metadata['title'])
        'Telephone'
    """
    metadata = {
        'title': '',
        'artist': '',
        'music': '',
        'offset': '0.000',
        'bpms': '0.000=120.000'
    }
    
    for line in sm_content.split('\n'):
        line = line.strip()
        if line.startswith('#TITLE:'):
            metadata['title'] = line.split(':', 1)[1].strip(';')
        elif line.startswith('#ARTIST:'):
            metadata['artist'] = line.split(':', 1)[1].strip(';')
        elif line.startswith('#MUSIC:'):
            metadata['music'] = line.split(':', 1)[1].strip(';')
        elif line.startswith('#OFFSET:'):
            metadata['offset'] = line.split(':', 1)[1].strip(';')
        elif line.startswith('#BPMS:'):
            metadata['bpms'] = line.split(':', 1)[1].strip(';')
    
    return metadata


def save_modified_chart(original_path: str, chart_content: str, difficulty_name: str, 
                       difficulty_data: Dict, original_content: str) -> str:
    """
    Salva uma versão modificada do chart na mesma pasta do original.
    
    Args:
        original_path (str): Caminho do arquivo original
        chart_content (str): Novo conteúdo do chart
        difficulty_name (str): Nome da dificuldade modificada
        difficulty_data (Dict): Dados da dificuldade original
        original_content (str): Conteúdo original completo do arquivo
        
    Returns:
        str: Caminho do arquivo salvo
        
    Example:
        >>> path = save_modified_chart("song.sm", new_chart, "Hard", data, content)
        >>> print(f"Arquivo salvo em: {path}")
    """
    original_dir = os.path.dirname(original_path)
    original_name = os.path.splitext(os.path.basename(original_path))[0]
    
    # Inclui nome da dificuldade no arquivo (remove texto entre parênteses)
    # Remove tudo entre parênteses e espaços extras
    clean_difficulty = re.sub(r'\s*\([^)]*\)', '', difficulty_name).strip()
    safe_difficulty = clean_difficulty.replace(' ', '_')
    new_filename = f"{original_name}_{safe_difficulty}_LearnMode.sm"
    new_filepath = os.path.join(original_dir, new_filename)
    
    # Encontra e substitui apenas a seção da dificuldade selecionada
    if difficulty_data and 'raw_section' in difficulty_data:
        raw_section = difficulty_data['raw_section']
        
        # Encontra a posição desta dificuldade específica no arquivo original
        section_start = original_content.find(raw_section)
        
        if section_start != -1:
            section_end = section_start + len(raw_section)
            
            # Reconstrói a seção de dados do chart com metadados
            metadata_lines = ["#NOTES:"]
            for meta in difficulty_data['metadata']:
                metadata_lines.append(f"     {meta}:")
            
            new_section = '\n'.join(metadata_lines) + '\n' + chart_content + '\n'
            
            # Substitui apenas esta seção
            new_content = (original_content[:section_start] + 
                          new_section + 
                          original_content[section_end:])
            
            # Adiciona "Learning Mode" ao subtitle de forma simples
            new_content = new_content.replace('#SUBTITLE:;', '#SUBTITLE:Learning Mode;')
        else:
            print("⚠️ Aviso: Não foi possível encontrar a seção da dificuldade selecionada no arquivo original")
            new_content = original_content
    else:
        # Fallback: extrai metadados originais e cria estrutura básica
        metadata = extract_original_metadata(original_content)
        
        # Cria estrutura básica com metadados originais e Learning Mode no subtitle
        new_content = f"""#TITLE:{metadata['title']};
#SUBTITLE:Learning Mode;
#ARTIST:{metadata['artist']};
#MUSIC:{metadata['music']};
#OFFSET:{metadata['offset']};
#BPMS:{metadata['bpms']};

#NOTES:
     dance-single:
     :
     Beginner:
     1:
     0,0,0,0,0:
{chart_content}
"""
    
    # Salva o novo arquivo
    with open(new_filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return new_filepath