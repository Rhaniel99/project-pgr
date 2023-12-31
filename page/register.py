import streamlit as st;
import controllers.CallController as CallController;
import models.Called as call
from enum import Enum
from datetime import datetime
 
class Names(Enum):
    FABRICIO_SOUZA_NOGUEIRA = "FABRICIO SOUZA" #
    JOABE_ARAÚJO_DA_SILVA = "JOABE ARAUJO" #
    MANOEL_ADAIDE_FIGUEIRA_ROCHA = "MANOEL ROCHA" #
    OBEDE_SILVA = "OBEDE SILVA" #
    VANUZIVON_CASSIANO = "VANUZIVON CASSIANO RODRIGUES" #
    VICTOR_HUGO_DE_OLIVEIRA = "VICTOR HUGO" #
    CARLOS_ROGERIO = "CARLOS ROGERIO MORAIS MARINHO" #
    DORIVAL_RODRIGUES = "DORIVAL RODRIGUES GONCALVES DE MELO" #
    ELINALDO_BRAGA = "ELINALDO BRAGA" #
    GUILHERME_FABIANO = "GUILHERME TEÓFILO" #
    JÚNIOR_MACEDO = "JÚNIOR MACEDO DA HORA" #
    ELISON_BELO = "ELISON ALFAIA" #
    WILK_MAX = "WILK MAX MONTEIRO DE AGUIAR" #
    ANNA_KELLY = "ANNA KELLY" #
 
def RegisterCall():
    idAlt = st.experimental_get_query_params()
    callRecover = None
    if idAlt.get("id") != None:
        idAlt = idAlt.get("id")[0]
        callRecover = CallController.selectOne(idAlt)
        st.experimental_set_query_params(
            id = [callRecover.get("id")]
        )
        st.title("Alterar")
    else:
        st.title("Cadastrar Chamados")
    
    with st.form(key="include_call"):
        status = ["Aguardando Atendimento", "Em Atendimento", "Finalizado", "Parado"]
        if callRecover == None:
            input_repDefect = st.text_input(label="Defeito Reportado")
            input_glpi = st.number_input(label="Número GLPI", format="%d", step=1)
            input_locale = st.text_input(label="Local")
            input_status = st.selectbox("Status:", status)
            input_resp = st.selectbox("Responsável:", [name.value for name in Names])
        else:
            input_repDefect = st.text_input(label="Defeito Reportado", value=callRecover.get("DefeitoRelatado"))
            input_glpi = st.number_input(label="Número GLPI", format="%d", step=1, value=callRecover.get("GLPI"))
            input_locale = st.text_input(label="Local", value=callRecover.get("Local"))
            input_status_options = [status for status in status if status != callRecover.get("Status")]
            input_status_options = [callRecover.get("Status")] + input_status_options
            input_status = st.selectbox("Status:", input_status_options)
            input_resp_options = [name.value for name in Names if name.value != callRecover.get("Responsavel")]
            input_resp_options = [callRecover.get("Responsavel")] + input_resp_options
            input_resp = st.selectbox("Responsável:", input_resp_options)

        input_button_submit = st.form_submit_button("Enviar")
                
    if input_button_submit:
       op_called = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       calls_instance = call.Call(
            opCalled=op_called,
            repDefect=input_repDefect,
            glpi=input_glpi,
            locale=input_locale,
            status=input_status,
            resp=input_resp
        )
       if callRecover == None: 
           CallController.register(calls_instance)
           st.success("Chamada incluída com sucesso")
       else:
           CallController.upDate(callRecover.get("id"), calls_instance)
           st.success("Chamada atualizada com sucesso")
