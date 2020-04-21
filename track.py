class Track:
    danceability = 0
    energy = 0
    acousticness = 0
    valence = 0
    instrumentalness = 0
    liveness = 0
    loudness = 0
    speechiness = 0
    tempo = 0

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def set_features(self, features):
        for key in features:
            if hasattr(self, key):
                setattr(self, key, features[key])
