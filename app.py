import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA (Tema Escuro Neon)
st.set_page_config(page_title="Dashboard Financeiro Executivo", layout="wide", initial_sidebar_state="expanded")

# CSS personalizado para customizar o fundo geral e destacar os blocos
st.markdown("""
    <style>
    .main {
        background-color: #0b091a;
    }
    h1, h2, h3 {
        color: #00f2fe !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stMetric {
        background-color: #16122d;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #7f00ff;
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
    # --- PAINEL LATERAL DE FILTROS INTERATIVOS ---
    st.sidebar.markdown("## 🎛️ Filtros Interativos")
    st.sidebar.markdown("Refine a exibição dos seus dados em tempo real:")

    # Filtro por Tipo
    tipos_disponiveis = df_original['Tipo'].unique().tolist()
    tipo_selecionado = st.sidebar.multiselect("Filtrar por Tipo", options=tipos_disponiveis, default=tipos_disponiveis)

    # Filtro por Categoria
    categorias_disponiveis = df_original['Categoria'].unique().tolist()
    categoria_selecionada = st.sidebar.multiselect("Filtrar por Categoria", options=categorias_disponiveis, default=categorias_disponiveis)

    # Aplicando os filtros ao DataFrame
    df = df_original[
        (df_original['Tipo'].isin(tipo_selecionado)) & 
        (df_original['Categoria'].isin(categoria_selecionada))
    ]

    # 2. CÁLCULOS E MÉTRICAS COM BASE NOS FILTROS
    receitas = df[df['Tipo'] == 'Receita']['Valor (R$)'].sum()
    despesas = df[df['Tipo'] == 'Despesa']['Valor (R$)'].sum()
    investimentos = df[df['Tipo'] == 'Investimento']['Valor (R$)'].sum()
    saldo_livre = receitas - despesas - investimentos
    
    # Média de renda total bruta para taxas (referência do total original)
    receita_total_base = df_original[df_original['Tipo'] == 'Receita']['Valor (R$)'].sum()
    taxa_poupanca = (investimentos / receita_total_base * 100) if receita_total_base > 0 else 0
    comprometimento_imovel = (df_original[df_original['Categoria'] == 'Parcela Apartamento']['Valor (R$)'].sum() / receita_total_base * 100) if receita_total_base > 0 else 0

    # TÍTULO
    st.markdown("<h1 style='text-align: center; text-shadow: 0px 0px 10px rgba(0,242,254,0.5);'>⚡ DASHBOARD FINANCEIRO EXECUTIVO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a09cb0;'>Controle Inteligente Santander • Roxo Neon & Azul Celeste</p>", unsafe_allow_html=True)
    st.markdown("---")

    # LINHA 1: CARTÕES DE KPIS (Estilo Neon)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div style='background: linear-gradient(135deg, #16122d, #1f1b3c); padding:20px; border-radius:12px; border-left: 5px solid #00f2fe; box-shadow: 0 4px 15px rgba(0,0,0,0.5);'>"
                    f"<h4 style='color:#a09cb0; margin:0; font-size:12px;'>RENDA TOTAL</h4>"
                    f"<h2 style='color:#00f2fe; margin:5px 0 0 0;'>R$ {receitas:,.2f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='background: linear-gradient(135deg, #16122d, #1f1b3c); padding:20px; border-radius:12px; border-left: 5px solid #ff007f; box-shadow: 0 4px 15px rgba(0,0,0,0.5);'>"
                    f"<h4 style='color:#a09cb0; margin:0; font-size:12px;'>DESPESAS TOTAIS</h4>"
                    f"<h2 style='color:#ff007f; margin:5px 0 0 0;'>R$ {despesas:,.2f}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='background: linear-gradient(135deg, #16122d, #1f1b3c); padding:20px; border-radius:12px; border-left: 5px solid #7f00ff; box-shadow: 0 4px 15px rgba(0,0,0,0.5);'>"
                    f"<h4 style='color:#a09cb0; margin:0; font-size:12px;'>PATRIMÔNIO & APORTES</h4>"
                    f"<h2 style='color:#b197fc; margin:5px 0 0 0;'>R$ {investimentos:,.2f}</h2></div>", unsafe_allow_html=True)
    with col4:
        cor_saldo = "#00e676" if saldo_livre >= 0 else "#ff007f"
        st.markdown(f"<div style='background: linear-gradient(135deg, #16122d, #1f1b3c); padding:20px; border-radius:12px; border-left: 5px solid {cor_saldo}; box-shadow: 0 4px 15px rgba(0,0,0,0.5);'>"
                    f"<h4 style='color:#a09cb0; margin:0; font-size:12px;'>SALDO LIVRE</h4>"
                    f"<h2 style='color:{cor_saldo}; margin:5px 0 0 0;'>R$ {saldo_livre:,.2f}</h2></div>", unsafe_allow_html=True)

    st.write("")

    # MÉTRICAS EXECUTIVAS
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Taxa de Poupança / Investimento", value=f"{taxa_poupanca:.1f}%")
    with m2:
        st.metric(label="Comprometimento com Imóvel", value=f"{comprometimento_imovel:.1f}%")
    with m3:
        st.metric(label="Movimentações Filtradas", value=int(len(df)))

    st.markdown("---")

    # GRÁFICOS VISUAIS INTERATIVOS
    col_graf1, col_graf2 = st.columns([2, 1])
    
    with col_graf1:
        st.markdown("### 📊 Detalhamento de Gastos (Despesas)")
        df_despesas = df[df['Tipo'] == 'Despesa'].groupby('Categoria')['Valor (R$)'].sum().reset_index()
        if not df_despesas.empty:
            fig_bar = px.bar(df_despesas, x='Valor (R$)', y='Categoria', orientation='h', text='Valor (R$)',
                             color_discrete_sequence=['#00f2fe'])
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            fig_bar.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside', marker_color='#00f2fe')
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Nenhuma despesa encontrada para os filtros selecionados.")

    with col_graf2:
        st.markdown("### 🍩 Composição Geral")
        df_composicao = df[df['Tipo'].isin(['Despesa', 'Investimento'])].groupby('Categoria')['Valor (R$)'].sum().reset_index()
        if not df_composicao.empty:
            fig_pie = px.pie(df_composicao, values='Valor (R$)', names='Categoria', hole=0.6,
                             color_discrete_sequence=['#00f2fe', '#7f00ff', '#ff007f', '#9b51e0', '#2d1b69'])
            fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Nenhum dado para exibir no gráfico.")

    st.markdown("### 📋 Histórico Detalhado Filtrado")
    st.dataframe(df[['ID', 'Data', 'Descrição', 'Tipo', 'Categoria', 'Valor (R$)', 'Status']], use_container_width=True)
