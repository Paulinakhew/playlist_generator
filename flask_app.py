#!usr/bin/env python3
from flask import Flask, redirect, render_template, request
import create_playlist as c

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def get_info():
    if request.method == "GET":
        return render_template("get_info.html")
    elif request.method == "POST":
        # TODO: add try/except here
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
            return render_template("get_info.html", failure=True, info=result)
        elif result and 'snapshot_id' in result:
            return render_template("get_info.html", success=True, info=result)
        return render_template("get_info.html")
    else:
        return render_template("get_info.html")


if __name__ == "__main__":
    app.run(debug=True)
