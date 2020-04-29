import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from track import Track
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()


class Playlist:
    def __init__(self, playlist_id: str, sp):
        self.sp = sp
        self.playlist_id = playlist_id
        self.__load_playlist(playlist_id)
        self.played = set()

    def __load_playlist(self, playlist_id: str):
        playlist = self.sp.playlist(playlist_id)
        self.name = playlist["name"]
        self.owner = playlist["owner"]
        self.tracks = playlist["tracks"]
        self.uri = playlist["uri"]

    def get_tracks(self):
        tracks = {}
        track_objects = self.sp.playlist_tracks(playlist_id=self.playlist_id, fields="items(track(id,name))")["items"]
        for track_obj in track_objects:
            tracks[track_obj["track"]["id"]] = Track(track_obj["track"]["id"], track_obj["track"]["name"])
        return tracks

    def replace_tracks(self, track_ids: List[str]):
        self.sp.user_playlist_replace_tracks(self.owner, self.playlist_id, track_ids)

    def tracks_to_matrix(self):
        matrix = {"labels": [], "data": []}
        for _, track in self.tracks.items():
            matrix["labels"].append(track.name)
            matrix["data"].append(track.get_features())
        return matrix

    def set_track_features(self):
        track_ids = list(self.tracks.keys())
        features = []
        chunks = [track_ids[i * 100:(i + 1) * 100] for i in range((len(track_ids) + 100 - 1) // 100)]
        for chunk in chunks:
            features.extend(self.sp.audio_features(chunk[:100]))
        for feature in features:
            self.tracks[feature["id"]].set_features(feature)


class SpotifyClient(spotipy.Spotify):
    def __init__(self, auth):
        super().__init__(auth=auth)

    def playlists(self):
        playlist_objects = self.current_user_playlists()["items"]
        playlists = {}
        for playlist in playlist_objects:
            playlists[playlist["id"]] = {
                "uri": playlist["uri"],
                "name": playlist["name"],
                "tracks": playlist["tracks"]["total"],
                "owner": playlist["owner"]["display_name"]
            }
        return playlists

    def new_playlist(self, name: str, user: str):
        res = self.user_playlist_create(user, name)
        return Playlist(res["id"], self)



if __name__ == "__main__":
    pl = Playlist("0ZHdYdAKTl3hxNUGvhBki6")
