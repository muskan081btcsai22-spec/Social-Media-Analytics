from flask_login import UserMixin
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, data):
        self._data = data
        self.id = str(data.get('_id'))

    @property
    def username(self):
        return self._data.get('username')

    @classmethod
    def get_by_username(cls, db, username):
        data = db.users.find_one({'username': username})
        return cls(data) if data else None

    @classmethod
    def get_by_id(cls, db, uid):
        try:
            oid = ObjectId(uid)
        except Exception:
            return None
        data = db.users.find_one({'_id': oid})
        return cls(data) if data else None
