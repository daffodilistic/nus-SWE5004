import datetime
from typing import List
from typing import Optional
from marshmallow import Schema, fields

# Base class
class Device:
    def __init__(self, mac_address, last_seen, first_seen, client_secret):
        self.mac_address = mac_address
        self.created_at = datetime.datetime.now()
        self.last_seen = last_seen
        self.first_seen = first_seen
        self.client_secret = client_secret

    def __repr__(self):
        return "<Device(name={self.name!r})>".format(self=self)

# Schema to serialize and deserialize data
class DeviceSchema(Schema):
    mac_address = fields.Str()
    created_at = fields.DateTime()
    last_seen = fields.DateTime()
    first_seen = fields.DateTime()
    client_secret = fields.Str()
