"""
Replay Extractor Module

Este módulo contém funções para extrair e processar dados de replay
de arquivos do Etterna/StepMania.

Author: Generated for StepMania Analysis
"""

import os
import glob
from typing import Optional, List, Dict, Any
import pandas as pd


def get_latest_replay_data(replays_dir: str) -> Optional[str]:
    """
    Extrai dados do arquivo de replay mais recente na pasta especificada.
    
    Args:
        replays_dir (str): Caminho para a pasta de replays
        
    Returns:
        Optional[str]: Conteúdo do arquivo de replay mais recente, ou None se não encontrado
        
    Raises:
        FileNotFoundError: Se a pasta de replays não existir
        Exception: Se não conseguir ler nenhum arquivo
        
    Example:
        >>> data = get_latest_replay_data("C:/Games/Etterna/Save/ReplaysV2")
        >>> if data:
        ...     print("Replay carregado com sucesso")
    """
    if not os.path.exists(replays_dir):
        raise FileNotFoundError(f"Pasta de replays não encontrada: {replays_dir}")
    
    # Pega todos os arquivos da pasta
    all_files = glob.glob(os.path.join(replays_dir, "*"))
    
    if not all_files:
        return None
    
    # Pega o arquivo mais recente
    latest_file = max(all_files, key=os.path.getctime)
    
    # Lê o arquivo
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Replay carregado: {latest_file}")
        return content
    except Exception as e:
        print(f"Erro ao ler replay: {e}")
        return None


def parse_replay_data(data_str: str) -> pd.DataFrame:
    """
    Converte dados brutos de replay em DataFrame estruturado.
    
    Args:
        data_str (str): String contendo dados de replay no formato "row offset track"
        
    Returns:
        pd.DataFrame: DataFrame com colunas ['row', 'offset', 'track']
        
    Raises:
        ValueError: Se os dados não estiverem no formato esperado
        
    Example:
        >>> data = "768 -0.019590 2\\n960 -0.014393 0"
        >>> df = parse_replay_data(data)
        >>> print(df.columns.tolist())
        ['row', 'offset', 'track']
    """
    rows = []
    
    for line in data_str.strip().splitlines():
        try:
            parts = line.split()
            if len(parts) < 3:
                continue
                
            row_index = int(parts[0])
            offset = float(parts[1])
            tracks = list(map(int, parts[2:]))
            
            for track in tracks:
                rows.append({"row": row_index, "offset": offset, "track": track})
        except (ValueError, IndexError) as e:
            print(f"Linha inválida ignorada: {line} - Erro: {e}")
            continue
    
    if not rows:
        raise ValueError("Nenhum dado válido encontrado nos dados de replay")
    
    return pd.DataFrame(rows)


def classify_judgment(offset: float) -> str:
    """
    Classifica um offset de timing em categoria de julgamento.
    
    Args:
        offset (float): Offset de timing em segundos
        
    Returns:
        str: Categoria de julgamento ('W1 (Flawless)', 'W2 (Perfect)', etc.)
        
    Example:
        >>> classify_judgment(0.01)
        'W1 (Flawless)'
        >>> classify_judgment(0.1)
        'W4 (Good)'
    """
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


def analyze_performance(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analisa performance do jogador baseado nos dados de replay.
    
    Args:
        df (pd.DataFrame): DataFrame com dados de replay processados
        
    Returns:
        Dict[str, Any]: Dicionário com estatísticas de performance
        
    Example:
        >>> df = parse_replay_data(replay_data)
        >>> stats = analyze_performance(df)
        >>> print(stats['judgment_counts'])
    """
    # Adiciona classificação de julgamento
    df["judgment"] = df["offset"].apply(classify_judgment)
    
    # Mapeamento de nomes para as tracks
    track_names = {
        0: "Seta Esquerda",
        1: "Seta Baixo", 
        2: "Seta Cima",
        3: "Seta Direita"
    }
    
    # Contagem por track e julgamento
    counts = df.groupby(['track', 'judgment']).size().reset_index(name='count')
    totals = df.groupby('track').size().reset_index(name='total')
    counts = counts.merge(totals, on='track')
    counts['percentage'] = (counts['count'] / counts['total'] * 100).round(2)
    counts['track_name'] = counts['track'].map(track_names)
    
    performance_stats = counts[['track', 'track_name', 'judgment', 'count', 'total', 'percentage']]
    
    return {
        'dataframe': df,
        'performance_stats': performance_stats,
        'judgment_counts': df["judgment"].value_counts().sort_index(),
        'track_names': track_names
    }