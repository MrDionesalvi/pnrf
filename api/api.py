from flask import Blueprint
from flask import request
from database import Database
from utils import *

import html
import json
import requests

api = Blueprint('api', __name__)


priceFrequency = {
    1: 1,
    2: 10,
    3: 100,
    4: 1000,
    5: 10000,
    6: 100000,
    7: 1000000,
    8: 10000000
}

@api.route('/')
def list():
    return 'helo!'

@api.route('/checkplayer')
def checkplayer():
    if 'player' in request.args:
        player = request.args['player']
        player = html.escape(player)
        db = Database()
        db_session = db.session
        try:
            data = db_session.query(db.frequency).filter(db.frequency.username == player).all()
            if data:
                return '{["status"]="OK"}'
        except:
            return '{["status"]="NP"}'


@api.route('/check/newfrequency')
def check_newfrequency():
    if 'player' in request.args:
        player = request.args['player']
        player = html.escape(player)

        frequency = get_FrequencyByUsername(player)
        totalFrequency = 0

        a = json.loads(frequency)

        for b in a:
            totalFrequency += 1

        if totalFrequency > 8:
            return '{["status"]="TMF"}'
        price = priceFrequency[totalFrequency+1]

        strings = "{[\"status\"]=\"OK\",[\"frequency\"]=\""+str(totalFrequency)+"\",[\"price\"]=\""+str(price)+"\"}" 
        return strings

    return '{["status"]="KO"}'


@api.route('/do/payments')
def do_payments():
    if 'player' in request.args and 'username' in request.args and 'password' in request.args and 'amount' in request.args:
        player = request.args.get('player')
        username = request.args.get('username')
        password = request.args.get('password')
        amount = request.args.get('amount')

        player = html.escape(player)
        username = html.escape(username)
        password = html.escape(password)
        amount = html.escape(amount)

        try:
            response = requests.get(f'https://sunfire.a-centauri.com/npayapi/?richiesta=trasferimento&utente={username}&auth={password}&valore={int(amount)}&beneficiario=lego11', timeout=3).json()
            if response['status'] == 200:
                assigendFrequency = assign_LastFrequencyNumber(player)
                if assigendFrequency:
                    return "{[\"status\"]=\"OK\",[\"frequency\"]=\""+str(assigendFrequency)+"\"}" 
                else:
                    print(assigendFrequency)
                    return '{["status"]="KO", ["detail"]="Errore col l\'assegnazione"}'
            else:
                return '{["status"]="KO", ["detail"]="Errore col pagamento"}'         
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            return '{["status"]="KO", ["detail"]="Server offline"}'
    
    return '{["status"]="KO"}'

@api.route('/new/frequency', methods=['GET','POST'])
def new_frequency():
    if request.method == 'POST':
        frequencyNumber = request.form.get('frequencyNumber')
        owner = request.form.get('owner')
        try:
            if owner != "":
                if frequencyNumber == "":
                    assigendFrequency = assign_LastFrequencyNumber(owner)
                    if assigendFrequency:
                        return redirect(url_for('dashboard.index'))
                    else:
                        return redirect(url_for('dashboard.index'))           
                elif frequencyNumber != "" and int(frequencyNumber) > 0:
                    try:
                        db = Database()
                        db_session = db.session
                        db_session.add(db.frequency(id=frequencyNumber,owner=owner, reallocable=0, occuped=1))
                        db_session.commit()
                        db_session.close()
                        return redirect(url_for('dashboard.index'))
                    except Exception as e:
                        print(e)
                        return '{["status"]="KO"}' 
        except:
            print('{["status"]="KO"}')
            return redirect(url_for('dashboard.index'))       
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('dashboard.index'))

@api.route('/delete/frequency', methods=['GET','POST'])
def delete_frequency():
    if request.method == 'GET':
        frequencyNumber = request.args.get('frequencyNumber')

        if frequencyNumber and int(frequencyNumber) > 0:
            try:
                db = Database()
                db_session = db.session
                data = db_session.query(db.frequency).filter(db.frequency.id == frequencyNumber).one()
                db_session.delete(data)
                db_session.commit()
                db_session.close()
                return redirect(url_for('dashboard.index'))
            except Exception as e:
                print(e)
                return '{["status"]="KO"}'

        
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('dashboard.index'))

@api.route('/version/lua')
def version_lua():

   return '{["version"]="0.0"}'
