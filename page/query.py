import streamlit as st
import controllers.CallController as CallController
import page.register as PageCreateCall

def apply_style_to_header():
    return (
        "font-size: 18px;"
        "font-weight: bold;"
    )

def QueryCall():
    st.header('Chamados')
    header_style = apply_style_to_header()
    params = st.experimental_get_query_params()

    if "current_page" not in st.session_state:
        st.session_state.current_page = 0

    if params.get("id") is None:
        st.experimental_set_query_params()

        colms = st.columns((33, 25, 25, 25, 25, 25, 25, 25, 25))
        field = ['Responsavel', 'Defeito', 'GLPI', 'Local', 'Status', 'Abertura', 'Termino', 'Alterar', 'Excluir']
        for col, fields_name in zip(colms, field):
            col.markdown(f"<p style='{header_style}'>{fields_name}</p>", unsafe_allow_html=True)
        items_per_page = 5  

        chamados = list(reversed(CallController.selectAll()))

        start_idx = st.session_state.current_page * items_per_page
        end_idx = (st.session_state.current_page + 1) * items_per_page

        for item in chamados[start_idx:end_idx]:
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns((33, 25, 25, 25, 25, 25, 25, 25, 25))
            col1.write(item.get('Responsavel', ''))
            col2.write(item.get('DefeitoRelatado', ''))
            col3.write(item.get('GLPI', ''))
            col4.write(item.get('Local', ''))
            col5.write(item.get('Status', ''))
            col6.write(item.get('Abertura', ''))
            col7.write(item.get('Termino', ''))

            button_space_update = col8.empty()
            on_click_up = button_space_update.button('Alterar', 'btnUp' + str(item['id']))

            button_space_del = col9.empty()
            on_click_del = button_space_del.button('Deletar', 'btnDel' + str(item['id']))

            if on_click_del:
                iden = str(item['id'])
                CallController.deleteOne(iden)

            if on_click_up:
                st.experimental_set_query_params(
                    id=[str(item['id'])]
                )
                st.experimental_rerun()

        if len(chamados) > items_per_page:
            st.write("Página:", st.session_state.current_page + 1)
            if st.session_state.current_page > 0:
                if st.button("Página Anterior"):
                    st.session_state.current_page -= 1
                    st.experimental_rerun()  
            if end_idx < len(chamados):
                if st.button("Próxima Página"):
                    st.session_state.current_page += 1
                    st.experimental_rerun()  

    else:
        on_click_return = st.button("Voltar")
        if on_click_return:
            st.experimental_set_query_params()
            st.experimental_rerun()
        PageCreateCall.RegisterCall()
