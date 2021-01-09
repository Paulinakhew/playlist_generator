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

        result = cp.add_submitted_songs_to_playlist(submitted_songs)

        if result:
            return render_template("get_info.html", success=True, info=result)
        else:
            return render_template("get_info.html", failure=True)
    else:
        return render_template("get_info.html")


if __name__ == "__main__":
    app.run(debug=True)
