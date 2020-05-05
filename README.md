# Smart Shuffle
A heuristic-based "shuffle" play that tunes itself based on skipped songs and listening times.

## Approach
Popular recommender systems such as content-based and collaborative filtering rely on a history of user behaviour and/or the behaviour of other users. However this is not always feasible.

Smart Shuffle demonstrates a recommender system that does **not** rely on a dataset and can quickly ramp up from a cold start using a heuristic scoring system. Its implementation is described below:

1. Tracks are clustered based on its audio features (energy, danceability, valence, etc.) using k-means clustering. Each cluster is given an initial score of 0.
2. After a track is skipped, the score of each cluster is increased by _portion_skipped * distance from track_. The distance indicates how different the current track is from the tracks within each cluster.
3. Reorder the track queue from the highest to lowest score.
4. Repeat 2 and 3 on each skip.
