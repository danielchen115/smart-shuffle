from flask import Flask, render_template, request, jsonify
from spotify import SpotifyClient, Playback
from cluster import ClusterCollection
from session import Session

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/playlists', methods=['GET'])
def playlists():
    token = request.headers.get('token')
    sp = SpotifyClient(auth=token)
    playlists = sp.get_playlists()
    data = {"playlists": playlists}
    return jsonify(data)


@app.route('/set-playlist', methods=['PUT'])
def set_playlist():
    token = request.headers.get('token')
    user = request.headers.get('username')
    sp = SpotifyClient(auth=token)
    playlist = sp.get_playlist(request.form['playlist_id'])
    Session(user).set("playlist", playlist)
    Session(user).set("clusters", ClusterCollection(playlist, sp))
    playback = Playback(sp)
    playback.new_queue(playlist.tracks.items())
    Session(user).set("playback", playback)


@app.route('/play', methods=['PUT'])
def play():
    user = request.headers.get('username')
    playback = Session(user).get("playback")
    playback.play()


@app.route('/pause', methods=['PUT'])
def pause():
    user = request.headers.get('username')
    playback = Session(user).get("playback")
    playback.pause()


@app.route('/skip', methods=['PUT'])
def skip():
    user = request.headers.get('username')
    playback = Session(user).get("playback")
    playback.skip()


if __name__ == "__main__":
    app.run(debug=True)
