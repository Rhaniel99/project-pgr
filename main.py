import streamlit as st
import page.register as RegisterCall
import page.query as QueryCall
import page.dashboard as DashBoard

st.sidebar.title("Sejam bem vindos!")

selected_option = st.sidebar.radio('Opções', ['Cadastrar', 'Consultar', 'Dashboard'])

if selected_option == 'Consultar':
    QueryCall.QueryCall()

if selected_option == 'Cadastrar':
    st.experimental_set_query_params()
    RegisterCall.RegisterCall()

if selected_option == 'Dashboard':
    DashBoard.DashBoard()
