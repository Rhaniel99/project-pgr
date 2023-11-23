import mysql.connector

def criar_conexao():
    return mysql.connector.connect(
        host='172.16.15.34',
        user='controle',
        password='getag2022',
        database='pgr',
    )