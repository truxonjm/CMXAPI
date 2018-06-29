"""API routing and Database Connection"""

import json

from flask_restful import Resource, marshal_with

import api
from api.models import Client, Client_Fields, Log_Fields, RequestLog
from api.database import session

class Util():
    @marshal_with(Log_Fields)
    def format_log(log):
        """Converts RequestLog objects to json"""
        return log

    @marshal_with(Client_Fields)
    def format_clients(clients):
        """Converts Client objects to json"""
        return clients

class ClientResource():

    class CLatest(Resource):
        """Last client stored in the database

        Returns:
            json -- last client stored in the database
        """
        @marshal_with(Client_Fields)
        def get(self):
            return Client.most_recent()

    class CAll(Resource):
        """[NOT RECOMMENDED FOR USE!]  Client list from local database

        Returns:
            json -- all clients from local database
        """
        @marshal_with(Client_Fields)
        def get(self):
            return Client.group.all_()

    class CCount(Resource):
        """Number of clients stored in the database

        Returns:
            json -- number of clients stored in the database
        """
        def get(self):
            return {"Count(Client)":Client.group.count()}

class RequestLogResource():

    class LLatest(Resource):
        """Last request log stored in the database

        Returns:
            json -- last request log stored in the database
        """
        @marshal_with(Log_Fields)
        def get(self):
            return RequestLog.most_recent()

    class LAll(Resource):
        """RequestLog list from local database

        Returns:
            json -- all request logs from local database
        """
        @marshal_with(Log_Fields)
        def get(self):
            return RequestLog.group.all_()

    class LCount(Resource):
        """Number of request logs stored in the database

        Returns:
            json -- number of request logs stored in the database
        """
        def get(self):
            return {"Count(RequestLog)":RequestLog.group.count()}
    
class CMXResource():

    class pull(Resource):
        """Pull and store data from CMX
        
        Returns:
            json -- stored clients
        """        
        def get(self):
            _log, _clients = api.stepper.base_iterate()
            _request_data = {}
            _request_data['RequestLog'] = Util.format_log(_log)
            _request_data['Clients'] = Util.format_clients(_clients)
            return _request_data

class TestResource():

    class cmx():

        class client_count(Resource):
            """Quantity of clients in test call
            
            Returns:
                json -- number of clients in the call
            """
            def get(self):
                _start = 1528473784691
                _step = 180000
                api.stepper.get_client_data_in_range(_start, _step)
                return {'StepCount':len(_client_data)}
