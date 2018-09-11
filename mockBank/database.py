import os
import sqlite3
from flask import g

from app import app


db_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_dir, 'database.db')


# create a table for log-in user, not app related
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY,
        name text NOT NULL,
        password text NOT NULL,
        authenticated integer NOT NULL
    );
    """

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql)
    except Exception as e:
        print(e)
    finally:
        conn.close()


# shortcut to check if sqlite connection is closed, not app related
def check_conn_closed():
    conn = sqlite3.connect(db_path)
    conn.close()
    try:
        cursor = conn.cursor()
        cursor.execute("select * from users")
    except sqlite3.ProgrammingError as e:
        print(e)  # if conn closed, expected error: Cannot operate on a closed database.


# add user to table users, not app related
def add_user(id_, name, password, auth):
    sql = """
    INSERT INTO users (id, name, password, authenticated) VALUES (?, ?, ?, ?)
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql, (id_, name, password, auth))
    except Exception as e:
        print(e)
    finally:
        conn.close()


# select all users from users, not app related
def select_user():
    sql = """SELECT * FROM users"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql)
        print(cursor.fetchall())
    except Exception as e:
        print(e)
    finally:
        conn.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()