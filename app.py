import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA (Layout Profissional Wide)
st.set_page_config(page_title="Enterprise Financial System", layout="wide", initial_sidebar_state="expanded")

# CSS Corporativo Estilo BI System
st.markdown("""
    <style>
    .stApp {
        background-color: #07060d;
    }
    /* Estilização da Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0d0b16;
        border-right: 1px solid #1f1b3c;
    }
    /* Cards de Métricas Estilo Enterprise */
    .metric-card {
        background: #110f1f;
        border: 1px solid #26214a;
        padding: 20px;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .metric-title {
        color: #8b85a3;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 24px;
        font-weight: 700;
    }
    /* Ajuste de Títulos */
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ3VnSkS3SR48P7huQS-PWlok-wEmocdpyu71vQ1jrZjTi_kHt4bWG6NXgy_3tfxh0mgifCxRiPRHQw/pub?output=csv"

@st.cache_data(ttl=600)
def carregar_dados():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df['Valor (R$)'] = df['Valor (R$)'].replace({'R\$': '', '\.': '', ',': '.'}, regex=True)
        df['Valor (R$)'] = pd.to_numeric(df['Valor (R$)'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df_original = carregar_dados()

if not df_original.empty:
    # --- SIDEBAR DE FILTROS CORPORATIVOS ---
    st.sidebar.markdown("### 🎛️ Painel de Filtros")
    st.sidebar.markdown("---")

    tipos_disponiveis = df_original['Tipo'].unique().tolist()
    tipo_selecionado = st.sidebar.multiselect("Filtrar por Tipo", options=tipos_disponiveis, default=tipos_disponiveis)

    categorias_disponiveis = df_original['Categoria'].unique().tolist()
    categoria_selecionada = st.sidebar.multiselect("Filtrar por Categoria", options=categorias_disponiveis, default=categorias_disponiveis)

    df = df_original[
        (df_original['Tipo'].isin(tipo_selecionado)) & 
        (df_original['Categoria'].isin(categoria_selecionada))
    ]

    # CÁLCULOS
    receitas = df[df['Tipo'] == 'Receita']['Valor (R$)'].sum()
    despesas = df[df['Tipo'] == 'Despesa']['Valor (R$)'].sum()
    investimentos = df[df['Tipo'] == 'Investimento']['Valor (R$)'].sum()
    saldo_livre = receitas - despesas - investimentos
    
    receita_total_base = df_original[df_original['Tipo'] == 'Receita']['Valor (R$)'].sum()
    taxa_poupanca = (investimentos / receita_total_base * 100) if receita_total_base > 0 else 0
    comprometimento_imovel = (df_original[df_original['Categoria'] == 'Parcela Apartamento']['Valor (R$)'].sum() / receita_total_base * 100) if receita_total_base > 0 else 0

    # HEADER DO SISTEMA
    st.markdown("<h2 style='color: #f1f0f5; font-weight: 600; margin-bottom: 0;'>SANTANDER EXEC // FINANCIAL CORE</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6e688a; font-size: 13px; margin-top: 2px;'>Módulo de Monitoramento de Ativos e Fluxo de Caixa</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #1f1b3c; margin-top: 10px; margin-bottom: 25px;'>", unsafe_allow_html=True)

    # LINHA 1: KPIS PRINCIPAIS (ESTILO SYSTEM CARDS)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #00f2fe;">
                <div class="metric-title">Renda Total Bruta</div>
                <div class="metric-value">R$ {receitas:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #ff007f;">
                <div class="metric-title">Despesas Totais</div>
                <div class="metric-value">R$ {despesas:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #7f00ff;">
                <div class="metric-title">Patrimônio & Aportes</div>
                <div class="metric-value">R$ {investimentos:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        cor_hex = "#00e676" if saldo_livre >= 0 else "#ff007f"
        st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {cor_hex};">
                <div class="metric-title">Saldo Livre Operacional</div>
                <div class="metric-value" style="color: {cor_hex};">R$ {saldo_livre:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # LINHA 2: INDICADORES EXECUTIVOS SECUNDÁRIOS
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"""
            <div class="metric-card" style="padding: 14px;">
                <div class="metric-title">Taxa de Poupança</div>
                <div class="metric-value" style="font-size: 18px; color: #00f2fe;">{taxa_poupanca:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
            <div class="metric-card" style="padding: 14px;">
                <div class="metric-title">Comprometimento Imobiliário</div>
                <div class="metric-value" style="font-size: 18px; color: #b197fc;">{comprometimento_imovel:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
            <div class="metric-card" style="padding: 14px;">
                <div class="metric-title">Registros Filtrados</div>
                <div class="metric-value" style="font-size: 18px; color: #ffffff;">{int(len(df))} itens</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # GRÁFICOS ANALÍTICOS (LAYOUT LIMPO)
    col_graf1, col_graf2 = st.columns([2, 1])
    
    with col_graf1:
        st.markdown("<h4 style='color: #c9c5d4; font-size: 15px; font-weight: 600;'>Análise de Custos por Categoria</h4>", unsafe_allow_html=True)
        df_despesas = df[df['Tipo'] == 'Despesa'].groupby('Categoria')['Valor (R$)'].sum().reset_index()
        if not df_despesas.empty:
            fig_bar = px.bar(df_despesas, x='Valor (R$)', y='Categoria', orientation='h', text='Valor (R$)',
                             color_discrete_sequence=['#00f2fe'])
            fig_bar.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='#8b85a3', size=11),
                margin=dict(t=10, b=10, l=10, r=10)
            )
            fig_bar.update_xaxis(showgrid=True, gridcolor='#1f1b3c')
            fig_bar.update_yaxis(showgrid=False)
            fig_bar.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside', marker_color='#00f2fe')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Sem dados de despesa para exibir.")

    with col_graf2:
        st.markdown("<h4 style='color: #c9c5d4; font-size: 15px; font-weight: 600;'>Composição de Saídas</h4>", unsafe_allow_html=True)
        df_composicao = df[df['Tipo'].isin(['Despesa', 'Investimento'])].groupby('Categoria')['Valor (R$)'].sum().reset_index()
        if not df_composicao.empty:
            fig_pie = px.pie(df_composicao, values='Valor (R$)', names='Categoria', hole=0.65,
                             color_discrete_sequence=['#00f2fe', '#7f00ff', '#ff007f', '#b197fc', '#3b287a'])
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='#8b85a3', size=11),
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Sem dados para o gráfico.")

    st.markdown("<hr style='border: 1px solid #1f1b3c; margin: 25px 0;'>", unsafe_allow_html=True)
    
    # TABELA EXECUTIVA DE DADOS
    st.markdown("<h4 style='color: #c9c5d4; font-size: 15px; font-weight: 600; margin-bottom: 15px;'>Base de Transações Detalhada</h4>", unsafe_allow_html=True)
    st.dataframe(
        df[['ID', 'Data', 'Descrição', 'Tipo', 'Categoria', 'Valor (R$)', 'Status']], 
        use_container_width=True,
        hide_index=True
    )
