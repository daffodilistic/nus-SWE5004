import json
from typing import Union
from fastapi import Request, FastAPI
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.json_util import dumps

import datetime

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