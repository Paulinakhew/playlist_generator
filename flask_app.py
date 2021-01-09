#!usr/bin/env python3
from flask import Flask, redirect, render_template, request
import create_playlist as c

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def get_info():
    if request.method == "GET":
        return render_template("get_info.html")
    else:
        submitted_token = request.form["token"]
        submitted_userid = request.form["userid"]
        submitted_songs = request.form["songs"]


if __name__ == "__main__":
    app.run(debug=True)
