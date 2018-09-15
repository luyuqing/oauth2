import requests
import jwt
from flask import Flask, render_template, redirect, session, url_for, jsonify, request


app = Flask(__name__)
app.secret_key = 'clientSecretKey'


@app.before_first_request
def before_first_request():
    session.pop('token', None)
    session.pop('balance', None)


@app.route('/callback')
def callback():
    code = request.args.get('code')
    url = "http://127.0.0.1:5005/token?client_id=mockClient&client_secret=clientSecretKey&grant_type=authorization_code&code={}".format(code) # &redirect_uri
    res = requests.get(url)
    token = res.json().get('token')
    session['token'] = token
    return redirect(url_for('index'))


@app.route('/')
def index():
    if session.get('token') is None:
        return render_template('index.html')
    else:
        token = session.get('token')
        res = requests.post('http://127.0.0.1:5005/api/balance', json={'token': token})
        verified = res.json().get('token_verified')
        if verified:
            encoded = res.json().get('info')
            info = jwt.decode(encoded, app.secret_key)
            username = info['user_info']['username']
            uuid = info['user_info']['uuid']
            balance = info['user_info']['balance']
            session['balance'] = str(balance)
            return redirect(url_for('user', username=username, uuid=uuid))
        else:
            return jsonify('Invalid Token')


@app.route('/<username>')
def user(username):
    balance = session.get('balance')
    return render_template('user.html', name=username, balance=balance)


if __name__ == '__main__':
    app.run(debug=True)