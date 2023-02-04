import logging
from pymongo import MongoClient
from decouple import config

mongo_pwd = config('MONGODB_PWD')
mongo_user = config('MONGODB_USER')

connection_string = f'mongodb+srv://{mongo_user}:{mongo_pwd}@cluster0.u17j29t.mongodb.net/test'

client = MongoClient(connection_string)

db = client.test


def create_user_collection():
    user_validator = { 
        '$jsonSchema': {
            'bsonType': "object",
            'title': "User Object Validation",
            'required': ["id", "name", "telegram_id"],  
            'properties': {  
                'name': {
                    'bsonType': "string",
                    'description': "'name' must be a string and is required"
                },
                'telegram_id': {
                    'bsonType': "int",
                    'minimum': 0,
                    'description': "'telegram_id' must be an integer and is required"
                },
                'email': {
                    'bsonType': 'email',
                    'description': "'email' must be in a right format if the field exists"
                },
            }
        }
    }
    db.create_collection('student')
    db.command('collMod', 'student', validator=user_validator)


def add_user(user_info):
    collection = db.accountant_bot_collection
    inserted_id = collection.insert_one(user_info).inserted_id
    create_user_collection()
    print(inserted_id)


def add_expense(expense):
    collection = db.accountant_bot_collection
    inserted_id = collection.insert_one(expense).inserted_id

    print(inserted_id)

