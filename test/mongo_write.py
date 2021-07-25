from bson import json_util
import pymongo
import os
import json
#! Local
from dotenv import load_dotenv, find_dotenv
from pymongo import cursor
load_dotenv(find_dotenv())


# Connect mongo
client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
db = client['study']


def get_next_sequence_value(id_value):
    sequence_document = db.counters.find_one_and_update(
        {'_id': id_value},
        {'$inc': {'sequence_value': 1}}
    )
    return sequence_document['sequence_value']


# Insert a document
db.aluraflix.insert_one(
    {'test': 'test', "_id": get_next_sequence_value('develop')})

# Get all documents
cursor = db.aluraflix.find({})

# Print documents
for idx, val in enumerate(cursor):
    print(idx, val)
