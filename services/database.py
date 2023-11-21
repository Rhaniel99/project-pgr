import mysql.connector

def criar_conexao():
    return mysql.connector.connect(
        host='localhost',
        user='rhaniel',
        password='123',
        database='pgr',
    )