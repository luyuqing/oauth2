from flask import Flask, g, render_template, session, request, jsonify, redirect, url_for

from database import update_auth, get_db, check_password, check_balance


app = Flask(__name__)
app.secret_key = 'mySecretKey'


@app.route('/')
def index():
    welcome_message = ''
    if 'logged_in_user' in session:
        name = session.get('logged_in_user')
        welcome_message = 'Welcome {}'.format(name)
    else:
        pass
    return render_template('index.html', welcome_message=welcome_message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        try:
            pw = check_password(username)
        except TypeError as e:
            print(e)

        if password == pw:
            session['logged_in_user'] = username
            return jsonify('verified')
        else:
            return jsonify('invalid')
    else:
        return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in_user', None)
    return redirect(url_for('index'))


@app.route('/balance')
def balance():
    name = session.get('logged_in_user', None)
    if name:
        balance = str(check_balance(name))
        message = 'Hi, {}, your balance is {}'.format(name, balance)
    else:
        message = 'You need log in first'
    return render_template('balance.html', message=message)


@app.teardown_appcontext
def close_connection(exception):
    update_auth('foo', 0)
    update_auth('peanut', 0)
    db = get_db()
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, port=5005)