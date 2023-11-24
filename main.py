import streamlit as st
from page import register as RegisterCall
from page import query as QueryCall
from page import dashboard as DashBoard

def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("Sejam bem-vindos!")

    selected_option = st.sidebar.radio('Opções', ['Cadastrar', 'Consultar', 'Dashboard'])
    if selected_option == 'Consultar':
        QueryCall.QueryCall()

    if selected_option == 'Cadastrar':
        st.experimental_set_query_params()
        RegisterCall.RegisterCall()

    if selected_option == 'Dashboard':
        DashBoard.DashBoard()

if __name__ == '__main__':
    main()
