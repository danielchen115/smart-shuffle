import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import track
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_playlist_tracks(sp, playlist_id):
    tracks = {}
    track_objects = sp.playlist_tracks(playlist_id=playlist_id, fields="items(track(id,name))")["items"]
    for track_obj in track_objects:
        tracks[track_obj["track"]["id"]] = track.Track(track_obj["track"]["id"], track_obj["track"]["name"])
    return tracks


def set_track_features(sp, tracks):
    track_ids = list(tracks.keys())
    features = []
    chunks = [track_ids[i * 100:(i + 1) * 100] for i in range((len(track_ids) + 100 - 1) // 100)]
    for chunk in chunks:
        features.extend(sp.audio_features(chunk[:100]))
    for feature in features:
        tracks[feature["id"]].set_features(feature)
    return tracks


def tracks_to_matrix(tracks):
    matrix = {"labels": [], "data": []}
    for _, track in tracks.items():
        matrix["labels"].append(track.name)
        matrix["data"].append(track.get_features())
    return matrix
