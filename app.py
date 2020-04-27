from flask import Flask, render_template, request, jsonify
from spotipy import Spotify
from spotify import Playlist

app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/playlists', methods=['GET', 'POST'])
def playlists():
    token = request.form['token']
    sp = Spotify(auth=token)
    playlists = Playlist.all(sp)
    data = {"playlists": playlists}
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
