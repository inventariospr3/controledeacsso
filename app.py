import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔹 Caminho do arquivo de credenciais JSON
caminho_credenciais = "credenciais.json"  # Altere para o caminho correto

def conectar_google_sheets():
    """ Conecta ao Google Sheets e retorna a aba 'REGISTRO'. """
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        credenciais = ServiceAccountCredentials.from_json_keyfile_name(caminho_credenciais, scope)
        cliente = gspread.authorize(credenciais)
        
        nome_planilha = "Controle_Acesso"
        planilha = cliente.open(nome_planilha).worksheet("REGISTRO")  
        return planilha
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {e}")
        return None

def verificar_imei(imei):
    """ Verifica se o IMEI está cadastrado e retorna o resultado. """
    planilha = conectar_google_sheets()
    if not planilha:
        return "❌ Erro ao acessar a planilha"

    dados = planilha.get_all_records()
    
    for registro in dados:
        if str(registro["IMEI"]) == str(imei):
            return f"✅ Acesso Permitido: {registro['Nome']}"
    return "🚫 Acesso Negado: IMEI não cadastrado"

# 🔹 Criando a interface no Streamlit
st.title("📱 Controle de Acesso - IMEI")
st.write("Digite o IMEI do dispositivo para verificar o acesso.")

imei_digitado = st.text_input("Digite o IMEI:")

if st.button("Verificar"):
    if imei_digitado:
        resultado = verificar_imei(imei_digitado)
        st.success(resultado)
    else:
        st.warning("Por favor, digite um IMEI válido.")
