import streamlit as st;
import page.register as RegisterCall
import page.query as QueryCall
import page.dashboard as DashBoard


st.sidebar.title("Sejam bem vindos!")
Page_client = st.sidebar.selectbox('Opções', ['Incluir', 'Consultar', 'Dashboard'])

if Page_client == 'Consultar':
    QueryCall.QueryCall()
   
if Page_client == 'Incluir':
    st.experimental_set_query_params()
    RegisterCall.RegisterCall()

if Page_client == 'Dashboard':
    DashBoard.DashBoard()