from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
import spotipy
import spotify as s
import pandas as pd
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

NUM_CLUSTERS = 4

def generate_clusters(playlist_id):
    tracks = s.get_playlist_tracks(sp, playlist_id)
    s.set_track_features(sp, tracks)
    matrix = s.tracks_to_matrix(tracks)
    data_normalized = normalize(matrix["data"])
    kmeans = KMeans(n_clusters=NUM_CLUSTERS).fit(data_normalized)
    clusters = kmeans.predict(matrix["data"])
    for cluster in range(NUM_CLUSTERS):
        print('cluster: ', cluster)
        print(np.array(matrix["labels"])[np.where(clusters == cluster)])


if __name__ == "__main__":
    generate_clusters("1rRd3sbV22wzxF4crXauTF")
