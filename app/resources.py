"""API routing and Database Connection"""
from flask_restful import Resource, ResponseBase, fields, marshal_with
from flask import request
from sqlalchemy import Column, String, DateTime, Float, Integer, create_engine, func, Boolean, BigInteger, Text, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import Config
from app.connection import safe_session, DEBUGGER, LOGGER

import time
import json

import dateutil.parser

DB=Config.DB
ENGINE = create_engine(DB['URI'])
SESSION = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=ENGINE
                                      )
                        )
BASE = declarative_base(bind=ENGINE)
"""CLIENT_FIELDS = {
    'id': fields.Integer,
    'datetime': fields.DateTime(dt_format='rfc822'),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
}"""

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
            clients = [Client(client) for client in json.loads(req.text)]
            for client in clients:
                SESSION.add(client)
                SESSION.commit() 
            return clients[0]
        finally:
            t1 = time.time()
            DEBUGGER.debug('Took {} seconds'.format(t1-t0))
         

class ClientLast(Resource):
    #@marshal_with(CLIENT_FIELDS)
    def get(self):
        return SESSION.query(Client).order_by(-Client.id).first()

class ClientList(Resource):
    #@marshal_with(CLIENT_FIELDS)
    def get(self):
        return SESSION.query(Client).all()

class Now(Resource):
    #@marshal_with(CLIENT_FIELDS)
    def get(self):
        return Jeeves.get_clients

class Client(BASE):
    """ORM Class Model for the Client object\n
    Arguments:
        BASE {DeclarativeMeta} -- Constructor Object Type.
    """

    __tablename__ = 'Client'
    def __init__(self, jsonData):
        clientData = jsonData

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

    id = Column(Integer, primary_key=True)
    MacAddress = Column(String(50))
    MapHierarchyString = Column(String(100))
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
    Manufacturer = Column(String(50))
    AreaGlobalIdList = Column(String(50))
    DetectingControllers = Column(String(50))
    BytesSent = Column(Integer)
    BytesReceived = Column(Integer)
    GuestUser = Column(String(50))
