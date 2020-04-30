from flask import Flask, render_template, request, jsonify
from spotify import SpotifyClient
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


@app.route('/set-playlist', methods=['POST'])
def set_playlist():
    token = request.headers.get('token')
    user = request.headers.get('username')
    sp = SpotifyClient(auth=token)
    playlist = sp.get_playlist(request.form['playlist_id'])
    Session(user).set("playlist", playlist)


if __name__ == "__main__":
    app.run(debug=True)
