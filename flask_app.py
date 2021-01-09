#!usr/bin/env python3
from flask import Flask, redirect, render_template, request
from flask_restful import Api

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def get_info():
    if request.method == "GET":
        return render_template("get_info.html")
    else:
        submitted_username = request.form["username"]
        submitted_password = request.form["password"]
        result = m.log_in(submitted_username, submitted_password)
        if result:
            return redirect("/menu")
        else:
            cannot_login = True
            return render_template("login.html", cannot_login=cannot_login)


if __name__ == "__main__":
    app.run(debug=True)