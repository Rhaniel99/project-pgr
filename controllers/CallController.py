# from typing import List
# import mysql.connector
# from mysql.connector import Error
# from services.database import criar_conexao
from data import criar_conexao
from models.Called import Call
from datetime import datetime  # Importe o módulo datetime
import sqlite3

def register(call):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        sql = """
        INSERT INTO FormsData(opCalled, repDefect, glpi, locale, status, resp) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        value = (call.opCalled, call.repDefect, call.glpi, call.locale, call.status, call.resp)

        cursor.execute(sql, value)
        conn.commit()

        return cursor.rowcount

    except sqlite3.Error as e:
        print('Não foi possível inserir o registro. Erro:', str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def upDate(flag, call):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()

        if call.status == "Finalizado":
            call.endCalled = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = """
            UPDATE FormsData 
            SET opCalled=?, repDefect=?, glpi=?, locale=?, status=?, resp=?, endCalled=?
            WHERE id=?
            """
            value = (call.opCalled, call.repDefect, call.glpi, call.locale, call.status, call.resp, call.endCalled, flag)
        else:
            sql = """
            UPDATE FormsData 
            SET opCalled=?, repDefect=?, glpi=?, locale=?, status=?, resp=?
            WHERE id=?
            """
            value = (call.opCalled, call.repDefect, call.glpi, call.locale, call.status, call.resp, flag)

        cursor.execute(sql, value)
        conn.commit()

        return cursor.rowcount

    except sqlite3.Error as e:
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

        cursor.execute("SELECT * FROM FormsData WHERE id = ?", value)

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

        return registros[0] if registros else None

    except sqlite3.Error as e:
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

    except sqlite3.Error as e:
        print('Não foi possível executar a consulta. Erro:', str(e))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def deleteOne(id):
    conn = criar_conexao()
    cursor = conn.cursor()

    value = (id,)
    sql = "DELETE FROM FormsData WHERE id = ?"

    cursor.execute(sql, value)
    conn.commit()