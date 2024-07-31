import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def execute_query(conn, query, params=()):
    """ Execute a query with the provided parameters """
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
    except Error as e:
        print(e)

def fetch_query(conn, query, params=()):
    """ Fetch results from a query with the provided parameters """
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(e)
    return []
