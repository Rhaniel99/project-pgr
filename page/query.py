import streamlit as st;
import controllers.CallController as CallController;
import page.register as PageCreateCall

def QueryCall():
    params = st.experimental_get_query_params()
    if params.get("id") == None:
        st.experimental_set_query_params()
        colms = st.columns((7, 6, 5, 6, 5, 6, 5, 6, 7))
        field = ['Abertura', 'Defeito Relatado', 'GLPI', 'LOCAL', 'STATUS', 'RESPONSAVEL', 'TERMINO', 'Alterar', 'Excluir']
        for col, fields_name in zip(colms, field):
            col.write(fields_name)
            
        for item in CallController.selectAll():
            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns((7, 6, 5, 6, 5, 6, 5, 7, 7))
            col1.write(item.get('Abertura', ''))        
            col2.write(item.get('DefeitoRelatado', ''))
            col3.write(item.get('GLPI', ''))
            col4.write(item.get('Local', ''))
            col5.write(item.get('Status', ''))
            col6.write(item.get('Responsavel', ''))
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
                    id = [str(item['id'])]
                )
                st.experimental_rerun()
    else:
        on_click_return = st.button("Voltar")
        if on_click_return:
            st.experimental_set_query_params()
            st.experimental_rerun()
        PageCreateCall.RegisterCall()
        