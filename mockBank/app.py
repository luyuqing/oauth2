from flask import Flask, g, render_template, session, request, jsonify

from database import update_auth, get_db


app = Flask(__name__)


@app.route('/')
def index():
    welcome_message = ''
    if 'login_name' in session: 
        name = session.get('login_name')
        welcome_message = 'Welcome {}'.format(name)
    else:
        pass
    return render_template('index.html', welcome_message=welcome_message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        username = request.form.get('username')
        password = request.form.get('password')
        return jsonify('hahaha')
    else:
        return render_template('login.html')


@app.route('/balance')
def balance():
    return render_template('balance.html')


@app.teardown_appcontext
def close_connection(exception):
    update_auth('foo', 0)
    update_auth('peanut', 0)
    db = get_db()
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, port=5005)