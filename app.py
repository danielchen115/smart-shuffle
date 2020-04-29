from flask import Flask, render_template, request, jsonify
from spotify import SpotifyClient, Playlist

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/playlists', methods=['GET', 'POST'])
def playlists():
    token = request.form['token']
    sp = SpotifyClient(auth=token)
    playlists = sp.playlists()
    data = {"playlists": playlists}
    return jsonify(data)


@app.route('/skip', methods=['POST'])
def skip():
    token = request.form['token']


if __name__ == "__main__":
    app.run(debug=True)
