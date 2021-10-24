from flask import *
from utils import *
from database import Database

import requests

auth = Blueprint('auth', __name__, template_folder='views', static_folder='assets', static_url_path='/assets')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        message = None
        invalid_inputs = {}

        errors = False
        if username == '':
            invalid_inputs['username'] = 'Devi inserire un username!'
            errors = True

        if password == '':
            invalid_inputs['password'] = 'Devi inserire una password!'
            errors = True

        if errors:
            return render_template('login.html', invalid_inputs=invalid_inputs, username_value=username, password_value=password)

        try:
            #  xhr.open('GET', 'https://sunfire.a-centauri.com/npayapi/?richiesta=estratto&utente=' + user + '&auth=' + pass);
            response = requests.get(f'https://sunfire.a-centauri.com/npayapi/?richiesta=estratto&utente={username}&auth={password}', timeout=3).json()
            if response['status'] != 403:
                if username.lower() == "lego11" or username.lower() == "mrdionesalvi":
                    session['username'] = username
                    session['logged'] = True
                    return redirect(url_for('dashboard.index'))
                else:
                    message = 'Non sei un\'admin!.'
            elif response['detail'] == 'Credenziali errate':
                invalid_inputs['password'] = 'Password errata!'
            elif response['detail'] == 'Utente non trovato':
                invalid_inputs['username'] = 'Utente inesistente!'
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            message = 'Impossibile contattare i server di autenticazione! Riprova più tardi.'

        return render_template('login.html', invalid_inputs=invalid_inputs, message=message, username_value=username, password_value=password)

    if session.get('logged'):
        return redirect(url_for('dashboard.index'))
    else:
        return render_template('login.html', invalid_inputs={})


@auth.route('/logout')
def logout():
    if session.get('logged'):
        session.clear()
        session['logged'] = False

    return redirect(url_for('index'))
