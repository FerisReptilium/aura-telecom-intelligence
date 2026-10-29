"""
=============================================================================
ARQUIVO: predictor.py
O QUE FAZ: Módulo de Machine Learning (Random Forest) para prever Churn.
=============================================================================
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def treinar_modelo_churn():
    np.random.seed(42)
    n = 1000
    consumo_gb = np.random.uniform(5, 100, n)
    meses = np.random.randint(1, 60, n)
    fatura = np.random.uniform(30, 250, n)
    reclamacoes = np.random.poisson(0.8, n)
    
    prob_churn = (reclamacoes * 0.3) + (fatura / 300) - (meses / 100) + np.random.normal(0, 0.1, n)
    y = (prob_churn > 0.5).astype(int)
    
    X = pd.DataFrame({'consumo_gb': consumo_gb, 'meses_relacionamento': meses, 'valor_fatura': fatura, 'reclamacoes': reclamacoes})
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    return clf

def prever_churn_cliente(consumo_gb, meses_relacionamento, valor_fatura, reclamacoes=0):
    modelo = treinar_modelo_churn()
    entrada = pd.DataFrame({'consumo_gb': [consumo_gb], 'meses_relacionamento': [meses_relacionamento], 'valor_fatura': [valor_fatura], 'reclamacoes': [reclamacoes]})
    return float(modelo.predict_proba(entrada)[0][1])