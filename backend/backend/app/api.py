import json
import logging

from fastapi import FastAPI
from pymongo import MongoClient

from bson.objectid import ObjectId

from kafka import KafkaProducer
from fastapi.middleware.cors import CORSMiddleware

mongo_client = MongoClient('mongodb://mongo:27017/')
todo_list_db = mongo_client["todo_list_database"]
todo_collection = todo_list_db['todo_list']

import os

print(os.environ)
logging.info(os.environ)

producer = KafkaProducer(
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    bootstrap_servers='kafka:9092',
    api_version=(0, 11, 5)
)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "0.0.0.0:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}


@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return {"data": [
        {'id': str(i['_id']), 'item': i['item']
         } for i in todo_collection.find()]}


@app.post("/todo", tags=["todos"])
async def add_todo(todo: dict) -> dict:
    r = todo_collection.insert_one(todo)
    producer.send('todo_updates', value={'action': 'add'})

    # logging.error("Yay! Error log message!")
    # raise Exception("Yay! Exception!")

    return {
        "id": str(r.inserted_id),
        "data": {"Todo added."},
    }


@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: str, body: dict) -> dict:
    result = todo_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"item": body['item']}})
    if result is not None:
        return {"data": f"Todo with id {id} has been updated."}
    return {"data": f"Todo with id {id} not found."}


@app.delete("/todo/{id}", tags=["todos"])
async def delete_todo(id: str) -> dict:
    result = todo_collection.delete_one({'_id': ObjectId(id)})
    producer.send('todo_updates', value={'action': 'delete'})
    if result.deleted_count == 0:
        return {"data": f"Todo with id {id} not found."}
    return {"data": f"Todo with id {id} has been removed."}
