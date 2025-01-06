from pymongo import MongoClient

MONGO_URI = "mongodb+srv://duyentqcs170619:duyen2503@duyentq.l1iwp.mongodb.net/?retryWrites=true&w=majority&appName=DuyenTQ"
DB_NAME = "books_db"
COLLECTION_NAME = "books"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]