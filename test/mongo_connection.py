import pymongo
import os

#! Local
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Connect mongo
client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
db = client.test

# Print test connection
print(db)
