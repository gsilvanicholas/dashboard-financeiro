import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Painel Financeiro", layout="wide", initial_sidebar_state="collapsed")

# 2. CONEXÃO COM O GOOGLE SHEETS
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ3VnSkS3SR48P7huQS-PWlok-wEmocdpyu71vQ1jrZjTi_kHt4bWG6NXgy_3tfxh0mgifCxRiPRHQw/pub?output=csv"

@st.cache_data(ttl=600)
def carregar_dados():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        # Limpa o "R$" caso venha da planilha e converte para número
        df['Valor (R$)'] = df['Valor (R$)'].replace({'R\$': '', '\.': '', ',': '.'}, regex=True)
        df['Valor (R$)'] = pd.to_numeric(df['Valor (R$)'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

df = carregar_dados()

if not df.empty:
    # 3. CÁLCULOS DE KPI
    receitas = df[df['Tipo'] == 'Receita']['Valor (R$)'].sum()
    despesas = df[df['Tipo'] == 'Despesa']['Valor (R$)'].sum()
    investimentos = df[df['Tipo'] == 'Investimento']['Valor (R$)'].sum()
    saldo_livre = receitas - despesas - investimentos

    # 4. LAYOUT DO DASHBOARD
    st.markdown("<h1 style='text-align: center; color: #4facfe;'>Dashboard Financeiro Executivo</h1>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"<div style='background-color:#1e1e2f; padding:20px; border-radius:10px; border-left: 5px solid #4facfe;'>"
                    f"<h4 style='color:#a0a0b0; margin:0;'>Renda Total</h4>"
                    f"<h2 style='color:#ffffff; margin:0;'>R$ {receitas:,.2f}</h2>"
                    f"</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div style='background-color:#1e1e2f; padding:20px; border-radius:10px; border-left: 5px solid #ff4b4b;'>"
                    f"<h4 style='color:#a0a0b0; margin:0;'>Saídas Totais</h4>"
                    f"<h2 style='color:#ffffff; margin:0;'>R$ {despesas:,.2f}</h2>"
                    f"</div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div style='background-color:#1e1e2f; padding:20px; border-radius:10px; border-left: 5px solid #00c6ff;'>"
                    f"<h4 style='color:#a0a0b0; margin:0;'>Aportes & Patrimônio</h4>"
                    f"<h2 style='color:#ffffff; margin:0;'>R$ {investimentos:,.2f}</h2>"
                    f"</div>", unsafe_allow_html=True)

    with col4:
        cor_saldo = "#00e676" if saldo_livre >= 0 else "#ff4b4b"
        st.markdown(f"<div style='background-color:#1e1e2f; padding:20px; border-radius:10px; border-left: 5px solid {cor_saldo};'>"
                    f"<h4 style='color:#a0a0b0; margin:0;'>Saldo Livre</h4>"
                    f"<h2 style='color:{cor_saldo}; margin:0;'>R$ {saldo_livre:,.2f}</h2>"
                    f"</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")

    # 5. GRÁFICOS VISUAIS
    col_graf1, col_graf2 = st.columns([2, 1])

    with col_graf1:
        st.markdown("### Gastos por Categoria")
        df_despesas = df[df['Tipo'] == 'Despesa'].groupby('Categoria')['Valor (R$)'].sum().reset_index()
        fig_bar = px.bar(df_despesas, x='Valor (R$)', y='Categoria', orientation='h', text='Valor (R$)',
                         color_discrete_sequence=['#4facfe'])
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        fig_bar.update_traces(texttemplate='R$ %{text:,.2f}', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_graf2:
        st.markdown("### Distribuição de Despesas")
        fig_pie = px.pie(df_despesas, values='Valor (R$)', names='Categoria', hole=0.6,
                         color_discrete_sequence=px.colors.sequential.Teal)
        fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("### Histórico de Lançamentos")
    st.dataframe(df[['Data', 'Descrição', 'Categoria', 'Valor (R$)']], use_container_width=True)
