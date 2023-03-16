from typing import Union
from fastapi import FastAPI
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import User, Base

# In-memory database
engine = create_engine("sqlite:///mario_toilet.sqlite", echo=True)
Base.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def read_root():
    with Session(engine) as session:
        # p = User(name='Kate', email="kate@sharklasers.com", password="123456")
        # commit() will be done automatically
        # database session cache will be cleared automatically
        # database connection will be returned to the pool
        # session.add_all([p])
        # session.commit()

        stmt = select(User)

        users = []
        for user in session.scalars(stmt):
            users.append(user)
        return users
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
