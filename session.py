import os
import redis
import pickle
from spotify import Playlist
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

    def set_playlist(self, playlist: Playlist):
        pickled_playlist = pickle.dumps(playlist)
        self.r.hset(self.user_id, "playlist", pickled_playlist)

    def get_playlist(self):
        playlist = self.r.hget(self.user_id, "playlist")
        return pickle.loads(playlist)
