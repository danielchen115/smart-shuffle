from collections import deque
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
import spotipy
import spotify as s
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

NUM_CLUSTERS = 4


class Cluster:
    def __init__(self, location, tracks):
        self.score = 0
        self.location = location
        self.tracks = tracks

    def get_distance(self, other):
        return np.linalg.norm(self.location - other.location)


class ClusterCollection:
    def __init__(self):
        self.clusters = []
        self.curr_i = -1

    def generate_clusters(self, playlist_id):
        tracks = s.get_playlist_tracks(sp, playlist_id)
        s.set_track_features(sp, tracks)
        matrix = s.tracks_to_matrix(tracks)
        data_normalized = normalize(matrix["data"])
        kmeans = KMeans(n_clusters=NUM_CLUSTERS).fit(data_normalized)
        pred_clusters = kmeans.predict(matrix["data"])
        centers = kmeans.cluster_centers_
        for cluster in range(NUM_CLUSTERS):
            new_cluster = Cluster(centers[cluster],
                                  (np.array(matrix["labels"])[np.where(pred_clusters == cluster)]).tolist())
            self.clusters.append(new_cluster)

    def update_scores(self, portion_played):
        portion_left = 1 - portion_played
        for cluster in self.clusters:
            cluster.score += portion_left * cluster.get_distance(self.clusters[self.curr_i])
        self.clusters.sort(key=lambda x: x.score, reverse=True)

    def get_highest_scored_cluster(self):
        max_i = 0
        max_score = 0
        for i, cluster in enumerate(self.clusters):
            if cluster.score > max_score:
                max_i = i
        return max_i

    def create_track_queue(self):
        q = deque()
        for cluster in self.clusters:
            q.extend(cluster.tracks)
        return q
