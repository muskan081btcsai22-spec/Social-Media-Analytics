# Simple config placeholder. Set secrets and URIs via env vars in production.
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'sma_db')
APIFY_TOKEN = os.environ.get('APIFY_TOKEN')
