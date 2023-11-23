import streamlit as st
from controllers.CallController import selectAll
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from st_aggrid import AgGrid, GridOptionsBuilder
from streamlit_card import card
from streamlit_cardselectable import st_cardselectable
import time

def get_chamados_finalizados_por_tecnico(chamados):
    chamados_finalizados_por_tecnico = {}

    for chamado in chamados:
        if chamado['Status'] == 'Finalizado':
            tecnico = chamado['Responsavel']
            chamados_finalizados_por_tecnico[tecnico] = chamados_finalizados_por_tecnico.get(tecnico, 0) + 1

    return chamados_finalizados_por_tecnico

def apply_custom_style():
    style.use('dark_background')
    plt.rcParams['figure.figsize'] = (6, 4.4)

def DashBoard():
    chamados = selectAll()
    colunas_desejadas = [
        ('Responsavel', 'Técnico'),
        ('GLPI', 'GLPI'),
        ('Local', 'Local'),
        ('Status', 'Status'),
        ('Abertura', 'Abertura'),
        ('Termino', 'Término')
    ]
    chamados_por_responsavel = {}
    for chamado_dict in chamados:
        responsavel = chamado_dict.get('Responsavel')
        if responsavel not in chamados_por_responsavel or chamado_dict.get('id') > chamados_por_responsavel[responsavel].get('id', 0):
            chamados_por_responsavel[responsavel] = chamado_dict

    chamados_formatados = []
    for chamado_dict in chamados_por_responsavel.values():
        chamado_formatado = {cabecalho: chamado_dict[coluna] for coluna, cabecalho in colunas_desejadas}
        if chamado_formatado['Término'] is None:
            chamado_formatado['Término'] = 'Em andamento'
        chamados_formatados.append(chamado_formatado)

    df = pd.DataFrame(chamados_formatados)

    chamados_finalizados_por_tecnico = get_chamados_finalizados_por_tecnico(chamados)
    df['Finalizados'] = df['Técnico'].map(chamados_finalizados_por_tecnico).fillna(0).astype(int)
    df['Término'] = df['Término'].astype(str)

    col1, col2 = st.columns([2, 1], gap="small")

    with col1:
        st.subheader("Tabela de Chamados")
        gd = GridOptionsBuilder.from_dataframe(df)
        grid_options = gd.build()
        AgGrid(df, gridOptions=grid_options, allow_unsafe_jscode=True, theme='streamlit')

    estatisticas = {
        'Total de Chamados': len(chamados),
        'Chamados Finalizados': df['Finalizados'].sum(),
        'Aguardando Atendimento': len([chamado for chamado in chamados if chamado['Status'] == 'Aguardando Atendimento']),
        'Em Atendimento': len([chamado for chamado in chamados if chamado['Status'] == 'Em Atendimento']),
        'Parado': len([chamado for chamado in chamados if chamado['Status'] == 'Parado'])
    }

        


    with col2:
        st.subheader("Estatísticas")
        gd_estatisticas = GridOptionsBuilder.from_dataframe(pd.DataFrame(estatisticas.items(), columns=['Estatística', 'Valor']))
        grid_options_estatisticas = gd_estatisticas.build()

        AgGrid(pd.DataFrame(estatisticas.items(), columns=['Estatística', 'Valor']), gridOptions=grid_options_estatisticas, allow_unsafe_jscode=True, theme='streamlit')


        apply_custom_style()

        fig, ax = plt.subplots()
        bars = ax.barh(df['Técnico'], df['Finalizados'])
        for bar, label in zip(bars, df['Finalizados']):
            ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, label, ha='left', va='center')
        ax.get_xaxis().set_visible(False)

        ax.set_xlabel('Chamados Finalizados')
        ax.set_ylabel('Técnico')
        ax.set_title('Quantidade de Chamados Finalizados por Técnico')

        st.pyplot(fig)
   

if __name__ == "__main__":
    DashBoard()
