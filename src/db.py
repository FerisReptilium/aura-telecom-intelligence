"""
=============================================================================
ARQUIVO: db.py
O QUE FAZ: É o "Guardião dos Dados".
FUNÇÃO: Carrega o catálogo do CSV local ou gera um catálogo padrão de segurança 
        para evitar qualquer erro caso o arquivo não seja encontrado.
=============================================================================
"""

import pandas as pd
import os

def carregar_catalogo_do_supabase():
    """
    Carrega o catálogo oficial de planos de telecomunicações. 
    Se o arquivo CSV não for encontrado, gera um DataFrame padrão de contingência.
    """
    caminho_csv = 'Projeto_1_Recomendador_de_Planos_Economia.csv'
    
    if os.path.exists(caminho_csv):
        try:
            df = pd.read_csv(caminho_csv)
            return df
        except Exception as e:
            print(f"Erro ao ler o CSV: {e}")
            
    # Catálogo padrão de contingência (caso o CSV não esteja na pasta)
    dados_padrao = {
        'nome': ['Aura Essencial', 'Aura Fibra Plus', 'Aura Premium Ultra', 'Aura Turbo Global'],
        'preco_mensal_brl': [49.90, 79.90, 119.90, 159.90],
        'franquia_gb': [15.0, 45.0, 90.0, 150.0],
        'minutos_inclusos': [300, 600, 1000, 2000],
        'streaming_horas_referencia': [4.0, 12.0, 25.0, 50.0],
        'cobertura_mobilidade': [1, 2, 2, 3],
        'regiao': ['urbana', 'periférica', 'urbana', 'rural']
    }
    return pd.DataFrame(dados_padrao)