import spotipy
from track import Track
from session import Session
from typing import Dict, List


class SpotifyClient(spotipy.Spotify):
    def __init__(self, auth):
        super().__init__(auth=auth)

    def get_playlists(self):
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

    def get_playlist(self, playlist_id):
        return Playlist(playlist_id, self)


class Playlist:
    def __init__(self, playlist_id: str, sp: SpotifyClient):
        self.sp = sp
        self.playlist_id = playlist_id
        self.__load_playlist(playlist_id)
        self.played = set()

    def __load_playlist(self, playlist_id: str):
        playlist = self.sp.playlist(playlist_id)
        self.name = playlist["name"]
        self.owner = playlist["owner"]
        self.tracks = {}
        for track_obj in playlist["tracks"]["items"]:
            track = track_obj["track"]
            self.tracks[track["id"]] = (Track(track))
        self.set_track_features()
        self.uri = playlist["uri"]

    @classmethod
    def uri_to_id(cls, uri):
        return uri.split(':')[-1]

    def __load_tracks(self):
        track_objects = self.sp.playlist_tracks(playlist_id=self.playlist_id, fields="items(track(id,name))")["items"]
        for track_obj in track_objects:
            self.tracks[track_obj["track"]["id"]] = Track(track_obj["track"])

    def replace_tracks(self, track_ids: List[str]):
        self.sp.user_playlist_replace_tracks(self.owner, self.playlist_id, track_ids)

    def tracks_to_matrix(self):
        matrix = {"labels": [], "data": []}
        for _, track in self.tracks.items():
            matrix["labels"].append(track)
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


class Playback:
    def __init__(self, sp: SpotifyClient):
        self.sp = sp
        self.user_id = sp.me()["id"]
        self.track = None
        self.progress = 0
        self.is_playing = False
        self.queue = []
        self.update_state()

    def update_state(self):
        state = self.sp.current_playback()
        if not state:
            return
        self.track = Track(state["item"])
        self.progress = state["progress_ms"]
        self.is_playing = state["is_playing"]

    def new_queue(self, tracks: List[Track]):
        self.queue = [track.uri for track in tracks]

    def play(self):
        self.sp.start_playback()

    def pause(self):
        self.sp.pause_playback()

    def skip(self):
        session = Session(self.user_id)
        playlist = session.get("playlist")
        clusters = session.get("clusters")
        prev_skip_i = self.queue.index(self.track.uri)
        self.update_state()
        curr_i = self.queue.index(self.track.uri)
        playlist.played.update(self.queue[prev_skip_i:curr_i + 1])
        clusters.update_scores(self.track.portion_played(self.progress))
        queue = clusters.create_track_queue()
        self.sp.start_playback(uris=[track.uri for track in queue])


