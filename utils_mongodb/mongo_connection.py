from pymongo import MongoClient
import os

__all__ = ['get_db_handle_mongodb']


def get_db_handle_mongodb(database_name):

    client = MongoClient(os.environ.get('MONGO_URL'))
    db_handle = client[database_name]

    return db_handle, client
