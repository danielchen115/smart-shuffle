import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import track
from dotenv import load_dotenv

load_dotenv()


class Playlist:
    def __init__(self, playlist_id):
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        self.playlist_id = playlist_id
        self.__load_playlist(playlist_id)

    def __load_playlist(self, playlist_id):
        playlist = self.sp.playlist(playlist_id)
        self.name = playlist["name"]
        self.owner = playlist["owner"]
        self.tracks = playlist["tracks"]
        self.uri = playlist["uri"]

    def get_playlist_tracks(self):
        tracks = {}
        track_objects = self.sp.playlist_tracks(playlist_id=self.playlist_id, fields="items(track(id,name))")["items"]
        for track_obj in track_objects:
            tracks[track_obj["track"]["id"]] = track.Track(track_obj["track"]["id"], track_obj["track"]["name"])
        return tracks


class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    def set_track_features(self, tracks):
        track_ids = list(tracks.keys())
        features = []
        chunks = [track_ids[i * 100:(i + 1) * 100] for i in range((len(track_ids) + 100 - 1) // 100)]
        for chunk in chunks:
            features.extend(self.sp.audio_features(chunk[:100]))
        for feature in features:
            tracks[feature["id"]].set_features(feature)
        return tracks

    def tracks_to_matrix(self, tracks):
        matrix = {"labels": [], "data": []}
        for _, track in tracks.items():
            matrix["labels"].append(track.name)
            matrix["data"].append(track.get_features())
        return matrix

    def get_playlists(self):
        playlists_objects = self.sp.current_user_playlists()["items"]
        playlists = {}
        for playlist in playlists_objects:
            playlists[playlist["id"]] = {
                "uri": playlist["uri"],
                "name": playlist["name"],
                "tracks": playlist["tracks"]["total"],
                "owner": playlist["owner"]["display_name"]
            }
        return playlists

if __name__ == "__main__":
    playlist = Playlist("0ZHdYdAKTl3hxNUGvhBki6")
