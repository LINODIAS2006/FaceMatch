import os
import sqlite3
import sys

class Database:
    @staticmethod
    def get_db_path():
        # Verifica se o programa está sendo executado como executável gerado por PyInstaller
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS  # Caminho temporário onde os arquivos são extraídos no executável
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Caminho do arquivo Python

        # Retorna o caminho absoluto do banco de dados
        return os.path.join(base_dir, 'photo_app.db')

    @staticmethod
    def connect():
        # Conecta ao banco de dados usando o caminho dinâmico
        return sqlite3.connect(Database.get_db_path())

    @staticmethod
    def initialize_db():
        with Database.connect() as conn:
            cursor = conn.cursor()

            # Criação da tabela de usuários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            """)

            # Criação da tabela de fotos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS photos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    photo BLOB,
                    group_assigned TEXT,
                    FOREIGN KEY(username) REFERENCES users(username)
                )
            """)

            conn.commit()

            # Verifica se o administrador padrão já está no banco de dados
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            admin = cursor.fetchone()

            # Se o administrador não existir, cria um com senha padrão "admin123"
            if admin is None:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    ('admin', 'admin123')
                )
                print("Administrador padrão criado: Usuário='admin', Senha='admin123'")
                conn.commit()

    @staticmethod
    def authenticate_user(username, password):
        with Database.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            return cursor.fetchone() is not None

    @staticmethod
    def authenticate_admin(username, password):
        # Autentica o administrador com as credenciais padrão
        return username == "admin" and password == "admin123"

    @staticmethod
    def register_user(username, password):
        with Database.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
            conn.commit()
