from flask import Flask

from database import get_db


app = Flask(__name__)




@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()