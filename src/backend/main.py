import json
from typing import Union
from fastapi import Request, FastAPI
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.json_util import dumps

import datetime
import datetime
import secrets
from typing import Union
from fastapi import FastAPI
from randmac import RandMac
from models import Device, DeviceSchema

# In-memory database
# engine = create_engine("sqlite:///mario_toilet.sqlite", echo=True)
# Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/users")
async def create_user(request: Request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mariotoilet']
    users:Collection = db['users']
    user = await request.json()
    user_id = users.insert_one(user)
    user = users.find_one({"_id": user_id.inserted_id})
    user["_id"] = str(user.pop("_id"))
    return {"user": user}

@app.get("/users")
async def retrieve_user():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mariotoilet']
    users:Collection = db['users']
    user_list = list(users.find({}))
    for user in user_list:
        user["_id"] = str(user.pop("_id"))
    return user_list

@app.get("/api/devices/enroll")
def enroll_device():
    test_device_a = Device(RandMac(), datetime.datetime.now() , datetime.datetime.now(), make_client_secret())
    device_schema = DeviceSchema()
    data = device_schema.dump(test_device_a)

    test_device_b = {
        "mac_address": str(RandMac()),
        "last_seen": datetime.datetime.now().isoformat(),
        "first_seen": datetime.datetime.now().isoformat(),
        "client_secret": make_client_secret()
    }
    print(device_schema.load(test_device_b))

    return data

def make_client_secret() -> str:
    return secrets.token_urlsafe(16)
