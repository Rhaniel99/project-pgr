import streamlit as st
from controllers.CallController import selectAll
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import streamlit_pandas as sp
from st_aggrid import AgGrid, GridUpdateMode, GridOptionsBuilder

def get_chamados_finalizados_por_tecnico(chamados):
    chamados_finalizados_por_tecnico = {}

    for chamado in chamados:
        if chamado['Status'] == 'Finalizado':
            tecnico = chamado['Responsavel']
            chamados_finalizados_por_tecnico[tecnico] = chamados_finalizados_por_tecnico.get(tecnico, 0) + 1

    return chamados_finalizados_por_tecnico

def apply_custom_style():
    # Adicione estilos personalizados aqui
    style.use('dark_background')  # Tema mais escuro
    plt.rcParams['figure.figsize'] = (8, 4)  # Tamanho menor
    
def DashBoard():
    st.subheader("Chamados Atuais")
    # Carregar chamados do banco de dados
    chamados = selectAll()

    # Criar uma lista de colunas desejadas e seus respectivos cabeçalhos
    colunas_desejadas = [
        ('Responsavel', 'Técnico'),
        ('GLPI', 'GLPI'),
        ('Local', 'Local'),
        ('Status', 'Status'),
        ('Abertura', 'Abertura'),
        ('Termino', 'Término')
    ]

    # Criar um dicionário para rastrear chamados por responsável
    chamados_por_responsavel = {}

    # Preencher o dicionário com o chamado mais recente para cada responsável
    for chamado_dict in chamados:
        responsavel = chamado_dict.get('Responsavel')
        if responsavel not in chamados_por_responsavel or chamado_dict.get('id') > chamados_por_responsavel[responsavel].get('id', 0):
            chamados_por_responsavel[responsavel] = chamado_dict

    # Criar uma lista de dicionários com colunas desejadas e formatar o valor 'Término'
    chamados_formatados = []
    for chamado_dict in chamados_por_responsavel.values():
        chamado_formatado = {cabecalho: chamado_dict[coluna] for coluna, cabecalho in colunas_desejadas}

        # Formatar o valor 'Término' para 'Em andamento' se for nulo
        if chamado_formatado['Término'] is None:
            chamado_formatado['Término'] = 'Em andamento'

        chamados_formatados.append(chamado_formatado)

    # Criar um DataFrame a partir dos chamados formatados
    df = pd.DataFrame(chamados_formatados)

    # Calcular a quantidade de chamados finalizados por Técnico usando a função criada
    chamados_finalizados_por_tecnico = get_chamados_finalizados_por_tecnico(chamados)

    # Adicionar uma coluna 'Finalizados' ao DataFrame
    df['Finalizados'] = df['Técnico'].map(chamados_finalizados_por_tecnico).fillna(0).astype(int)

    # Corrigir tipo de dados na coluna 'Término' para permitir a exibição na tabela
    df['Término'] = df['Término'].astype(str)
    gd = GridOptionsBuilder.from_dataframe(df)
    # Exibir a tabela usando AgGrid com tema 'balham'
    gridoptions = gd.build()
    AgGrid(df, gridOptions=gridoptions, allow_unsafe_jscode=True, theme='alpine')

    # Aplicar estilo personalizado para o gráfico
    apply_custom_style()

    # Criar o gráfico de barras horizontal
    fig, ax = plt.subplots()
    bars = ax.barh(df['Técnico'], df['Finalizados'])

    # Adicionar numeração dentro das barras
    for bar, label in zip(bars, df['Finalizados']):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, label, ha='left', va='center')

    # Desativar os marcadores de eixo
    ax.get_xaxis().set_visible(False)

    ax.set_xlabel('Chamados Finalizados')
    ax.set_ylabel('Técnico')
    ax.set_title('Quantidade de Chamados Finalizados por Técnico')

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    DashBoard()
