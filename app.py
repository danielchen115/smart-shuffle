from flask import Flask, render_template, request, jsonify
from spotify import SpotifyClient, Playback, Playlist
from cluster import ClusterCollection
from session import Session

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/playlists", methods=["GET"])
def playlists():
    token = request.headers.get("token")
    sp = SpotifyClient(auth=token)
    playlists = sp.get_playlists()
    data = {"playlists": playlists}
    return jsonify(data)


@app.route("/set-playlist", methods=["PUT"])
def set_playlist():
    token = request.headers.get("token")
    user = request.headers.get("username")
    sp = SpotifyClient(auth=token)
    playlist_uri = request.form["playlist_uri"]
    playlist = sp.get_playlist(Playlist.uri_to_id(playlist_uri))
    Session(user).set("playlist", playlist)
    Session(user).set("clusters", ClusterCollection(playlist, sp))
    playback = Playback(sp)
    playback.new_queue(list(playlist.tracks.values()))
    Session(user).set("playback", playback)
    return jsonify(success=True)


@app.route("/play", methods=["PUT"])
def play():
    user = request.headers.get("username")
    playback = Session(user).get("playback")
    playback.play()
    res = jsonify(success=True)
    res.status_code = 200
    return res


@app.route("/pause", methods=["PUT"])
def pause():
    user = request.headers.get("username")
    playback = Session(user).get("playback")
    playback.pause()
    res = jsonify(success=True)
    res.status_code = 200
    return res


@app.route("/skip", methods=["PUT"])
def skip():
    user = request.headers.get("username")
    playback = Session(user).get("playback")
    playback.skip()
    res = jsonify(success=True)
    res.status_code = 200
    return res


if __name__ == "__main__":
    app.run(debug=True)
