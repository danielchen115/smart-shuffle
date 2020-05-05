from collections import deque
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from spotify import SpotifyClient, Playlist
import numpy as np

NUM_CLUSTERS = 4


class Cluster:
    def __init__(self, location, tracks: set):
        self.score = 0
        self.location = location
        self.tracks = tracks

    def get_distance(self, other):
        return np.linalg.norm(self.location - other.location)


class ClusterCollection:
    def __init__(self, playlist: Playlist, sp: SpotifyClient):
        self.clusters = []
        self.curr_i = 0
        self.sp = sp
        self.generate_clusters(playlist)

    def generate_clusters(self, playlist: Playlist):
        playlist.set_track_features()
        matrix = playlist.tracks_to_matrix()
        data_normalized = normalize(matrix["data"])
        kmeans = KMeans(n_clusters=NUM_CLUSTERS).fit(data_normalized)
        pred_clusters = kmeans.predict(matrix["data"])
        centers = kmeans.cluster_centers_
        for cluster in range(NUM_CLUSTERS):
            new_cluster = Cluster(centers[cluster],
                                  set((np.array(matrix["labels"])[np.where(pred_clusters == cluster)]).tolist()))
            self.clusters.append(new_cluster)

    def update_scores(self, portion_played: float):
        portion_left = 1 - portion_played
        for cluster in self.clusters:
            cluster.score += portion_left * cluster.get_distance(self.clusters[self.curr_i])

    def get_highest_scored_cluster(self):
        max_i = 0
        max_score = 0
        for i, cluster in enumerate(self.clusters):
            if cluster.score > max_score:
                max_i = i
        return max_i

    def create_track_queue(self, exclude=None):
        if not exclude:
            exclude = set([])
        clusters = sorted(self.clusters, key=lambda x: x.score, reverse=True)
        q = []
        for cluster in clusters:
            for track in cluster.tracks:
                if track not in exclude:
                    q.append(track)
        return q

