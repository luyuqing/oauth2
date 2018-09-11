import os
import sqlite3
from flask import g

db_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_dir, 'database.db')
print(db_path)