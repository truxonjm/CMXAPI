"""Initialize API"""
from flask import Flask
from flask_restful import Api

from app.resources import ClientLast, ClientList, Now
from app.config import Config

APP = Flask(__name__)
APP.config.from_object(Config)
API = Api(APP)

API.add_resource(ClientLast, '/api/Clients/last')
API.add_resource(ClientList, '/api/Clients')
API.add_resource(Now, '/api/now')
    