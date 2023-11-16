# from typing import List
import mysql.connector
from mysql.connector import Error
from services.database import criar_conexao
from models.Cliente import Cliente


def register(Cliente):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        sql = """
        INSERT INTO Cliente(cliNome, cliIdade, cliProfissao) 
        VALUES (%s, %s, %s)
        """
        valores = (Cliente.nome, Cliente.idade, Cliente.profissao)

        cursor.execute(sql, valores)
        conn.commit()

        return cursor.rowcount

    except mysql.connector.Error as e:
        print('Não foi possível inserir o registro. Erro:', str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def selectAll():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Cliente")
        rows = cursor.fetchall()

        registros = []

        for row in rows:
            registro = {
                'id': row[0],
                'Nome': row[1],
                'Idade': row[2],
                'Profissao': row[3]
            }
            registros.append(registro)

        return registros

    except mysql.connector.Error as e:
        print('Não foi possível executar a consulta. Erro:', str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()