"""API routing and Database Connection"""
import json
import time

from flask import request
from flask_restful import Resource, ResponseBase, fields, marshal_with
from sqlalchemy import func

from app.config import Config
from app.connection import DEBUGGER, LOGGER, safe_session
from app.database import SESSION
from app.models import CLIENT_FIELDS, Client

WEB = Config.WEB

MILLIS_IN_DAY = 86400000

def client_call(start, end):
    t0 = time.time()
    try:
        DEBUGGER.debug('Fetching Clientele')
        arguments = "?locatedAfterTime={}&locatedBeforeTime={}".format(start,end)
        url = WEB['URL']+arguments
        req = safe_session(url, WEB['UID'], WEB['PWD'])
        req.raise_for_status()
    except Exception as x:
        LOGGER.exception('Connection failed: {}'.format(x))
    else:
        DEBUGGER.debug('Connection Successful: {}'.format(req.status_code))
        clients = [Client(client) for client in json.loads(req.text)]
        return clients
    finally:
        t1 = time.time()
        DEBUGGER.debug('Took {} seconds'.format(t1-t0))
        
def get_clients(step, startTime):
    numCalls = MILLIS_IN_DAY/step
    start = startTime
    end = start
    all_clients = []
    while numCalls > 0:
        DEBUGGER.info('{} steps until all clients recieved'.format(numCalls))
        start = end
        end = end+step
        all_clients+=client_call(start,end)
        numCalls-=1
    return all_clients

class ClientLast(Resource):
    @marshal_with(CLIENT_FIELDS)
    def get(self):
        return SESSION.query(Client).order_by(-Client.id).first()

class ClientList(Resource):
    @marshal_with(CLIENT_FIELDS)
    def get(self):
        return SESSION.query(Client).all()

class ClientCount(Resource):
    def get(self):
        return {"count":SESSION.query(Client).count()}

class Clientele(Resource):
    @marshal_with(CLIENT_FIELDS)
    def get(self):
        api = Config.API
        step = api['HISTORY_STEP']
        startTime = api['HISTORY_START']
        return get_clients(step, startTime)