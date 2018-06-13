"""API routing and Database Connection"""
from flask_restful import Resource, ResponseBase, fields, marshal_with
from flask import request
from sqlalchemy import Column, VARCHAR, DateTime, Float, Integer, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import Config
from app.connection import safe_session, DEBUGGER, LOGGER

import time

DB=Config.DB
ENGINE = create_engine(DB['URI'])
SESSION = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=ENGINE
                                      )
                        )
BASE = declarative_base(bind=ENGINE)
CLIENT_FIELDS = {
    'id': fields.Integer,
    'datetime': fields.DateTime(dt_format='rfc822'),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
}

class Jeeves(object): 
    def get_clients():
        t0 = time.time()
        try:
            DEBUGGER.debug(' * Fetching Clientele, sir.')
            req = safe_session()
            req.raise_for_status()
        except Exception as x:
            LOGGER.exception('Connection failed, {}'.format(x))
        else:
            DEBUGGER.debug('Connection Successful, {}'.format(req.status_code))
            clients = [Client(client) for client in json.loads(req.text))]
            SESSION.add(clients)
            SESSION.commit() 
            return clients[0]
        finally:
            t1 = time.time()
            DEBUGGER.debug('Took {} seconds'.format(t1-t0))
         

class ClientLast(Resource):
    @marshal_with(CLIENT_FIELDS)
    def get(self):
        return SESSION.query(Client).order_by(-Client.id).first()

class ClientList(Resource):
    @marshal_with(CLIENT_FIELDS)
    def get(self):
        return SESSION.query(Client).all()

class Now(Resource):
    @marshal_with(CLIENT_FIELDS)
    def get(self):
        return Jeeves.get_clients

class Client(BASE):
    """ORM Class Model for the Client object\n
    Arguments:
        BASE {DeclarativeMeta} -- Constructor Object Type.
    """

    __tablename__ = 'Client'
    def __init__(self, jsonData):
        clientData = json.loads(jsonData)

    mac = Column(VARCHAR, primary_key=True)
    datetime = Column(DateTime, default=func.now())
    latitude = Column(Float(10))
    longitude = Column(Float(10))
