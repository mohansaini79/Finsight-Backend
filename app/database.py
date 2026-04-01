from pymongo import MongoClient, ASCENDING
from app.config import settings

client = MongoClient(settings.mongo_uri)
db = client[settings.mongo_db_name]

users_collection = db["users"]
financial_records_collection = db["financial_records"]


def create_indexes() -> None:
    users_collection.create_index([("email", ASCENDING)], unique=True)
    users_collection.create_index([("role", ASCENDING)])
    users_collection.create_index([("is_active", ASCENDING)])

    financial_records_collection.create_index([("type", ASCENDING)])
    financial_records_collection.create_index([("category", ASCENDING)])
    financial_records_collection.create_index([("date", ASCENDING)])
    financial_records_collection.create_index([("created_by", ASCENDING)])
    financial_records_collection.create_index([("is_deleted", ASCENDING)])