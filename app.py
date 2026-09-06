import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from pluggy_sdk import PluggyClient

# 1. CONFIGURAÇÃO DA PÁGINA (Layout Profissional Wide)
st.set_page_config(page_title="Controle Financeiro - Nicholas Henrique", layout="wide", initial_sidebar_state="collapsed")

# CSS Corporativo Avançado (Fundo Preto Profundo & Roxo Neon / Celeste)
st.markdown("""
    <style>
    .stApp {
        background-color: #07060d;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    .metric-card {
        background: #110f1f;
        border: 1px solid #26214a;
        padding: 18px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
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
        font-size: 22px;
        font-weight: 700;
    }
    h1, h2, h3, h4 {
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
    # --- HEADER EXECUTIVO ---
    st.markdown("<h2 style='color: #f1f0f5; font-weight: 700; margin-bottom: 0; letter-spacing: 0.5px;'>CONTROLE FINANCEIRO - NICHOLAS HENRIQUE GOMES DA SILVA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00f2fe; font-size: 13px; margin-top: 2px; font-weight: 500;'>SANTANDER EXEC // CORE DE MONITORAMENTO PATRIMONIAL</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #1f1b3c; margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

    # --- FILTROS NO TOPO ---
    with st.container():
        st.markdown("<p style='color: #b197fc; font-size: 13px; font-weight: 600; margin-bottom: 5px;'>🔍 PAINEL DE FILTRAGEM RÁPIDA</p>", unsafe_allow_html=True)
        f_col1, f_col2 = st.columns(2)
        
        tipos_disponiveis = df_original['Tipo'].unique().tolist()
        categorias_disponiveis = df_original['Categoria'].unique().tolist()
        
        with f_col1:
            tipo_selecionado = st.multiselect("Filtrar por Tipo de Transação", options=tipos_disponiveis, default=tipos_disponiveis)
        with f_col2:
            categoria_selecionada = st.multiselect("Filtrar por Categoria", options=categorias_disponiveis, default=categorias_disponiveis)

    df = df_original[
        (df_original['Tipo'].isin(tipo_selecionado)) & 
        (df_original['Categoria'].isin(categoria_selecionada))
    ]

    st.markdown("<br>", unsafe_allow_html=True)

    # CÁLCULOS DE KPIS
    receitas = df[df['Tipo'] == 'Receita']['Valor (R$)'].sum()
    despesas = df[df['Tipo'] == 'Despesa']['Valor (R$)'].sum()
    investimentos = df[df['Tipo'] == 'Investimento']['Valor (R$)'].sum()
    saldo_livre = receitas - despesas - investimentos
    
    receita_total_base = df_original[df_original['Tipo'] == 'Receita']['Valor (R$)'].sum()
    taxa_poupanca = (investimentos / receita_total_base * 100) if receita_total_base > 0 else 0
    comprometimento_imovel = (df_original[df_original['Categoria'] == 'Parcela Apartamento']['Valor (R$)'].sum() / receita_total_base * 100) if receita_total_base > 0 else 0
    
    total_despesas_qtd = len(df[df['Tipo'] == 'Despesa'])
    ticket_medio_despesa = (despesas / total_despesas_qtd) if total_despesas_qtd > 0 else 0

    # LINHA 1: KPIS PRINCIPAIS
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

    # LINHA 2: MÉTRICAS EXECUTIVAS SECUNDÁRIAS
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"""
            <div class="metric-card" style="padding: 14px;">
                <div class="metric-title">Taxa de Poupança</div>
                <div class="metric-value" style="font-size: 16px; color: #00f2fe;">{taxa_poupanca:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
            <div class="metric-card" style="padding: 14px;">
                <div class="metric-title">Comprometimento Imóvel</div>
                <div class="metric-value" style="font-size: 16px; color: #b197fc;">{comprometimento_imovel:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown(f"""
            <div class="metric-card" style="padding: 14px;">
                <div class="metric-title">Ticket Médio de Gastos</div>
                <div class="metric-value" style="font-size: 16px; color: #ff007f;">R$ {ticket_medio_despesa:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown(f"""
            <div class="metric-card" style="padding: 14px;">
                <div class="metric-title">Itens Filtrados</div>
                <div class="metric-value" style="font-size: 16px; color: #ffffff;">{int(len(df))} registros</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MÓDULO: PROGRESSO DA RESERVA DE EMERGÊNCIA & ALERTAS ---
    p_col1, p_col2 = st.columns([2, 1])
    with p_col1:
        st.markdown("<h4 style='color: #c9c5d4; font-size: 15px; font-weight: 600;'>🎯 Progresso da Meta: Reserva de Emergência</h4>", unsafe_allow_html=True)
        meta_reserva = 15000.0
        total_reserva_atual = df_original[(df_original['Categoria'] == 'Reserva') | (df_original['Categoria'] == 'Reserva de Emergência')]['Valor (R$)'].sum()
        progresso_val = min(total_reserva_atual / meta_reserva, 1.0)
        st.progress(progresso_val)
        st.markdown(f"<p style='color: #8b85a3; font-size: 12px;'>Acumulado atual: <b>R$ {total_reserva_atual:,.2f}</b> de uma meta de <b>R$ {meta_reserva:,.2f}</b> ({progresso_val*100:.1f}%)</p>", unsafe_allow_html=True)

    with p_col2:
        st.markdown("<h4 style='color: #c9c5d4; font-size: 15px; font-weight: 600;'>⚠️ Alertas Pendentes</h4>", unsafe_allow_html=True)
        pendentes = df_original[df_original['Status'].str.contains("Não Pago", case=False, na=False)]
        total_pendente = pendentes['Valor (R$)'].sum()
        st.markdown(f"""
            <div style="background: #19122c; border: 1px solid #ff007f; padding: 10px; border-radius: 6px;">
                <span style="color: #ff007f; font-weight: bold;">{len(pendentes)} contas pendentes</span><br>
                <span style="color: #ffffff; font-size: 14px;">Total: R$ {total_pendente:,.2f}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # GRÁFICOS ANALÍTICOS
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
    
    # --- BOTÃO DE INTEGRAÇÃO OPEN FINANCE (PLUGGY SDK OFICIAL) ---
    st.markdown("<h4 style='color: #00f2fe; font-size: 16px; font-weight: 600; margin-bottom: 8px;'>🔗 Conexão Bancária Automatizada (Open Finance)</h4>", unsafe_allow_html=True)
    
    def gerar_connect_token_sdk():
        try:
            client_id = st.secrets["pluggy"]["client_id"]
            client_secret = st.secrets["pluggy"]["client_secret"]
            
            # Inicializa o cliente oficial da Pluggy
            pluggy = PluggyClient(client_id=client_id, client_secret=client_secret)
            
            # Cria o connect token usando o método oficial do SDK
            connect_token_obj = pluggy.create_connect_token(client_user_id="nicholas-exec-user")
            return connect_token_obj.access_token
        except Exception as e:
            st.error(f"Erro ao gerar token oficial: {e}")
            return None

    if st.button("Conectar Conta do Santander"):
        connect_token = gerar_connect_token_sdk()
        if connect_token:
            widget_code = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <script src="https://api.pluggy.ai/connect.js"></script>
            </head>
            <body style="background-color: #07060d; color: white; margin: 0; padding: 20px; font-family: sans-serif; text-align: center;">
                <div id="root"></div>
                <script>
                    const client = new PluggyConnect({{
                        connectToken: "{connect_token}",
                        onSuccess: (data) => {{
                            document.getElementById("root").innerHTML = "<h2 style='color: #00e676;'>✅ Conta Conectada com Sucesso!</h2><p>Copie o seu Item ID:</p><code style='background: #110f1f; color: #00f2fe; padding: 12px; font-size: 16px; border-radius: 6px; display:inline-block;'>" + data.item.id + "</code>";
                        }},
                        onError: (error) => {{
                            document.getElementById("root").innerHTML = "<p style='color: #ff007f;'>Erro na conexão: " + JSON.stringify(error) + "</p>";
                        }}
                    }});
                    client.init();
                </script>
            </body>
            </html>
            """
            components.html(widget_code, height=650, scrolling=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- TABELA DE GASTOS EM DESTAQUE EXTREMO ---
    st.markdown("<h4 style='color: #00f2fe; font-size: 16px; font-weight: 600; margin-bottom: 12px;'>📋 Base de Transações e Lançamentos Detalhados</h4>", unsafe_allow_html=True)
    st.dataframe(
        df[['ID', 'Data', 'Descrição', 'Tipo', 'Categoria', 'Valor (R$)', 'Status']], 
        use_container_width=True,
        hide_index=True
    )
