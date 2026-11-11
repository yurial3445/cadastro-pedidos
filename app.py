
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import datetime
import os

# Configurações do Banco de Dados
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "senha123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "pedidos_db")

# String de conexão SQLAlchemy
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}')

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id SERIAL PRIMARY KEY,
            data DATE,
            hora TIME,
            solicitante VARCHAR(100),
            assunto VARCHAR(255),
            descricao TEXT,
            prioridade VARCHAR(50)
        )
        """))

init_db()

st.title('Cadastro de Pedidos')

# Formulário de Cadastro
with st.form("cadastro_form"):
    data = st.date_input("Data", datetime.date.today())
    hora = st.time_input("Hora", datetime.datetime.now().time())
    solicitante = st.text_input("Solicitante")
    assunto = st.text_input("Assunto")
    descricao = st.text_area("Descrição")
    prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta"])
    
    submit_button = st.form_submit_button(label="Cadastrar Pedido")

if submit_button:
    if solicitante and assunto:
        df = pd.DataFrame([{
            'data': data,
            'hora': hora,
            'solicitante': solicitante,
            'assunto': assunto,
            'descricao': descricao,
            'prioridade': prioridade
        }])
        df.to_sql('pedidos', con=engine, if_exists='append', index=False)
        st.success("Pedido cadastrado com sucesso!")
    else:
        st.error("Por favor, preencha os campos Solicitante e Assunto.")

# Visualização dos Pedidos
st.subheader('Pedidos Cadastrados')
try:
    pedidos_df = pd.read_sql("SELECT * FROM pedidos", con=engine)
    st.dataframe(pedidos_df)
except Exception as e:
    st.error(f"Erro ao carregar pedidos: {e}")

