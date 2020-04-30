import os
import redis
import pickle
from dotenv import load_dotenv
load_dotenv()


class Session:
    def __init__(self, user_id: str):
        self.r = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            db=os.getenv("REDIS_DB"),
            decode_responses=True
        )
        self.user_id = user_id

    def set(self, obj_type: str, obj):
        pickled = pickle.dumps(obj)
        self.r.hset(self.user_id, obj_type, pickled)

    def get(self, obj_type):
        obj = self.r.hget(self.user_id, obj_type)
        return pickle.loads(obj)

