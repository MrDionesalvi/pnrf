from flask import redirect, url_for, session, request
from datetime import datetime
from functools import wraps
from flask.json import jsonify
from sqlalchemy.ext.declarative import DeclarativeMeta


from database import Database
import json

def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not session.get('logged'):
            return redirect(url_for('auth.login', after=request.path))
        return f(*args, **kwargs)

    return decorator

def is_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if session.get('logged'):
            db = Database()
            data = db.session.query(db.admin).filter(db.admin.username == session.get('username')).first()
            if not data:
                return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorator


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)




def get_allFrequency():
    """
    Restituisce tutte le frequenze presenti sul DB
    """

    db = Database()
    db_session = db.session
    data = db.session.query(db.frequency).all()

    data_dumped = json.dumps(data, cls=AlchemyEncoder)

    db.session.close()

    return data_dumped

def get_Frequency(ids):
    """
    Restituisce la frequenze presente sul DB con un ID specifico
    """

    db = Database()
    db_session = db.session
    data = db.session.query(db.frequency).filter(db.frequency.id == ids).all()

    data_dumped = json.dumps(data, cls=AlchemyEncoder)

    db.session.close()

    return data_dumped 

