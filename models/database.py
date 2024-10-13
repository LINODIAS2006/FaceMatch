import sqlite3

class Database:
    @staticmethod
    def connect():
        return sqlite3.connect("photo_app.db")

    @staticmethod
    def initialize_db():
        with Database.connect() as conn:
            cursor = conn.cursor()
            # Cria a tabela de usuários
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            """)
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
