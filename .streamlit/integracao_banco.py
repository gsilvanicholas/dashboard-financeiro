import streamlit as st
import requests
import pandas as pd

# 1. Recuperando as credenciais de forma segura pelo Streamlit Secrets
try:
    CLIENT_ID = st.secrets["pluggy"]["client_id"]
    CLIENT_SECRET = st.secrets["pluggy"]["client_secret"]
except Exception:
    CLIENT_ID = None
    CLIENT_SECRET = None

def autenticar_pluggy():
    """Gera o token de acesso temporário na API da Pluggy."""
    url = "https://api.pluggy.ai/auth"
    payload = {
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("apiKey")
    else:
        return None

def buscar_extrato_bancario(api_key, item_id):
    """Busca as transações da conta vinculada através do Open Finance."""
    url = f"https://api.pluggy.ai/transactions?itemId={item_id}"
    headers = {"X-API-KEY": api_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

# Interface visual de teste no Streamlit
st.markdown("### 🔌 Módulo de Integração Open Finance")

if not CLIENT_ID or CLIENT_ID == "seu_client_id_aqui":
    st.warning("⚠️ Insira suas credenciais reais no arquivo `.streamlit/secrets.toml` no GitHub para prosseguir.")
else:
    token = autenticar_pluggy()
    if token:
        st.success("✅ Conexão estabelecida com sucesso com a API da Pluggy!")
        st.info("Próxima etapa: Vincular o ID da sua conta do Santander (itemId) para começar a listar os lançamentos.")
    else:
        st.error("❌ Falha na autenticação. Verifique se o Client ID e Client Secret estão corretos.")
