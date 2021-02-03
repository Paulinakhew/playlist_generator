#!usr/bin/env python3
from flask import abort, Flask, make_response, redirect, render_template, request
import logging
import os
import secrets
import string
from urllib.parse import urlencode

import create_playlist as c


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG
)


# Client info
CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI')

# Spotify API endpoints
AUTH_URL = 'https://accounts.spotify.com/authorize'
SEARCH_ENDPOINT = 'https://api.spotify.com/v1/search'


# Start 'er up
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth')
def auth():

    state = ''.join(
        secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
    )

    # Request authorization from user
    # Only including `state` here for error logging purposes.
    payload = {
        'client_id': CLIENT_ID,
        'response_type': 'token',
        'redirect_uri': REDIRECT_URI,
        'scope': 'playlist-modify-public playlist-modify-private',
        'state': state
    }

    res = make_response(redirect(f'{AUTH_URL}/?{urlencode(payload)}'))

    return res


@app.route("/callback", methods=["GET", "POST"])
def callback():
    if request.method == "GET":
        error = request.args.get('error')
        state = request.args.get('state')

        if error:
            app.logger.error('Error: %s, State: %s', error, state)
            abort(400)

        return render_template('profile.html')
    elif request.method == "POST":
        cp = c.CreatePlaylist()

        submitted_token = request.form["token"]
        submitted_userid = request.form["userid"]
        cp.set_credentials(submitted_userid, submitted_token)

        submitted_songs = request.form["songs"]
        del1 = request.form["del1"]
        del2 = request.form["del2"]

        playlist_name = request.form['playlist_name']
        playlist_description = request.form['playlist_description']

        # artist_song = request.form['artist_song']
        if request.form.get('artist_song'):
            artist_song = True
        else:
            artist_song = False

        result = cp.add_submitted_songs_to_playlist(submitted_songs, del1, del2, playlist_name, playlist_description, artist_song)

        if result and 'error' in result:
            return render_template("profile.html", failure=True, info=result)
        elif result and 'snapshot_id' in result:
            return render_template("profile.html", success=True, info=result)
        return render_template("profile.html")
    else:
        return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)
