from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

def _get_cursor():
    """Acede à ligação nativa (raw) gerida pelo SQLAlchemy e cria um cursor."""
    conn = db.engine.raw_connection()
    return conn, conn.cursor()

def init_db():
    """DDL: Executa a criação da tabela através do cursor."""
    conn, cursor = _get_cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        """)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_user_by_username(username):
    """
    DQL: Procura o utilizador parametrizando a consulta com '?'.
    Previne SQL Injection ao separar a instrução SQL dos dados inseridos.
    """
    conn, cursor = _get_cursor()
    try:
        # O marcador '?' instrui o driver a tratar o valor como um dado puro, e não como código SQL
        sql = "SELECT id, username, password_hash FROM users WHERE username = ?"
        cursor.execute(sql, (username,))
        resultado = cursor.fetchone()

        if resultado:
            return {
                "id": resultado[0],
                "username": resultado[1],
                "password_hash": resultado[2]
            }
        return None
    finally:
        cursor.close()
        conn.close()

def create_user(username, password):
    """
    DML: Insere um novo registo utilizando uma tupla de parâmetros no cursor.
    """
    password_hash = generate_password_hash(password)
    conn, cursor = _get_cursor()
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        cursor.execute(sql, (username, password_hash))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def check_user_password(stored_hash, password_input):
    """Compara a palavra-passe em texto limpo com o hash armazenado."""
    return check_password_hash(stored_hash, password_input)