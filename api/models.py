"""Contains the ORM Class Models for Database Objects"""

import json

from flask_restful import fields
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, Float, Integer,
                        SmallInteger, String, func)

import dateutil.parser

from .config import Config
from .generic.database import SafeSession

sess = SafeSession(Config.DB['URI'])

Client_Fields = {
    'id': fields.Integer,
    'MacAddress': fields.String(),
    'MapHierarchyString': fields.String(),
    'MapCampus': fields.String(),
    'MapBuilding': fields.String(),
    'MapFloor': fields.String(),
    'MapZones': fields.String(),
    'MapCoordinateX': fields.Integer,
    'MapCoordinateY': fields.Integer,
    'MapCoordinateZ': fields.Integer,
    'MapCoordinateUnit': fields.String(),
    'CurrentlyTracked': fields.String(),
    'ConfidenceFactor': fields.Integer,
    'LocComputeType': fields.String(),
    'CurrentServerTime': fields.String(),
    'FirstLocatedTime': fields.String(),
    'LastLocatedTime': fields.String(),
    'HistoryLogReason': fields.String(),
    'GeoCoordinate': fields.String(),
    'RawLocation': fields.String(),
    'NetworkStatus': fields.String(),
    'ChangedOn': fields.String(),
    'IpAddress': fields.String(),
    'UserName': fields.String(),
    'SsId': fields.String(),
    'SourceTimestamp': fields.String(),
    'Band': fields.String(),
    'ApMacAddress': fields.String(),
    'Dot11Status': fields.String(),
    'Manufacturer': fields.String(),
    'AreaGlobalIdList': fields.String(),
    'DetectingControllers': fields.String(),
    'BytesSent': fields.Integer,
    'BytesReceived': fields.Integer,
    'GuestUser': fields.String(),
    'RequestLogID:': fields.Integer
}

Log_Fields = {
    'id': fields.Integer,
    'RangeStart': fields.String(),
    'RangeEnd': fields.String(),
    'Timestamp': fields.String(),
    'ClientCount': fields.Integer
}

class LogAndClient():
    @staticmethod
    def to_database(log, clients):
        """Stores the CMX data to the database
        
        Arguments:
            log {RequestLog} -- The log containing the request info
            clients {Client} -- list of all clients in CMX pull
        
        Returns:
            tuple -- the log and client list now stored in the database
        """
        try:
            # Store the RequestLog to the database
            _stored_log = sess.store(log, True)
            # Update the client log id value from the newly made log's id
            Client.group.set_request_id(clients, _stored_log.id)
            # Store the clients to the database
            _stored_clients = sess.store_list(clients)
        except Exception as _x:
            logging.exception('Storage failed: %s', (_x))
        finally:
            return (_stored_log, _stored_clients)

class RequestLog(sess.base):
    """RequestLog -- Holds a log of all requests made to CMX"""

    __tablename__ = 'RequestLog'

    id = Column(Integer, primary_key=True)
    RangeStart = Column(BigInteger)
    RangeEnd = Column(BigInteger)
    Timestamp = Column(DateTime, default=func.now())
    ClientCount = Column(Integer)

    @staticmethod
    def from_step(start, step, client_count):
        """Creates new log from a step range and client count
        
        Arguments:
            start {int} -- start time
            step {int} -- size of step
            client_count {int} -- quantity of clients in request
        
        Returns:
            Request -- new request instantiated with values
        """
        _new_log = RequestLog()
        _end = start + step
        _new_log.RangeStart = start
        _new_log.RangeEnd = _end
        _new_log.ClientCount = client_count
        return _new_log

    @staticmethod
    def most_recent():
        """Returns the most recent log stored in the database
        
        Returns:
            ResourceLog -- the most recent log by RangeEnd
        """
        return sess.session.query(RequestLog).order_by(-RequestLog.RangeEnd).first()

    class group():
        """Functions for groups of RequestLogs"""

        def all_():
            """All request logs stored in database
            
            Returns:
                list -- all request logs
            """
            return sess.session.query(RequestLog).order_by(-RequestLog.RangeEnd).all()

        def count():
            """Number of request logs in database
            
            Returns:
                int -- number of request logs in database
            """
            return sess.session.query(RequestLog).count()
        
class Client(sess.base):
    """Client -- Contains data about a particular point from CMX"""

    __tablename__ = 'Client'

    id = Column(Integer, primary_key=True)
    MacAddress = Column(String(50))
    MapHierarchyString = Column(String(200))
    MapCampus = Column(String(50))
    MapBuilding = Column(String(50))
    MapFloor = Column(String(50))
    MapZones = Column(String(50))
    MapCoordinateX = Column(Integer)
    MapCoordinateY = Column(Integer)
    MapCoordinateZ = Column(Integer)
    MapCoordinateUnit = Column(String(50))
    CurrentlyTracked = Column(String(50))
    ConfidenceFactor = Column(SmallInteger)
    LocComputeType = Column(String(50))
    CurrentServerTime = Column(DateTime(timezone=True))
    FirstLocatedTime = Column(DateTime(timezone=True))
    LastLocatedTime = Column(DateTime(timezone=True))
    HistoryLogReason = Column(String(50))
    GeoCoordinate = Column(String(50))
    RawLocation = Column(String(50))
    NetworkStatus = Column(String(50))
    ChangedOn = Column(BigInteger)
    IpAddress = Column(String(50))
    UserName = Column(String(50))
    SsId = Column(String(50))
    SourceTimestamp = Column(BigInteger)
    Band = Column(String(50))
    ApMacAddress = Column(String(50))
    Dot11Status = Column(String(50))
    Manufacturer = Column(String(100))
    AreaGlobalIdList = Column(String(50))
    DetectingControllers = Column(String(50))
    BytesSent = Column(BigInteger)
    BytesReceived = Column(BigInteger)
    GuestUser = Column(String(50))
    RequestLogID = Column(Integer)

    def populate_data(self, clientData):
        """Populate the data fields of the Client from json text

        Arguments:
            json_data {json} -- json containing data to populate Client
        """
        mapInfo = clientData['mapInfo']
        mapHierarchyDetails = mapInfo['mapHierarchyDetails']
        mapCoordinate = clientData['mapCoordinate']
        statistics = clientData['statistics']

        self.MacAddress = clientData['macAddress']
        self.MapHierarchyString = mapInfo['mapHierarchyString']
        self.MapCampus = mapHierarchyDetails['campus']
        self.MapBuilding = mapHierarchyDetails['building']
        self.MapFloor = mapHierarchyDetails['floor']
        self.MapZones = mapHierarchyDetails['zones']
        self.MapCoordinateX = mapCoordinate['x']
        self.MapCoordinateY = mapCoordinate['y']
        self.MapCoordinateZ = mapCoordinate['z']
        self.MapCoordinateUnit = mapCoordinate['unit']
        self.CurrentlyTracked = clientData['currentlyTracked']
        self.ConfidenceFactor = int(clientData['confidenceFactor'])
        self.LocComputeType = clientData['locComputeType']
        self.CurrentServerTime = dateutil.parser.parse(statistics['currentServerTime'])
        self.FirstLocatedTime = dateutil.parser.parse(statistics['firstLocatedTime'])
        self.LastLocatedTime = dateutil.parser.parse(statistics['lastLocatedTime'])
        self.HistoryLogReason = clientData['historyLogReason']
        self.GeoCoordinate = clientData['geoCoordinate']
        self.RawLocation = clientData['rawLocation']
        self.NetworkStatus = clientData['networkStatus']
        self.ChangedOn = clientData['changedOn']
        self.IpAddress = None if len(clientData['ipAddress'])==0 else clientData['ipAddress'][0]
        self.UserName = clientData['userName']
        self.SsId = clientData['ssId']
        self.SourceTimestamp = clientData['sourceTimestamp']
        self.Band = clientData['band']
        self.ApMacAddress = clientData['apMacAddress']
        self.Dot11Status = clientData['dot11Status']
        self.Manufacturer = clientData['manufacturer']
        self.AreaGlobalIdList = clientData['areaGlobalIdList']
        self.DetectingControllers = clientData['detectingControllers']
        self.BytesSent = clientData['bytesSent']
        self.BytesReceived = clientData['bytesReceived']
        self.GuestUser = clientData['guestUser']

    def set_request_id(self, log_id):
        """Populates the RequestLogId in the client
        
        Arguments:
            log_id {int} -- RequestLog id value
        """
        self.RequestLogID = log_id

    @staticmethod
    def from_json(client_data):
        """Creates Client from json data
        
        Arguments:
            client_data {json} -- data to make client
        
        Returns:
            Client -- the instantiated Client
        """

        _client = Client()
        _client.populate_data(client_data)
        return _client
    
    @staticmethod
    def one_from(req_data):
        """Instatiate a Client from a request.

        Arguments:
            req {Request} -- requests_retry_session response
            to_database {bool} -- Whether to store in database or not (default: {True})            

        Returns:
            Client -- the instantiated client object with data populated from request
        """
        _client = Client.from_json(req_data[0])
        return _client

    @staticmethod
    def most_recent():
        """Most recent Client in database
        
        Returns:
            Client -- The most recent Client
        """

        return session.query(Client).order_by(-Client.SourceTimestamp).first()

    class group():
        """Functions for groups of clients"""
        def from_data(req_data):
            """Instatiate a list of Clients from a request.

            Arguments:
                req {Request} -- requests_retry_session response
                to_database {bool} -- Whether to store in database or not (default: {True})            

            Returns:
                Client list -- the instantiated client list with data populated from request
            """
            _clients = [Client.from_json(client_data) for client_data in req_data]
            return _clients

        def all_():
            """All clients stored in database
            
            Returns:
                list -- all clients
            """
            return api.sess.session.query(Client).order_by(-Client.SourceTimestamp).all()

        def count():
            """Number of clients in database
            
            Returns:
                int -- number of clients in database
            """
            return api.sess.session.query(Client).count()

        def set_request_id(client_group, log_id):
            """Populates the RequestLogIds in all clients
        
            Arguments:
                log_id {int} -- RequestLog id value
            """
            for client in client_group:
                client.set_request_id(log_id)
