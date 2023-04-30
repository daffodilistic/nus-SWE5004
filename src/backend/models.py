import datetime
from typing import List
from typing import Optional
import uuid
from marshmallow import Schema, fields

# Base class
class User:
    def __init__(self, name, password, account_guid):
        self.name = name
        self.password = password
        self.account_guid = account_guid

    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)

# Schema to serialize and deserialize data
class UserSchema(Schema):
    name = fields.Str()
    password = fields.Str()
    # NOTE - this is to prevent 
    # account_guid = fields.Str() 
    account_guid = fields.UUID(load_default=uuid.uuid4, missing=uuid.uuid4)

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
