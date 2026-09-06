import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Diagnóstico Pluggy - Nicholas", layout="wide")

SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ3VnSkS3SR48P7huQS-PWlok-wEmocdpyu71vQ1jrZjTi_kHt4bWG6NXgy_3tfxh0mgifCxRiPRHQw/pub?output=csv"

@st.cache_data(ttl=600)
def carregar_dados_planilha():
    df = pd.read_csv(SHEET_CSV_URL)
    df['Valor (R$)'] = df['Valor (R$)'].replace({'R\$': '', '\.': '', ',': '.'}, regex=True)
    df['Valor (R$)'] = pd.to_numeric(df['Valor (R$)'], errors='coerce')
    return df

df_original = carregar_dados_planilha()

st.markdown("## 🔍 Painel de Diagnóstico da API Pluggy")

try:
    client_id = str(st.secrets["pluggy"]["client_id"]).strip()
    client_secret = str(st.secrets["pluggy"]["client_secret"]).strip()
    item_id = "6b12297a-5846-4732-8c6f-171717697388"
    
    # 1. Auth
    auth_res = requests.post("https://api.pluggy.ai/auth", json={"clientId": client_id, "clientSecret": client_secret})
    st.write(f"**Status Auth:** {auth_res.status_code}")
    
    if auth_res.status_code == 200:
        api_key = auth_res.json().get("apiKey")
        headers = {"X-API-KEY": api_key}
        
        # 2. Contas
        contas_res = requests.get(f"https://api.pluggy.ai/accounts?itemId={item_id}", headers=headers)
        st.write(f"**Status Accounts:** {contas_res.status_code}")
        st.json(contas_res.json())
        
        # 3. Transações
        trans_res = requests.get(f"https://api.pluggy.ai/transactions?itemId={item_id}", headers=headers)
        st.write(f"**Status Transactions:** {trans_res.status_code}")
        st.json(trans_res.json())
    else:
        st.error(f"Erro na autenticação: {auth_res.text}")

except Exception as e:
    st.error(f"Erro crítico: {e}")

st.markdown("---")
st.markdown("### Planilha Original")
st.dataframe(df_original, use_container_width=True)
