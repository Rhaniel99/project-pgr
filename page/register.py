import streamlit as st;
import controllers.CallController as CallController;
import models.Called as call
from enum import Enum
 
class Names(Enum):
    FABRICIO_SOUZA_NOGUEIRA = "Fabricio Souza Nogueira"
    JOABE_ARAÚJO_DA_SILVA = "Joabe Araújo da Silva"
    MANOEL_ADAIDE_FIGUEIRA_ROCHA = "Manoel Adaíde Figueira Rocha"
    OBEDE_SILVA = "Obede Silva de Menezes Portela"
    VANUZIVON_CASSIANO = "Vanuzivon Cassiano Rodrigues"
    VICTOR_HUGO_DE_OLIVEIRA = "Victor Hugo de Oliveira"
    CARLOS_ROGERIO = "Carlos Rogerio Morais Marinho"
    DORIVAL_RODRIGUES = "Dorival Rodrigues Gonçalves de Melo"
    ELINALDO_BRAGA = "Elinaldo Braga de Almeida"
    GUILHERME_FABIANO = "Guilherme Fabiano Santos Teófilo"
    JÚNIOR_MACEDO = "Júnior Macedo da Hora"
    ELISON_BELO = "Elison Belo Alfaia"

 
def RegisterCall():
    idAlt = st.experimental_get_query_params()
    # Verifica se existe parametro na url e limpa
    callRecover = None
    if idAlt.get("id") != None:
        idAlt = idAlt.get("id")[0]
        callRecover = CallController.selectOne(idAlt)
        st.experimental_set_query_params(
            id = [callRecover.get("id")]
        )
        st.title("Alterar")
    else:
        st.title("Incluir")
    
    with st.form(key="include_call"):
        status = ["Aguardando Atendimento", "Em Atendimento", "Finalizado", "Parado"]
        if callRecover == None:
            input_opCalled = st.date_input(label="Data da Chamada")
            input_repDefect = st.text_input(label="Defeito Reportado")
            input_glpi = st.number_input(label="Número GLPI", format="%d", step=1)
            input_locale = st.text_input(label="Local")
            input_status = st.selectbox("Status:", status)
            input_resp = st.selectbox("Responsável:", [name.value for name in Names])
        else:
            input_opCalled = st.date_input(label="Data da Chamada", value=callRecover.get("Abertura"))
            input_repDefect = st.text_input(label="Defeito Reportado", value=callRecover.get("DefeitoRelatado"))
            input_glpi = st.number_input(label="Número GLPI", format="%d", step=1, value=callRecover.get("GLPI"))
            input_locale = st.text_input(label="Local", value=callRecover.get("Local"))
            # Adicione o status recuperado apenas se não estiver presente na lista status
            input_status_options = [status for status in status if status != callRecover.get("Status")]
            # Adicione o status recuperado apenas se não estiver presente na lista status
            input_status_options = [callRecover.get("Status")] + input_status_options
            input_status = st.selectbox("Status:", input_status_options)
             # Remova o responsável recuperado da lista de opções
            input_resp_options = [name.value for name in Names if name.value != callRecover.get("Responsavel")]
            # Adicione o responsável recuperado apenas se não estiver presente na lista de opções
            input_resp_options = [callRecover.get("Responsavel")] + input_resp_options
            input_resp = st.selectbox("Responsável:", input_resp_options)

        input_button_submit = st.form_submit_button("Enviar")
                
    if input_button_submit:
       calls_instance = call.Call(
        opCalled=input_opCalled,
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
           CallController.upDate(calls_instance)
           st.success("Chamada atualizada com sucesso")
