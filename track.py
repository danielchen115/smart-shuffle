class Track:
    def __init__(self, obj):
        self.id = obj["id"]
        self.name = obj["name"]
        self.duration = obj["duration_ms"]
        self.uri = obj["uri"]

        self.danceability = 0
        self.energy = 0
        self.acousticness = 0
        self.valence = 0
        self.instrumentalness = 0
        self.liveness = 0
        self.loudness = 0
        self.speechiness = 0
        self.tempo = 0

    @classmethod
    def by_id(cls, track_id, sp):
        return Track(sp.track(track_id))

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

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

    def portion_played(self, progress):
        return progress / self.duration
