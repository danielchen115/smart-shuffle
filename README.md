# Smart Shuffle
A heuristic-based "Shuffle" play that tunes itself based on listening times of previous songs. Finds out what you like and don't like to pick the next song accordingly.

## Approach
First, songs are clustered based on its audio features (energy, danceability, vibe, etc.) using k-means clustering.
Each cluster holds a score to determine how _likeable_ its songs are to the user's current listening patterns. If a song is skipped,
each cluster's score is updated based on its distance from the current cluster. The next song is then picked from the highest score cluster.
