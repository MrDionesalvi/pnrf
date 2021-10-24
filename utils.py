from flask import redirect, url_for, session, request
from datetime import datetime
from functools import wraps
from flask.json import jsonify
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql.functions import user


from database import Database
import json

def login_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not session.get('logged'):
            return redirect(url_for('auth.login', after=request.path))
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
    data = db_session.query(db.frequency).all()

    data_dumped = json.dumps(data, cls=AlchemyEncoder)

    db_session.close()

    return data_dumped

def get_FrequencyByUsername(username):
    """
    Restituisce tutte le frequenze presenti sul DB con quell'username
    """

    db = Database()
    db_session = db.session
    data = db_session.query(db.frequency).filter(db.frequency.owner == username).all()

    data_dumped = json.dumps(data, cls=AlchemyEncoder)

    db_session.close()

    return data_dumped   

def get_Frequency(ids):
    """
    Restituisce la frequenze presente sul DB con un ID specifico
    """

    db = Database()
    db_session = db.session
    data = db_session.query(db.frequency).filter(db.frequency.id == ids).all()

    data_dumped = json.dumps(data, cls=AlchemyEncoder)

    db_session.close()

    return data_dumped 

def get_lastFrequency():
    """
    Restituisce l'ultima frequenza sul DB
    """
    allFrequency = get_allFrequency()

    allFrequencyLoaded = json.loads(allFrequency)

    lastFrequency = allFrequencyLoaded[-1]

    return(int(lastFrequency['id']))

def assign_LastFrequencyNumber(username):
    """
    Assegna l'ultima frequenza
    """
    try:
        def find_missing(lst):
            return [x for x in range(1000, lst[-1]+1) if x not in lst]

        frequencys = []

        db = Database()
        db_session = db.session

        allFrequency = get_allFrequency()
        allFrequencyLoaded = json.loads(allFrequency)

        for a in allFrequencyLoaded:
            frequencys.append(a['id'])

        FrequencyMissing = find_missing(frequencys)
        frequencys.sort()

        if frequencys[-1] == 1999:
            # TODO: Impletare che controlla le riallocabili!!!
            return False


        if FrequencyMissing:
            lastFrequencyNumber = FrequencyMissing[0]
            try:
                db_session.add(db.frequency(id=lastFrequencyNumber,owner=username, reallocable=0, occuped=1))
                db_session.commit()
                db_session.close()
                return lastFrequencyNumber
            except Exception as e:
                print(e)
                return False
        else:
            lastFrequency = frequencys[-1]

            lastFrequencyNumber = lastFrequency+1
            try:
                db_session.add(db.frequency(id=lastFrequencyNumber,owner=username, reallocable=0, occuped=1))
                db_session.commit()
                db_session.close()

                return lastFrequencyNumber
            except Exception as e:
                print(e)
                return False
    except Exception as e:
        print(e)
        return False



