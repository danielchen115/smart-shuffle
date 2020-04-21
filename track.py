class Track:
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.danceability = 0
        self.energy = 0
        self.acousticness = 0
        self.valence = 0
        self.instrumentalness = 0
        self.liveness = 0
        self.loudness = 0
        self.speechiness = 0
        self.tempo = 0

    def set_features(self, features):
        for key in features:
            if hasattr(self, key):
                setattr(self, key, features[key])

    def get_features(self):
        # Adjusted based on empirical best results
        return [
            self.danceability,
            self.energy,
            self.acousticness,
            self.valence,
            self.instrumentalness,
            # self.liveness,
            # self.loudness,
            self.speechiness,
            # self.tempo,
        ]
