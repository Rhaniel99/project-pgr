# from typing import List
import mysql.connector
from mysql.connector import Error
from services.database import criar_conexao
from models.Called import Call
from datetime import datetime  # Importe o módulo datetime


def register(Call):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        sql = """
        INSERT INTO formsdata(opCalled, repDefect, glpi, locale, status, resp) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        value = (Call.opCalled, Call.repDefect, Call.glpi,Call.locale, Call.status, Call.resp)

        cursor.execute(sql, value)
        conn.commit()

        return cursor.rowcount

    except mysql.connector.Error as e:
        print('Não foi possível inserir o registro. Erro:', str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def upDate(flag, Call):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        # Se o status for "Finalizado", atualize também o endCalled
        if Call.status == "Finalizado":
            Call.endCalled = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sql = """
        UPDATE FormsData 
        SET opCalled=%s, repDefect=%s, glpi=%s, locale=%s, status=%s, resp=%s, endCalled=%s
        WHERE id=%s
        """
        value = (Call.opCalled, Call.repDefect, Call.glpi, Call.locale, Call.status, Call.resp, Call.endCalled, flag)

        cursor.execute(sql, value)
        conn.commit()

        return cursor.rowcount

    except mysql.connector.Error as e:
        print('Não foi possível atualizar o registro. Erro:', str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def selectOne(id):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        value = (id,)
        
        cursor.execute("SELECT * FROM FormsData WHERE id = %s", value)
        
        rows = cursor.fetchall()
        registros = []
        for row in rows:
            registro = {
                'id': row[0],
                'Abertura': row[1],
                'DefeitoRelatado': row[2],
                'GLPI': row[3],
                'Local': row[4],
                'Status': row[5],
                'Responsavel': row[6],
                'Termino': row[7]
            }
            registros.append(registro)

        return registros[0]

    except mysql.connector.Error as e:
        print('Não foi possível executar a consulta. Erro:', str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def selectAll():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM FormsData")
        rows = cursor.fetchall()
        registros = []
        for row in rows:
            registro = {
                'id': row[0],
                'Abertura': row[1],
                'DefeitoRelatado': row[2],
                'GLPI': row[3],
                'Local': row[4],
                'Status': row[5],
                'Responsavel': row[6],
                'Termino': row[7]
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
            
def deleteOne(id):
    conn = criar_conexao()
    cursor = conn.cursor()
    
    # Correção aqui, utilizando uma tupla e ajustando a consulta
    value = (id,)
    sql = "DELETE FROM FormsData WHERE id = %s"
    
    cursor.execute(sql, value)
    conn.commit()