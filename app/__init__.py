"""Initialize API"""
from flask import Flask
from flask_restful import Api

from app.resources import ClientLast, ClientList, ClientCount, Clientele
from app.config import Config

APP = Flask(__name__)
APP.config.from_object(Config)
API = Api(APP)

API.add_resource(ClientLast, '/api/v2/Client/last')
API.add_resource(ClientList, '/api/v2/Client/all')
API.add_resource(ClientCount, '/api/v2/Client/count')
API.add_resource(Clientele, '/api/v2/Client/fromDay')
    