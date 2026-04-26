# Simple config placeholder. Set secrets and URIs via env vars in production.
import os
from pymongo import MongoClient

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'sma_db')
APIFY_TOKEN = os.environ.get('APIFY_TOKEN')

# Initialize MongoDB connection
client = MongoClient(MONGO_URI)
db = client[MONGO_DBNAME]
