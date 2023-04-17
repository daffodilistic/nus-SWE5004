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