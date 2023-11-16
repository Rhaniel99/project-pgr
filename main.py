import streamlit as st;
import controllers.ClientController as ClienteController;
import models.Cliente as cliente
import pandas as pd


st.sidebar.title("Sejam bem vindos!")
Page_client = st.sidebar.selectbox('Opções', ['Incluir', 'Alterar', 'Excluir', 'Consultar'])

if Page_client == 'Consultar':
    st.title("Consultar")
    costumerList = []
    for item in ClienteController.selectAll():
        costumerList.append([item['Nome'], item['Idade'], item['Profissao']])
        
    df = pd.DataFrame(
        costumerList,
        columns = ['Nome', 'Idade', 'Profissão']
    )
    st.table(df)
    
if Page_client == 'Incluir':
    st.title("Incluir")
    with st.form(key="include_cliente"):
        input_name = st.text_input(label="Insira o seu nome: ")
        input_age = st.number_input(label="Insira sua idade", format="%d", step=1)
        input_occupation = st.selectbox("Selecione sua profissão", ["Desenvolvimento", "Música", "Design"])
        input_button_submit = st.form_submit_button("Enviar")

    if input_button_submit:
        cliente.id = 0
        cliente.nome = input_name
        cliente.idade = input_age
        cliente.profissao = input_occupation

        ClienteController.register(cliente)
        st.success("Cliente incluido com sucesso")
