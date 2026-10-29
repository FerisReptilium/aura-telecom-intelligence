"""
=============================================================================
ARQUIVO: recommender.py
O QUE FAZ: Cérebro Matemático do Projeto AURA.
FUNÇÃO: Calcula a distância euclidiana ponderada, penalidades de franquia (H1) 
        e o fator de fidelidade por tempo de relacionamento em meses (H4).
=============================================================================
"""

import numpy as np
import pandas as pd

# ESCALAS FIXAS DE NORMALIZAÇÃO:
# Padronizam grandezas diferentes (GB, Minutos, Streaming, Mobilidade) para o cálculo.
ESCALAS = np.array([100.0, 2500.0, 50.0, 3.0])

# PESOS PADRÃO DA MATRIZ:
# Dados (40%), Voz (25%), Streaming (20%), Mobilidade (15%).
PESOS_PADRAO = np.array([0.40, 0.25, 0.20, 0.15])

def recomendar_planos(df_catalogo, dados_gb, minutos, streaming, mobilidade, meses_relacionamento=12, pesos_personalizados=None):
    """
    Calcula e retorna os top 3 melhores planos considerando o perfil, 
    as penalidades de insuficiência e o tempo de fidelidade do cliente.
    """
    if df_catalogo is None or df_catalogo.empty:
        return pd.DataFrame()
        
    pesos = pesos_personalizados if pesos_personalizados is not None else PESOS_PADRAO
    usuario = np.array([dados_gb, minutos, streaming, mobilidade], dtype=float)
    
    scores = []
    dados_suficientes_list = []
    minutos_suficientes_list = []
    
    for _, plano in df_catalogo.iterrows():
        plano_vetor = np.array([
            plano.get('franquia_gb', 0),
            plano.get('minutos_inclusos', 0),
            plano.get('streaming_horas_referencia', 0),
            plano.get('cobertura_mobilidade', 0)
        ], dtype=float)
        
        # 1. Normalização matemática das diferenças
        diff = (usuario - plano_vetor) / ESCALAS
        
        # 2. Penalidades comerciais (Validação H1: Franquia insuficiente gera risco de Churn)
        penalidade_dados = 2.0 if plano.get('franquia_gb', 0) < dados_gb else 0.0
        penalidade_minutos = 1.5 if plano.get('minutos_inclusos', 0) < minutos else 0.0
        
        # 3. Fator de fidelidade temporal (Validação H4: Meses de relacionamento reduzem o risco)
        fator_fidelidade = max(0.85, 1.0 - (meses_relacionamento / 120.0))
        
        # 4. Cálculo da Distância Euclidiana Ponderada com fator de retenção
        distancia = (np.sqrt(np.sum(pesos * (diff ** 2))) + penalidade_dados + penalidade_minutos) * fator_fidelidade
        
        scores.append(distancia)
        dados_suficientes_list.append(plano.get('franquia_gb', 0) >= dados_gb)
        minutos_suficientes_list.append(plano.get('minutos_inclusos', 0) >= minutos)
        
    df_resultado = df_catalogo.copy()
    df_resultado['score_final'] = scores
    df_resultado['dados_suficientes'] = dados_suficientes_list
    df_resultado['minutos_suficientes'] = minutos_suficientes_list
    
    # Ordena pelo menor score (maior adequação) e retorna o pódio (top 3)
    df_resultado = df_resultado.sort_values(by='score_final').reset_index(drop=True)
    return df_resultado.head(3)