import bcrypt
from database.db_handler import create_connection, execute_query, fetch_query

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode(), hashed)

def create_user(email, username, password):
    conn = create_connection('database/sqlite.db')
    hashed_password = hash_password(password)
    query = "INSERT INTO users (email, username, password) VALUES (?, ?, ?)"
    execute_query(conn, query, (email, username, hashed_password))

def authenticate_user(email, password):
    conn = create_connection('database/sqlite.db')
    query = "SELECT * FROM users WHERE email = ?"
    user = fetch_query(conn, query, (email,))
    if user and check_password(user[0][3], password):
        return True
    return False
