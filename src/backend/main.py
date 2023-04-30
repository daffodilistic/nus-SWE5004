import json
import traceback
from typing import Union
from bson import UuidRepresentation
from fastapi import HTTPException, Request, FastAPI
from marshmallow import ValidationError
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
from models import Device, DeviceSchema, UserSchema

# In-memory database
# engine = create_engine("sqlite:///mario_toilet.sqlite", echo=True)
# Base.metadata.create_all(engine)

app = FastAPI()
mongodb_client = MongoClient('mongodb://mariotoilet:luigismansion@10.148.0.2:27017/?authSource=mariotoilet', uuidRepresentation='standard')

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/users")
async def create_user(request: Request):
    json_data = await request.json()
    if not json_data:
        raise HTTPException(status_code=400, detail="No input data provided")
    try:
        schema_validator = UserSchema()
        new_user = schema_validator.load(json_data)

        db = mongodb_client['mariotoilet']
        users: Collection = db['users']

        user_id = users.insert_one(new_user)
        
        user_obj = users.find_one({"_id": user_id.inserted_id})
        new_user["_id"] = str(user_obj.get("_id"))

        return new_user
    except ValidationError as err:
        print(traceback.format_exc())
        raise HTTPException(status_code=422, detail=err.messages)


@app.get("/users")
async def retrieve_user():
    db = mongodb_client['mariotoilet']
    users: Collection = db['users']
    user_list = list(users.find({}))
    for user in user_list:
        user["_id"] = str(user.get("_id"))
    return user_list


@app.get("/api/devices/enroll")
def enroll_device():
    device_schema = DeviceSchema()
    test_device_params = {
        "mac_address": str(RandMac()),
        "last_seen": datetime.datetime.now().isoformat(),
        "first_seen": datetime.datetime.now().isoformat(),
        "client_secret": make_client_secret()
    }

    device = device_schema.load(test_device_params)
    device_dump = device_schema.dump(device)

    print("Deserialization Test:")
    print(device)
    print("Serialization Test:")
    print(device_dump)

    return device_dump


def make_client_secret() -> str:
    return secrets.token_urlsafe(16)
