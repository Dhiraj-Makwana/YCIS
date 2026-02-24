import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import DuplicateKeyError

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["ycis_db"]
comments_collection = db["comments"]
comments_collection.create_index("comment", unique=True)

def save_comments(comments):
    for comment in comments:
        try:
            comments_collection.insert_one({"comment": comment})
        except DuplicateKeyError:
            pass