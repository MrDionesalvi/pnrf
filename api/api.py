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



@api.route('/version/lua')
def version_lua():

   return '{["version"]="0.0"}'
