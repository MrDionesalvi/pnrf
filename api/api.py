from flask import Blueprint
from flask import request
from database import Database
from utils import *

import html
import json

api = Blueprint('api', __name__)


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


@api.route('/version/lua')
def version_lua():

   return '{["version"]="0.0"}'
