import sqlite3

def criar_tabela(conn):
    cursor = conn.cursor()
    # Criação da tabela
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FormData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opCalled DATETIME NOT NULL,
            repDefect VARCHAR(250) NOT NULL,
            glpi INT NOT NULL,
            locale VARCHAR(50) NOT NULL,
            status TEXT CHECK(status IN ('Aguardando Atendimento', 'Finalizado', 'Parado', 'Em Atendimento')) NOT NULL,
            resp VARCHAR(50) NOT NULL,
            endCalled DATETIME NULL
        )
    ''')
    conn.commit()

def criar_conexao():
    # Conecta ao banco de dados SQLite (cria um arquivo chamado data.db)
    conn = sqlite3.connect('data.db')
    # Chama a função para criar a tabela
    criar_tabela(conn)
    
    return conn
