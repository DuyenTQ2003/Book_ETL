from config.database import db
from config.log import logger

def load_data(data):
    logger.info("Starting data loading")
    collection = db["books"]
    for item in data:
        collection.update_one({"title": item["title"]}, {"$set": item}, upsert=True)
    logger.info("Data loading complete")
