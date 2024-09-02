#!/usr/bin/env python

import hashlib
import os
from pathlib import Path

from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageDraw, ImageFont

app = Flask(
    "task5_eating",
    template_folder=Path(__file__).parent / "templates",
    static_folder=Path(__file__).parent / "static",
)

flag = r"CTF{EXAMPLE}" if "FLAG" not in os.environ else os.environ["FLAG"]

img = Image.open(app.static_folder + "/flag.png")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(app.static_folder + "/font.ttf", 48)
draw.text((200, 200), flag, (255, 255, 255), font=font)
img.save(app.static_folder + "/../flag_processed.jpg")

users_db = {
    "user1": hashlib.md5(
        b"user1_password"
    ).hexdigest(),  # b4ca6e90dcef1196a20930c2d9ecfbc0
    "user2": hashlib.md5(
        b"user2_password"
    ).hexdigest(),  # 049914ab3268e59eb90526f64a5322d9
    "admin": float(
        hashlib.md5(b"mega_strong_password175183428").hexdigest()
    ),  # 0e******************************
}


def check_admin_credentials(username, password) -> bool:
    try:
        hashed_password = float(hashlib.md5(password.encode()).hexdigest())
        if username in users_db and users_db[username] == hashed_password:
            return True
        return False
    except ValueError:
        return False


def check_credentials(username, password) -> bool:
    try:
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if username in users_db and users_db[username] == hashed_password:
            return True
        return False
    except ValueError:
        return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        Path(__file__).parent / "static",
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/process", methods=["POST"])
def process():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "admin":
        if check_admin_credentials(username, password):
            return send_from_directory(
                Path(__file__).parent, "flag_processed.jpg", mimetype="image/png"
            )
        else:
            return render_template("sad.html")
    else:
        if check_credentials(username, password):
            return render_template("success.html")
        else:
            return render_template("sad.html")


app.run(host="0.0.0.0", port=1337)
