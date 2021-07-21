import pymongo
import os

#! Local
from dotenv import load_dotenv, find_dotenv
from pymongo import cursor
load_dotenv(find_dotenv())

# Connect mongo
client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
db = client['study']

# Insert a document
db.develop.insert_one({'test': 'test'})

# Get all documents
cursor = db.develop.find({})

# Print documents
for idx, val in enumerate(cursor):
    print(idx, val)
