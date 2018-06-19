from flask_restful import fields
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, Float, Integer,
                        SmallInteger, String, Text)

import dateutil.parser
from app.database import BASE

CLIENT_FIELDS = {
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
    'GuestUser': fields.String()
}

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
    id = Column(Integer, primary_key=True)
