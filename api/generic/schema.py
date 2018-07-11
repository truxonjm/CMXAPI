from marshmallow import Schema, fields

"""This module will hold the schema for marshmallow"""
# It's most likely going to take a while to reformat a lot of things to make it work
# This might not be worth it to do, but I feel like it would be beneficial later on
# as I'm adding complexity to the models.

# I feel this will be especially useful once the analytics are starting to be implemented

# As of now I only have the modules installed for marshmallow, marshmallow-sqlalchemy and flask-marshmallow 
# which all work together. 

class BaseSchema():
    class LogSchema(Schema):
        id = fields.Integer,
        RangeStart = fields.Str(),
        RangeEnd = fields.Str(),
        Timestamp = fields.Str(),
        ClientCount = fields.Integer
    
class CompositeSchema():
    class ClientSchema(Schema):
        id = fields.Integer,
        MacAddress = fields.Str(),
        MapHierarchyString = fields.Str(),
        MapCampus = fields.Str(),
        MapBuilding = fields.Str(),
        MapFloor = fields.Str(),
        MapZones = fields.Str(),
        MapCoordinateX = fields.Integer,
        MapCoordinateY = fields.Integer,
        MapCoordinateZ = fields.Integer,
        MapCoordinateUnit = fields.Str(),
        CurrentlyTracked = fields.Str(),
        ConfidenceFactor = fields.Integer,
        LocComputeType = fields.Str(),
        CurrentServerTime = fields.Str(),
        FirstLocatedTime = fields.Str(),
        LastLocatedTime = fields.Str(),
        HistoryLogReason = fields.Str(),
        GeoCoordinate = fields.Str(),
        RawLocation = fields.Str(),
        NetworkStatus = fields.Str(),
        ChangedOn = fields.Str(),
        IpAddress = fields.Str(),
        UserName = fields.Str(),
        SsId = fields.Str(),
        SourceTimestamp = fields.Str(),
        Band = fields.Str(),
        ApMacAddress = fields.Str(),
        Dot11Status = fields.Str(),
        Manufacturer = fields.Str(),
        AreaGlobalIdList = fields.Str(),
        DetectingControllers = fields.Str(),
        BytesSent = fields.Integer,
        BytesReceived = fields.Integer,
        GuestUser = fields.Str(),
        RequestLogID = fields.Integer

class AnalyticSchema():