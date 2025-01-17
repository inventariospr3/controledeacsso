from google.colab import drive
from pyngrok import ngrok
import os

# 🔹 Montar o Google Drive
drive.mount('/content/drive')

# 🔹 Caminho para o arquivo JSON dentro do Google Drive
caminho_credenciais = "/content/drive/My Drive/Colab_Notebooks/credenciais.json"

# 🔹 Criar o arquivo do Streamlit diretamente no Colab
%%writefile app.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# 🔹 Conectar ao Google Sheets
def conectar_google_sheets():
    """ Conecta ao Google Sheets e retorna a aba 'REGISTRO'. """
    try:
        # 🔹 Configurar autenticação
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        credenciais = ServiceAccountCredentials.from_json_keyfile_name(caminho_credenciais, scope)
        cliente = gspread.authorize(credenciais)

        # 🔹 Abrir a planilha
        nome_planilha = "Controle_Acesso"
        planilha = cliente.open(nome_planilha).worksheet("REGISTRO")  # Nome da aba

        return planilha
    except gspread.SpreadsheetNotFound:
        st.error("❌ Erro: Planilha 'Controle_Acesso' não encontrada.")
        return None
    except gspread.WorksheetNotFound:
        st.error("❌ Erro: Aba 'REGISTRO' não encontrada.")
        return None
    except Exception as e:
        st.error(f"❌ Erro desconhecido: {e}")
        return None

# 🔹 Função de verificação de IMEI
def verificar_imei(imei):
    """ Verifica se o IMEI está na planilha e retorna a autorização. """
    planilha = conectar_google_sheets()
    if planilha is None:
        return "❌ Erro ao acessar a planilha"

    # 🔹 Buscar todos os registros
    dados = planilha.get_all_records()

    # 🔹 Verifica se o IMEI existe na base
    for registro in dados:
        if str(registro["IMEI"]) == str(imei):
            return f"✅ Acesso Permitido: {registro['Nome']}"
    return "🚫 Acesso Negado: IMEI não cadastrado"

# 🔹 Interface do Streamlit
st.title("Controle de Acesso - Verificação de IMEI")

# 🔹 Entrada de IMEI
imei_digitado = st.text_input("Digite o IMEI do dispositivo:")

if imei_digitado:
    resultado = verificar_imei(imei_digitado)
    st.write(resultado)
