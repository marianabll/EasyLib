from app import mongo
from bson.objectid import ObjectId

class UserModel:
    @staticmethod
    def get_user_by_username(username):
        return mongo.db.Users.find_one({"username": username})
