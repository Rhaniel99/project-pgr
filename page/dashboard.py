import streamlit as st
from controllers.CallController import selectAll
import pandas as pd
import matplotlib.pyplot as plt

def get_chamados_finalizados_por_tecnico(chamados):
    chamados_finalizados_por_tecnico = {}

    for chamado in chamados:
        if chamado['Status'] == 'Finalizado':
            tecnico = chamado['Responsavel']
            chamados_finalizados_por_tecnico[tecnico] = chamados_finalizados_por_tecnico.get(tecnico, 0) + 1

    return chamados_finalizados_por_tecnico

def DashBoard():
    st.title("Dashboard de Chamados")

    # Carregar chamados do banco de dados
    chamados = selectAll()

    # Criar uma lista de colunas desejadas e seus respectivos cabeçalhos
    colunas_desejadas = [
        ('Responsavel', 'Técnico'),
        ('Abertura', 'Abertura'),
        ('DefeitoRelatado', 'Defeito Relatado'),
        ('GLPI', 'GLPI'),
        ('Local', 'Local'),
        ('Status', 'Status'),
        ('Termino', 'Término')
    ]

    # Criar um dicionário para rastrear chamados por responsável
    chamados_por_responsavel = {}

    # Preencher o dicionário com o chamado mais recente para cada responsável
    for chamado_dict in chamados:
        responsavel = chamado_dict.get('Responsavel')  # Use get() para lidar com a possível ausência da chave
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

    # Reorganizar as colunas
    colunas_reorganizadas = ['Técnico', 'Status', 'GLPI', 'Local', 'Abertura', 'Término', 'Finalizados']

    # Corrigir tipo de dados na coluna 'Término' para permitir a exibição na tabela
    df['Término'] = df['Término'].astype(str)

    # Adicionar uma coluna com índice começando de 1
    df.index = range(1, len(df) + 1)

    # Exibir a tabela
    st.subheader("Último Chamado por Responsável")
    st.table(df[colunas_reorganizadas].style.set_properties(**{'text-align': 'center'}))

    # Criar o gráfico de barras horizontal
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['Técnico'], df['Finalizados'])
    ax.set_xlabel('Chamados Finalizados')
    ax.set_ylabel('Técnico')
    ax.set_title('Quantidade de Chamados Finalizados por Técnico')
    st.pyplot(fig)


if __name__ == "__main__":
    DashBoard()
