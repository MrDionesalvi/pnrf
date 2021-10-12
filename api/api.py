from flask import Blueprint
from flask import request
from database import Database
from utils import *

import html
import json

api = Blueprint('api', __name__)


priceFrequency = {
    1: 0,
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

    return '{["status"]="OK"}'



@api.route('/version/lua')
def version_lua():

   return '{["version"]="0.0"}'
