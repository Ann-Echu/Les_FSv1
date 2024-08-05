import sqlite3
from .db_handler import create_connection
from .db_handler import execute_query

def create_tables():
    database = "database/user.db"
    
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """
    
    sql_create_responses_table = """
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        response TEXT NOT NULL,
        FOREIGN KEY (email) REFERENCES users (email)
    );
    """
    
    conn = create_connection(database)
    
    if conn is not None:
        execute_query(conn, sql_create_users_table)
        execute_query(conn, sql_create_responses_table)
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    create_tables()
