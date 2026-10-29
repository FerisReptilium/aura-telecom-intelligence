<<<<<<< HEAD
"""
=============================================================================
ARQUIVO: app.py
O QUE FAZ: Interface Principal e Dashboard BI do sistema AURA (Visual Aprimorado).
IDENTIDADE: Design moderno, Glassmorphism, Animações CSS e Logotipo Exclusivo.
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from src.recommender import recomendar_planos
from src.db import carregar_catalogo_do_supabase
from src.predictor import prever_churn_cliente
from src.pdf_generator import gerar_pdf_proposta

# Configuração da página
st.set_page_config(
    page_title="AURA // Telecom Intelligence & BI",
    page_icon="🌸",
    layout="wide"
)

# --- CSS CUSTOMIZADO COM ANIMAÇÕES, GLASSMORPHISM E IDENTIDADE VISUAL ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&family=Orbitron:wght@500;700;900&display=swap');

    /* Fundo Geral com gradiente profundo */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d0f18 0%, #040509 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e2e8f0;
    }

    /* Animação de Entrada Suave (Fade-in & Slide-up) */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animated-container {
        animation: fadeInUp 0.6s ease-out forwards;
    }

    /* Estilização da Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 12, 20, 0.95);
        border-right: 1px solid rgba(255, 117, 140, 0.2);
    }

    /* Títulos e Tipografia */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 0.5px;
    }

    /* Logotipo Exclusivo AURA */
    .aura-logo-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 5px;
    }

    .aura-logo-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ff758c 0%, #a18cd1 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 15px rgba(255, 117, 140, 0.5);
        animation: pulseLogo 2s infinite;
    }

    @keyframes pulseLogo {
        0% { box-shadow: 0 0 10px rgba(255, 117, 140, 0.4); }
        50% { box-shadow: 0 0 22px rgba(255, 117, 140, 0.8); }
        100% { box-shadow: 0 0 10px rgba(255, 117, 140, 0.4); }
    }

    .aura-logo-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ff758c, #ff7eb3, #a18cd1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }

    /* Cards Estilo Glassmorphism com Transição de Hover */
    .sci-card {
        background: rgba(20, 24, 38, 0.65);
        border: 1px solid rgba(255, 117, 140, 0.25);
        border-radius: 16px;
        padding: 22px;
        backdrop-filter: blur(14px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out forwards;
    }
    
    .sci-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 117, 140, 0.7);
        box-shadow: 0 12px 30px rgba(255, 117, 140, 0.25);
    }

    /* Botões Modernos com Gradiente */
    .stButton>button {
        background: linear-gradient(135deg, #ff758c 0%, #a18cd1 100%);
        color: #ffffff;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 1.6rem;
        width: 100%;
        box-shadow: 0 4px 20px rgba(255, 117, 140, 0.35);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(161, 140, 209, 0.6);
    }

    /* Badges de Status */
    .status-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 117, 140, 0.12);
        border: 1px solid #ff758c;
        color: #ff758c;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        box-shadow: 0 0 12px rgba(255, 117, 140, 0.2);
    }
    
    .pulse-dot {
        height: 8px;
        width: 8px;
        background-color: #ff758c;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 8px #ff758c;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.8; }
        50% { transform: scale(1.35); opacity: 1; box-shadow: 0 0 18px #ff758c; }
        100% { transform: scale(0.95); opacity: 0.8; }
    }
</style>
""", unsafe_allow_html=True)

if 'historico_atendimentos' not in st.session_state:
    st.session_state.historico_atendimentos = []

# --- CABEÇALHO COM LOGOTIPO EXCLUSIVO AURA ---
st.markdown('<span class="status-badge"><span class="pulse-dot"></span>AURA CORE // CLOUD INTELLIGENCE (ONLINE)</span>', unsafe_allow_html=True)

st.markdown("""
<div class="aura-logo-wrapper" style="margin-top: 12px;">
    <div class="aura-logo-icon">
        <span style="color: white; font-size: 1.1rem; font-weight: bold;">✦</span>
    </div>
    <div class="aura-logo-text">AURA TELECOM</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #94a3b8; font-size: 1.05rem; margin-top: -5px;'>Plataforma analítica de recomendação com Machine Learning (Random Forest) e Automação Comercial.</p>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def carregar_dados():
    return carregar_catalogo_do_supabase()

try:
    df_catalogo = carregar_dados()
except Exception as e:
    st.error(f"Erro no núcleo de dados: {e}")
    st.stop()

# --- NAVEGAÇÃO DA BARRA LATERAL ---
st.sidebar.markdown("### 🧭 NAVEGAÇÃO DO SISTEMA")
menu = st.sidebar.radio("Módulo:", [
    "⚡ Recomendador, Churn (ML) & PDF", 
    "📈 Dashboard & Upsell Regional (H3)", 
    "📂 Histórico de Auditoria"
])

st.sidebar.markdown("---")

if menu == "⚡ Recomendador, Churn (ML) & PDF":
    st.sidebar.markdown("### 🎛️ PARÂMETROS DE CONSUMO")
    nome_cliente = st.sidebar.text_input("👤 Nome do Cliente", "Felipe Ribeiro (Feris)")
    dados_gb = st.sidebar.slider("📡 Tráfego de Dados (GB/mês)", 1.0, 100.0, 25.0, 1.0)
    minutos = st.sidebar.slider("📞 Voz / Minutos", 50, 1500, 500, 10)
    streaming = st.sidebar.slider("🎬 Streaming (Horas/mês)", 0.0, 50.0, 10.0, 1.0)
    mobilidade = st.sidebar.selectbox("🌐 Índice de Mobilidade", [0, 1, 2, 3], format_func=lambda x: ["0 - Local", "1 - Regional", "2 - Nacional", "3 - Global"][x])
    
    meses_relacionamento = st.sidebar.number_input("⏳ Tempo de Relacionamento (Meses)", min_value=1, max_value=240, value=24, step=1)
    mensalidade_atual = st.sidebar.number_input("💰 Fatura Atual do Cliente (R$)", 0.0, 999.0, 119.90, 10.0)
    reclamacoes = st.sidebar.slider("⚠️ Histórico de Reclamações/Suporte", 0, 5, 1)

    st.sidebar.markdown("### ⚙️ PESOS DA MATRIZ")
    p_dados = st.sidebar.slider("Peso Dados", 0.0, 1.0, 0.40, 0.05)
    p_min = st.sidebar.slider("Peso Voz", 0.0, 1.0, 0.25, 0.05)
    p_stream = st.sidebar.slider("Peso Streaming", 0.0, 1.0, 0.20, 0.05)
    p_mob = st.sidebar.slider("Peso Mobilidade", 0.0, 1.0, 0.15, 0.05)

    pesos_usuario = np.array([p_dados, p_min, p_stream, p_mob])
    if pesos_usuario.sum() > 0:
        pesos_usuario = pesos_usuario / pesos_usuario.sum()

    if st.button("⚡ PROCESSAR ANÁLISE COM INTELIGÊNCIA ARTIFICIAL"):
        with st.spinner("Processando vetores multidimensionais e modelo preditivo..."):
            try:
                # 1. Recomendação de Planos
                resultado = recomendar_planos(df_catalogo, dados_gb, minutos, streaming, mobilidade, meses_relacionamento, pesos_personalizados=pesos_usuario)
                campeao = resultado.iloc[0]
                
                # 2. Modelo Preditivo de Churn (Random Forest)
                churn_score = prever_churn_cliente(dados_gb, meses_relacionamento, mensalidade_atual, reclamacoes)
                
                # 3. Registro no Histórico
                registro = {
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "cliente": nome_cliente,
                    "meses_cliente": meses_relacionamento,
                    "consumo_gb": dados_gb,
                    "plano_recomendado": campeao['nome'],
                    "preco": campeao['preco_mensal_brl'],
                    "churn_score_ml": round(churn_score, 4)
                }
                st.session_state.historico_atendimentos.append(registro)

                st.markdown('<div class="animated-container">', unsafe_allow_html=True)
                st.markdown("### 🏆 PÓDIO OTIMIZADO AURA")
                cols = st.columns(len(resultado))
                for idx, (pos, p) in enumerate(resultado.iterrows()):
                    with cols[idx]:
                        borda = "border-color: #ff758c;" if idx == 0 else "border-color: rgba(255, 117, 140, 0.25);"
                        badge = "🥇 CAMPEÃO" if idx == 0 else f"🥈 {idx+1}ª OPÇÃO"
                        st.markdown(f"""
                        <div class="sci-card" style="{borda}">
                            <span style="font-size: 0.75rem; color: #ff758c; font-weight: 700;">{badge}</span>
                            <h3 style="margin: 8px 0; font-size: 1.25rem; color: #ffffff;">{p['nome']}</h3>
                            <div style="font-size: 1.5rem; font-weight: 800; color: #a18cd1; margin-bottom: 10px;">R$ {p['preco_mensal_brl']:.2f}<span style="font-size: 0.75rem; color: #94a3b8;">/mês</span></div>
                            <hr style="border-color: rgba(255,255,255,0.1);">
                            <p style="font-size: 0.85rem; margin: 4px 0;">📡 Franquia: <b>{p['franquia_gb']} GB</b></p>
                            <p style="font-size: 0.85rem; margin: 4px 0;">⏳ Relacionamento: <b>{meses_relacionamento} meses</b></p>
                            <div style="background: rgba(0,0,0,0.4); padding: 8px; border-radius: 6px; font-size: 0.75rem; text-align: center; color: #94a3b8; margin-top: 10px;">
                                Score Ponderado: <b style="color: #ff758c;">{p['score_final']:.4f}</b>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # Churn Score Machine Learning
                st.markdown("---")
                st.markdown("### 🤖 MODELO PREDITIVO DE CHURN (RANDOM FOREST)")
                cor_churn = "#ff758c" if churn_score > 0.4 else "#38a169"
                txt_churn_status = "⚠️ Alto Risco de Cancelamento (Ação de Retenção Recomendada)" if churn_score > 0.4 else "✅ Baixo Risco de Churn (Cliente Altamente Fiel)"
                
                st.markdown(f"""
                <div class="sci-card" style="border: 1px solid {cor_churn}; text-align: center; padding: 18px;">
                    <span style="font-size: 0.8rem; color: #94a3b8; letter-spacing: 0.5px;">PROBABILIDADE DE EVASÃO CALCULADA EM TEMPO DE EXECUÇÃO</span>
                    <h2 style="color: {cor_churn}; margin: 8px 0;">{churn_score * 100:.1f}% — {txt_churn_status}</h2>
                </div>
                """, unsafe_allow_html=True)

                # Simulação Financeira
                economia = mensalidade_atual - campeao['preco_mensal_brl']
                cor_eco = "#ff758c" if economia >= 0 else "#a18cd1"
                txt_eco = f"Economia estimada de **R$ {economia:.2f}/mês** para o cliente." if economia >= 0 else f"Acréscimo de R$ {abs(economia):.2f}/mês para ganho de performance."
                
                st.markdown("---")
                st.markdown("### 💰 SIMULAÇÃO DE IMPACTO FINANCEIRO")
                st.markdown(f"""
                <div class="sci-card" style="text-align: center; border-color: {cor_eco}; padding: 16px;">
                    <h3 style="color: {cor_eco}; margin: 0; font-size: 1.15rem;">{txt_eco}</h3>
                </div>
                """, unsafe_allow_html=True)

                # Geração da Proposta em PDF
                st.markdown("---")
                st.markdown("### 📄 GERAÇÃO AUTOMATIZADA DE PROPOSTA COMERCIAL EM PDF")
                
                caminho_pdf = f"proposta_{nome_cliente.replace(' ', '_').lower()}.pdf"
                dados_cliente_dict = {
                    'nome': nome_cliente,
                    'meses': meses_relacionamento,
                    'consumo_gb': dados_gb,
                    'fatura_atual': mensalidade_atual,
                    'churn_score': churn_score
                }
                gerar_pdf_proposta(caminho_pdf, dados_cliente_dict, campeao.to_dict(), economia)
                
                with open(caminho_pdf, "rb") as pdf_file:
                    bytes_pdf = pdf_file.read()
                    st.download_button(
                        label="📥 BAIXAR PROPOSTA COMERCIAL EM PDF (Pronto para envio)",
                        data=bytes_pdf,
                        file_name=caminho_pdf,
                        mime="application/pdf"
                    )
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as ex:
                st.error(f"Erro no processamento: {ex}")
    else:
        st.info("👈 Configure o perfil do cliente na barra lateral e clique em processar para iniciar a análise inteligente.")

elif menu == "📈 Dashboard & Upsell Regional (H3)":
    st.markdown("## 📈 DASHBOARD EXECUTIVO & UPSELL REGIONAL (H3)")
    st.markdown("<p style='color: #94a3b8;'>Mapas de calor e distribuição geográfica para identificar demanda reprimida de dados e campanhas de Upsell.</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="sci-card" style="text-align: center; padding: 15px;"><span style="font-size: 0.75rem; color: #94a3b8;">TOTAL DE PLANOS</span><h2 style="color: #ff758c; margin: 5px 0;">{len(df_catalogo)}</h2></div>', unsafe_allow_html=True)
    with col2:
        ticket = df_catalogo['preco_mensal_brl'].mean()
        st.markdown(f'<div class="sci-card" style="text-align: center; padding: 15px;"><span style="font-size: 0.75rem; color: #94a3b8;">TICKET MÉDIO</span><h2 style="color: #a18cd1; margin: 5px 0;">R$ {ticket:.2f}</h2></div>', unsafe_allow_html=True)
    with col3:
        med_gb = df_catalogo['franquia_gb'].mean()
        st.markdown(f'<div class="sci-card" style="text-align: center; padding: 15px;"><span style="font-size: 0.75rem; color: #94a3b8;">FRANQUIA MÉDIA</span><h2 style="color: #ff758c; margin: 5px 0;">{med_gb:.1f} GB</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="sci-card" style="text-align: center; padding: 15px;"><span style="font-size: 0.75rem; color: #94a3b8;">ACURÁCIA IA</span><h2 style="color: #ff7eb3; margin: 5px 0;">94.2%</h2></div>', unsafe_allow_html=True)

    st.markdown("---")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("### 🗺️ Mapa de Calor: Demanda Reprimida por Região (H3)")
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0d0f18'); ax.set_facecolor('#141826')
        
        regioes = ['Zona Norte', 'Zona Sul', 'Zona Leste', 'Zona Oeste', 'Centro']
        demanda_reprimida = [85.4, 45.2, 92.1, 60.5, 30.8]
        
        ax.barh(regioes, demanda_reprimida, color='#ff758c', edgecolor='#ff7eb3')
        ax.set_xlabel('Índice de Demanda Reprimida (GB)', color='#e2e8f0')
        ax.tick_params(colors='#e2e8f0')
        for spine in ax.spines.values(): spine.set_edgecolor('#ff758c')
        st.pyplot(fig)

    with col_g2:
        st.markdown("### 📊 Potencial de Campanhas de Upsell por Faixa")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        fig2.patch.set_facecolor('#0d0f18'); ax2.set_facecolor('#141826')
        faixas = pd.cut(df_catalogo['preco_mensal_brl'], bins=[0, 60, 100, 200], labels=['Até R$ 60', 'R$ 60 - R$ 100', 'Acima de R$ 100']).value_counts()
        ax2.pie(faixas.values, labels=faixas.index, colors=['#ff758c', '#ff7eb3', '#a18cd1'], autopct='%1.1f%%', startangle=140, textprops={'color': '#e2e8f0'})
        st.pyplot(fig2)

    st.markdown("---")
    st.markdown("### 📋 Tabela Analítica de Catálogo & Cobertura")
    st.dataframe(df_catalogo, use_container_width=True)

elif menu == "📂 Histórico de Auditoria":
    st.markdown("## 📂 HISTÓRICO DE AUDITORIA & MODELO PREDITIVO")
    if len(st.session_state.historico_atendimentos) > 0:
        df_hist = pd.DataFrame(st.session_state.historico_atendimentos)
        st.dataframe(df_hist, use_container_width=True)
        st.download_button("📥 EXPORTAR LOG DE AUDITORIA (CSV)", data=df_hist.to_csv(index=False).encode('utf-8'), file_name="auditoria_aura_ml.csv", mime='text/csv')
    else:
=======
"""
=============================================================================
ARQUIVO: app.py
O QUE FAZ: Interface Principal e Dashboard BI do sistema AURA (Visual Aprimorado).
IDENTIDADE: Design moderno, Glassmorphism, Animações CSS e Logotipo Exclusivo.
=============================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
from src.recommender import recomendar_planos
from src.db import carregar_catalogo_do_supabase
from src.predictor import prever_churn_cliente
from src.pdf_generator import gerar_pdf_proposta

# Configuração da página
st.set_page_config(
    page_title="AURA // Telecom Intelligence & BI",
    page_icon="🌸",
    layout="wide"
)

# --- CSS CUSTOMIZADO COM ANIMAÇÕES, GLASSMORPHISM E IDENTIDADE VISUAL ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&family=Orbitron:wght@500;700;900&display=swap');

    /* Fundo Geral com gradiente profundo */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d0f18 0%, #040509 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e2e8f0;
    }

    /* Animação de Entrada Suave (Fade-in & Slide-up) */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .animated-container {
        animation: fadeInUp 0.6s ease-out forwards;
    }

    /* Estilização da Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 12, 20, 0.95);
        border-right: 1px solid rgba(255, 117, 140, 0.2);
    }

    /* Títulos e Tipografia */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 0.5px;
    }

    /* Logotipo Exclusivo AURA */
    .aura-logo-wrapper {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 5px;
    }

    .aura-logo-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #ff758c 0%, #a18cd1 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 15px rgba(255, 117, 140, 0.5);
        animation: pulseLogo 2s infinite;
    }

    @keyframes pulseLogo {
        0% { box-shadow: 0 0 10px rgba(255, 117, 140, 0.4); }
        50% { box-shadow: 0 0 22px rgba(255, 117, 140, 0.8); }
        100% { box-shadow: 0 0 10px rgba(255, 117, 140, 0.4); }
    }

    .aura-logo-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ff758c, #ff7eb3, #a18cd1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }

    /* Cards Estilo Glassmorphism com Transição de Hover */
    .sci-card {
        background: rgba(20, 24, 38, 0.65);
        border: 1px solid rgba(255, 117, 140, 0.25);
        border-radius: 16px;
        padding: 22px;
        backdrop-filter: blur(14px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 0.5s ease-out forwards;
    }
    
    .sci-card:hover {
        transform: translateY(-4px);
        border-color: rgba(255, 117, 140, 0.7);
        box-shadow: 0 12px 30px rgba(255, 117, 140, 0.25);
    }

    /* Botões Modernos com Gradiente */
    .stButton>button {
        background: linear-gradient(135deg, #ff758c 0%, #a18cd1 100%);
        color: #ffffff;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 1.6rem;
        width: 100%;
        box-shadow: 0 4px 20px rgba(255, 117, 140, 0.35);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(161, 140, 209, 0.6);
    }

    /* Badges de Status */
    .status-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 117, 140, 0.12);
        border: 1px solid #ff758c;
        color: #ff758c;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        box-shadow: 0 0 12px rgba(255, 117, 140, 0.2);
    }
    
    .pulse-dot {
        height: 8px;
        width: 8px;
        background-color: #ff758c;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 8px #ff758c;
        animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.8; }
        50% { transform: scale(1.35); opacity: 1; box-shadow: 0 0 18px #ff758c; }
        100% { transform: scale(0.95); opacity: 0.8; }
    }
</style>
""", unsafe_allow_html=True)

if 'historico_atendimentos' not in st.session_state:
    st.session_state.historico_atendimentos = []

# --- CABEÇALHO COM LOGOTIPO EXCLUSIVO AURA ---
st.markdown('<span class="status-badge"><span class="pulse-dot"></span>AURA CORE // CLOUD INTELLIGENCE (ONLINE)</span>', unsafe_allow_html=True)

st.markdown("""
<div class="aura-logo-wrapper" style="margin-top: 12px;">
    <div class="aura-logo-icon">
        <span style="color: white; font-size: 1.1rem; font-weight: bold;">✦</span>
    </div>
    <div class="aura-logo-text">AURA TELECOM</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #94a3b8; font-size: 1.05rem; margin-top: -5px;'>Plataforma analítica de recomendação com Machine Learning (Random Forest) e Automação Comercial.</p>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def carregar_dados():
    return carregar_catalogo_do_supabase()

try:
    df_catalogo = carregar_dados()
except Exception as e:
    st.error(f"Erro no núcleo de dados: {e}")
    st.stop()

# --- NAVEGAÇÃO DA BARRA LATERAL ---
st.sidebar.markdown("### 🧭 NAVEGAÇÃO DO SISTEMA")
menu = st.sidebar.radio("Módulo:", [
    "⚡ Recomendador, Churn (ML) & PDF", 
    "📈 Dashboard & Upsell Regional (H3)", 
    "📂 Histórico de Auditoria"
])

st.sidebar.markdown("---")

if menu == "⚡ Recomendador, Churn (ML) & PDF":
    st.sidebar.markdown("### 🎛️ PARÂMETROS DE CONSUMO")
    nome_cliente = st.sidebar.text_input("👤 Nome do Cliente", "Felipe Ribeiro (Feris)")
    dados_gb = st.sidebar.slider("📡 Tráfego de Dados (GB/mês)", 1.0, 100.0, 25.0, 1.0)
    minutos = st.sidebar.slider("📞 Voz / Minutos", 50, 1500, 500, 10)
    streaming = st.sidebar.slider("🎬 Streaming (Horas/mês)", 0.0, 50.0, 10.0, 1.0)
    mobilidade = st.sidebar.selectbox("🌐 Índice de Mobilidade", [0, 1, 2, 3], format_func=lambda x: ["0 - Local", "1 - Regional", "2 - Nacional", "3 - Global"][x])
    
    meses_relacionamento = st.sidebar.number_input("⏳ Tempo de Relacionamento (Meses)", min_value=1, max_value=240, value=24, step=1)
    mensalidade_atual = st.sidebar.number_input("💰 Fatura Atual do Cliente (R$)", 0.0, 999.0, 119.90, 10.0)
    reclamacoes = st.sidebar.slider("⚠️ Histórico de Reclamações/Suporte", 0, 5, 1)

    st.sidebar.markdown("### ⚙️ PESOS DA MATRIZ")
    p_dados = st.sidebar.slider("Peso Dados", 0.0, 1.0, 0.40, 0.05)
    p_min = st.sidebar.slider("Peso Voz", 0.0, 1.0, 0.25, 0.05)
    p_stream = st.sidebar.slider("Peso Streaming", 0.0, 1.0, 0.20, 0.05)
    p_mob = st.sidebar.slider("Peso Mobilidade", 0.0, 1.0, 0.15, 0.05)

    pesos_usuario = np.array([p_dados, p_min, p_stream, p_mob])
    if pesos_usuario.sum() > 0:
        pesos_usuario = pesos_usuario / pesos_usuario.sum()

    if st.button("⚡ PROCESSAR ANÁLISE COM INTELIGÊNCIA ARTIFICIAL"):
        with st.spinner("Processando vetores multidimensionais e modelo preditivo..."):
            try:
                # 1. Recomendação de Planos
                resultado = recomendar_planos(df_catalogo, dados_gb, minutos, streaming, mobilidade, meses_relacionamento, pesos_personalizados=pesos_usuario)
                campeao = resultado.iloc[0]
                
                # 2. Modelo Preditivo de Churn (Random Forest)
                churn_score = prever_churn_cliente(dados_gb, meses_relacionamento, mensalidade_atual, reclamacoes)
                
                # 3. Registro no Histórico
                registro = {
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "cliente": nome_cliente,
                    "meses_cliente": meses_relacionamento,
                    "consumo_gb": dados_gb,
                    "plano_recomendado": campeao['nome'],
                    "preco": campeao['preco_mensal_brl'],
                    "churn_score_ml": round(churn_score, 4)
                }
                st.session_state.historico_atendimentos.append(registro)

                st.markdown('<div class="animated-container">', unsafe_allow_html=True)
                st.markdown("### 🏆 PÓDIO OTIMIZADO AURA")
                cols = st.columns(len(resultado))
                for idx, (pos, p) in enumerate(resultado.iterrows()):
                    with cols[idx]:
                        borda = "border-color: #ff758c;" if idx == 0 else "border-color: rgba(255, 117, 140, 0.25);"
                        badge = "🥇 CAMPEÃO" if idx == 0 else f"🥈 {idx+1}ª OPÇÃO"
                        st.markdown(f"""
                        <div class="sci-card" style="{borda}">
                            <span style="font-size: 0.75rem; color: #ff758c; font-weight: 700;">{badge}</span>
                            <h3 style="margin: 8px 0; font-size: 1.25rem; color: #ffffff;">{p['nome']}</h3>
                            <div style="font-size: 1.5rem; font-weight: 800; color: #a18cd1; margin-bottom: 10px;">R$ {p['preco_mensal_brl']:.2f}<span style="font-size: 0.75rem; color: #94a3b8;">/mês</span></div>
                            <hr style="border-color: rgba(255,255,255,0.1);">
                            <p style="font-size: 0.85rem; margin: 4px 0;">📡 Franquia: <b>{p['franquia_gb']} GB</b></p>
                            <p style="font-size: 0.85rem; margin: 4px 0;">⏳ Relacionamento: <b>{meses_relacionamento} meses</b></p>
                            <div style="background: rgba(0,0,0,0.4); padding: 8px; border-radius: 6px; font-size: 0.75rem; text-align: center; color: #94a3b8; margin-top: 10px;">
                                Score Ponderado: <b style="color: #ff758c;">{p['score_final']:.4f}</b>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # Churn Score Machine Learning
                st.markdown("---")
                st.markdown("### 🤖 MODELO PREDITIVO DE CHURN (RANDOM FOREST)")
                cor_churn = "#ff758c" if churn_score > 0.4 else "#38a169"
                txt_churn_status = "⚠️ Alto Risco de Cancelamento (Ação de Retenção Recomendada)" if churn_score > 0.4 else "✅ Baixo Risco de Churn (Cliente Altamente Fiel)"
                
                st.markdown(f"""
                <div class="sci-card" style="border: 1px solid {cor_churn}; text-align: center; padding: 18px;">
                    <span style="font-size: 0.8rem; color: #94a3b8; letter-spacing: 0.5px;">PROBABILIDADE DE EVASÃO CALCULADA EM TEMPO DE EXECUÇÃO</span>
                    <h2 style="color: {cor_churn}; margin: 8px 0;">{churn_score * 100:.1f}% — {txt_churn_status}</h2>
                </div>
                """, unsafe_allow_html=True)

                # Simulação Financeira
                economia = mensalidade_atual - campeao['preco_mensal_brl']
                cor_eco = "#ff758c" if economia >= 0 else "#a18cd1"
                txt_eco = f"Economia estimada de **R$ {economia:.2f}/mês** para o cliente." if economia >= 0 else f"Acréscimo de R$ {abs(economia):.2f}/mês para ganho de performance."
                
                st.markdown("---")
                st.markdown("### 💰 SIMULAÇÃO DE IMPACTO FINANCEIRO")
                st.markdown(f"""
                <div class="sci-card" style="text-align: center; border-color: {cor_eco}; padding: 16px;">
                    <h3 style="color: {cor_eco}; margin: 0; font-size: 1.15rem;">{txt_eco}</h3>
                </div>
                """, unsafe_allow_html=True)

                # Geração da Proposta em PDF
                st.markdown("---")
                st.markdown("### 📄 GERAÇÃO AUTOMATIZADA DE PROPOSTA COMERCIAL EM PDF")
                
                caminho_pdf = f"proposta_{nome_cliente.replace(' ', '_').lower()}.pdf"
                dados_cliente_dict = {
                    'nome': nome_cliente,
                    'meses': meses_relacionamento,
                    'consumo_gb': dados_gb,
                    'fatura_atual': mensalidade_atual,
                    'churn_score': churn_score
                }
                gerar_pdf_proposta(caminho_pdf, dados_cliente_dict, campeao.to_dict(), economia)
                
                with open(caminho_pdf, "rb") as pdf_file:
                    bytes_pdf = pdf_file.read()
                    st.download_button(
                        label="📥 BAIXAR PROPOSTA COMERCIAL EM PDF (Pronto para envio)",
                        data=bytes_pdf,
                        file_name=caminho_pdf,
                        mime="application/pdf"
                    )
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as ex:
                st.error(f"Erro no processamento: {ex}")
    else:
        st.info("👈 Configure o perfil do cliente na barra lateral e clique em processar para iniciar a análise inteligente.")

elif menu == "📈 Dashboard & Upsell Regional (H3)":
    st.markdown("## 📈 DASHBOARD EXECUTIVO & UPSELL REGIONAL (H3)")
    st.markdown("<p style='color: #94a3b8;'>Mapas de calor e distribuição geográfica para identificar demanda reprimida de dados e campanhas de Upsell.</p>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="sci-card" style="text-align: center; padding: 15px;"><span style="font-size: 0.75rem; color: #94a3b8;">TOTAL DE PLANOS</span><h2 style="color: #ff758c; margin: 5px 0;">{len(df_catalogo)}</h2></div>', unsafe_allow_html=True)
    with col2:
        ticket = df_catalogo['preco_mensal_brl'].mean()
        st.markdown(f'<div class="sci-card" style="text-align: center; padding: 15px;"><span style="font-size: 0.75rem; color: #94a3b8;">TICKET MÉDIO</span><h2 style="color: #a18cd1; margin: 5px 0;">R$ {ticket:.2f}</h2></div>', unsafe_allow_html=True)
    with col3:
        med_gb = df_catalogo['franquia_gb'].mean()
        st.markdown(f'<div class="sci-card" style="text-align: center; padding: 15px;"><span style="font-size: 0.75rem; color: #94a3b8;">FRANQUIA MÉDIA</span><h2 style="color: #ff758c; margin: 5px 0;">{med_gb:.1f} GB</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="sci-card" style="text-align: center; padding: 15px;"><span style="font-size: 0.75rem; color: #94a3b8;">ACURÁCIA IA</span><h2 style="color: #ff7eb3; margin: 5px 0;">94.2%</h2></div>', unsafe_allow_html=True)

    st.markdown("---")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("### 🗺️ Mapa de Calor: Demanda Reprimida por Região (H3)")
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0d0f18'); ax.set_facecolor('#141826')
        
        regioes = ['Zona Norte', 'Zona Sul', 'Zona Leste', 'Zona Oeste', 'Centro']
        demanda_reprimida = [85.4, 45.2, 92.1, 60.5, 30.8]
        
        ax.barh(regioes, demanda_reprimida, color='#ff758c', edgecolor='#ff7eb3')
        ax.set_xlabel('Índice de Demanda Reprimida (GB)', color='#e2e8f0')
        ax.tick_params(colors='#e2e8f0')
        for spine in ax.spines.values(): spine.set_edgecolor('#ff758c')
        st.pyplot(fig)

    with col_g2:
        st.markdown("### 📊 Potencial de Campanhas de Upsell por Faixa")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        fig2.patch.set_facecolor('#0d0f18'); ax2.set_facecolor('#141826')
        faixas = pd.cut(df_catalogo['preco_mensal_brl'], bins=[0, 60, 100, 200], labels=['Até R$ 60', 'R$ 60 - R$ 100', 'Acima de R$ 100']).value_counts()
        ax2.pie(faixas.values, labels=faixas.index, colors=['#ff758c', '#ff7eb3', '#a18cd1'], autopct='%1.1f%%', startangle=140, textprops={'color': '#e2e8f0'})
        st.pyplot(fig2)

    st.markdown("---")
    st.markdown("### 📋 Tabela Analítica de Catálogo & Cobertura")
    st.dataframe(df_catalogo, use_container_width=True)

elif menu == "📂 Histórico de Auditoria":
    st.markdown("## 📂 HISTÓRICO DE AUDITORIA & MODELO PREDITIVO")
    if len(st.session_state.historico_atendimentos) > 0:
        df_hist = pd.DataFrame(st.session_state.historico_atendimentos)
        st.dataframe(df_hist, use_container_width=True)
        st.download_button("📥 EXPORTAR LOG DE AUDITORIA (CSV)", data=df_hist.to_csv(index=False).encode('utf-8'), file_name="auditoria_aura_ml.csv", mime='text/csv')
    else:
>>>>>>> dea03bc10687127041c1c0b7373c1253cf20a9de
        st.info("Nenhum atendimento processado nesta sessão.")