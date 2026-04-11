"""Drop app MongoDB collections: users, cases, posts.
Use environment variables `MONGO_URI` and `MONGO_DBNAME` or defaults.

WARNING: destructive. This will permanently delete data in those collections.

Usage:
  python scripts/drop_mongo.py --yes
"""
import os
import sys
from pymongo import MongoClient

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
DBNAME = os.environ.get('MONGO_DBNAME', 'sma_db')

def main():
    if '--yes' not in sys.argv:
        print('This will DROP collections: users, cases, posts from DB', DBNAME)
        print('Run with: python scripts/drop_mongo.py --yes')
        return
    client = MongoClient(MONGO_URI)
    db = client[DBNAME]
    to_drop = ['users','cases','posts']
    for c in to_drop:
        if c in db.list_collection_names():
            db[c].drop()
            print('Dropped', c)
        else:
            print('Not present:', c)
    print('Done.')

if __name__ == '__main__':
    main()
