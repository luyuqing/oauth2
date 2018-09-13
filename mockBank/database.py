import os
import sqlite3
from flask import g


db_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_dir, 'database.db')


# create a table for log-in user
def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY,
        name text NOT NULL,
        password text NOT NULL,
        authenticated integer NOT NULL,
        balance integer NOT NULL
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


# shortcut to check if sqlite connection is closed
def check_conn_closed():
    conn = sqlite3.connect(db_path)
    conn.close()
    try:
        cursor = conn.cursor()
        cursor.execute("select * from users")
    except sqlite3.ProgrammingError as e:
        print(e)  # if conn closed, expected error: Cannot operate on a closed database.


# add user to table users
def add_user(id_, name, password, auth, balance):
    sql = """
    INSERT INTO users (id, name, password, authenticated, balance) VALUES (?, ?, ?, ?, ?)
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql, (id_, name, password, auth, balance))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()


# select all users from users
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


# change auth status
def update_auth(name, num):
    sql = """update users set authenticated = ? where name = ?"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql, (num, name))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()


# check auth status
def check_auth(name):
    sql = """select authenticated from users where name = ?"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql, (name,))
        return cursor.fetchone()[0]
    except Exception as e:
        print(e)
    finally:
        conn.close()


# check balance
def check_balance(name):
    sql = """select balance from users where name = ?"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql, (name,))
        return cursor.fetchone()[0]
    except Exception as e:
        print(e)
    finally:
        conn.close()


# deduct balance
def deduct_balance(name, amount):
    balance = check_balance(name)
    sql = """update users set balance = ? where name = ?"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        new_val = balance - amount
        cursor.execute(sql, (new_val, name))
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db

