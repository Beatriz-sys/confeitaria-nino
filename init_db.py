import sqlite3

DB_NAME = "bancoTeste.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Criar tabela de login
cursor.execute("""
CREATE TABLE IF NOT EXISTS login (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

# Criar tabela de produtos
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL NOT NULL,
    imagem TEXT
)
""")

conn.commit()
conn.close()
print("Banco inicializado com sucesso!")
