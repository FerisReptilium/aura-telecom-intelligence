"""
=============================================================================
ARQUIVO: pdf_generator.py
O QUE FAZ: Geração automatizada de Propostas Comerciais em PDF (ReportLab).
=============================================================================
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def gerar_pdf_proposta(caminho_arquivo, dados_cliente, plano_campeao, economia):
    doc = SimpleDocTemplate(caminho_arquivo, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story, styles = [], getSampleStyleSheet()
    
    cor_primaria = colors.HexColor("#ff758c")
    cor_secundaria = colors.HexColor("#a18cd1")
    cor_texto = colors.HexColor("#2d3748")
    
    estilo_titulo = ParagraphStyle('TituloAura', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=cor_primaria, spaceAfter=4)
    estilo_sub = ParagraphStyle('SubAura', parent=styles['Normal'], fontName='Helvetica', fontSize=9, textColor=colors.HexColor("#718096"), spaceAfter=12)
    estilo_corpo = ParagraphStyle('CorpoAura', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, textColor=cor_texto, leading=13, spaceAfter=6)

    story.append(Paragraph("AURA TELECOM INTELLIGENCE", estilo_titulo))
    story.append(Paragraph("Proposta Comercial & Diagnóstico de Adequação de Planos (H1-H4)", estilo_sub))
    story.append(HRFlowable(width="100%", thickness=1.5, color=cor_primaria, spaceAfter=12))
    
    story.append(Paragraph("<b>📋 Dados do Cliente & Perfil Analisado</b>", estilo_corpo))
    t1 = Table([["Cliente:", dados_cliente.get('nome', 'Cliente VIP')], ["Tempo de Relacionamento:", f"{dados_cliente.get('meses', 12)} meses"], ["Tráfego Consumido:", f"{dados_cliente.get('consumo_gb', 22.0)} GB/mês"], ["Fatura Atual:", f"R$ {dados_cliente.get('fatura_atual', 99.90):.2f}"]], colWidths=[140, 360])
    t1.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f7fafc")), ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")), ('PADDING', (0,0), (-1,-1), 5), ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold')]))
    story.append(t1)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>🏆 Plano Recomendado (Pódio Otimizado AURA)</b>", estilo_corpo))
    t2 = Table([["Plano Recomendado:", plano_campeao.get('nome', 'Aura Fibra Plus')], ["Franquia de Dados:", f"{plano_campeao.get('franquia_gb', 45)} GB"], ["Nova Mensalidade:", f"R$ {plano_campeao.get('preco_mensal_brl', 79.90):.2f} / mês"], ["Impacto Financeiro:", f"<b>Economia de R$ {economia:.2f} / mês</b>" if economia >= 0 else f"Acréscimo de R$ {abs(economia):.2f}"]], colWidths=[140, 360])
    t2.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fff5f7")), ('BOX', (0,0), (-1,-1), 1, cor_primaria), ('PADDING', (0,0), (-1,-1), 5), ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold')]))
    story.append(t2)
    story.append(Spacer(1, 10))
    
    churn_score = dados_cliente.get('churn_score', 0.12)
    t3 = Table([["Probabilidade de Churn:", f"{churn_score * 100:.1f}%"], ["Diagnóstico Comercial:", "Baixo Risco (Cliente Fiel)" if churn_score < 0.3 else "Risco Moderado/Alto (Ação de Retenção)"]], colWidths=[140, 360])
    t3.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0f4f8")), ('BOX', (0,0), (-1,-1), 1, cor_secundaria), ('PADDING', (0,0), (-1,-1), 5), ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold')]))
    story.append(t3)
    
    doc.build(story)
    return caminho_arquivo