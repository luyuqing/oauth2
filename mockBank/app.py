from flask import Flask, render_template, session, request, jsonify, redirect, url_for
import datetime
import time
import jwt
import os
import base64

from database import update_auth, get_db, check_password, check_balance, deduct_balance, \
    check_auth_code, update_auth_code


app = Flask(__name__)
app.secret_key = 'mySecretKey'

config = {
    'client_id': 'mockClient',
    'client_secret': 'clientSecretKey',
    'callback_uri': 'http://127.0.0.1:5000/callback',
    'scope': 'balance_api',
    'response_type': 'code'
}

token_dict = {
    't123': {
        'token': 'access_token',
        'token_type': 'bearer',
        'expired_at': time.time() + 300,
        'scope': 'balance_api',
        'user_info': {
            'username': 'foo',
            'uuid': 'xxx111',
            'balance': check_balance('foo')
        }
    },
    't456': {
        'token': 'access_token',
        'token_type': 'bearer',
        'expired_at': time.time() + 300,
        'scope': 'balance_api',
        'user_info': {
            'username': 'peanut',
            'uuid': 'yyy222',
            'balance': check_balance('peanut')
        }
    }
}


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


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    message = ''
    if request.method == 'POST':
        name = session.get('logged_in_user')
        if name is None:
            return jsonify('You must log in first')
        else:
            amount = int(request.json)
            deduct_balance(name, amount)
            balance = check_balance(name)
            return jsonify({"balance": str(balance), "time": str(datetime.datetime.now())[:19]})
    return render_template('transfer.html', message=message)


@app.route('/oauth2_login', methods=['GET', 'POST'])
def oauth2_login():
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        try:
            pw = check_password(username)
        except TypeError as e:
            print(e)

        if password == pw:
            code = base64.b64encode(os.urandom(6)).decode()
            if username == 'foo':
                update_auth_code('foo', code)
            if username == 'peanut':
                update_auth_code('peanut', code)
            uri = config['callback_uri']
            uri += '?code={}'.format(code)
            return jsonify({'uri': uri})
        else:
            return jsonify('invalid')
    else:
        return render_template('oauth2_login.html')


@app.route('/token')
def token():
    code = request.args.get('code')
    name = check_auth_code(code)
    token = None
    for k, v in token_dict.items():
        if v['user_info']['username'] == name:
            token = k
            break
    return jsonify({'token': token})


@app.route('/api/balance', methods=['POST'])
def api_balance():
    token = request.json.get('token')
    info = token_dict.get(token)
    if info is not None:
        if 'balance_api' in info['scope']:
            encoded = jwt.encode(info, config['client_secret'], algorithm='HS256')
            encoded = encoded.decode()  # convert bytes to string
            # print(encoded)
            return jsonify({'token_verified': True, 'info': encoded})
        else:
            return "Invalid Scope", 403
    else:
        return "Invalid Token", 403


@app.teardown_appcontext
def close_connection(exception):
    update_auth('foo', 0)
    update_auth('peanut', 0)
    db = get_db()
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True, port=5005)