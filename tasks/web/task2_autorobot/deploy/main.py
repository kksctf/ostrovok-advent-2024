#!/usr/bin/env python

from flask import Flask, request, render_template, redirect, render_template_string, Response
import os
import hashlib
import random
import string


app = Flask("task2_autorobot",
            template_folder=".",
            static_folder="./static")

flag = r'CTF{EXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG']
DEBUG_VAR = False
# -------------------------------------------------------------------------- #

STAGES_COUNT = 256
def generate_db():
    bytes_in_id = 32
    last_id = hashlib.md5(bytes(random.randbytes(bytes_in_id))).hexdigest()
    db = {hashlib.md5(bytes(random.randbytes(bytes_in_id))).hexdigest():last_id}
    # set?
    for i in range(STAGES_COUNT):
        rand_id = hashlib.md5(bytes(random.randbytes(bytes_in_id))).hexdigest()

        if rand_id not in db.keys():
            db[last_id] = rand_id
        else:
            db[last_id] = hashlib.md5(rand_id.encode()).hexdigest()
        
        last_id = rand_id

    db[last_id] = flag
    return db

db = {}
is_db_ok=False
while not is_db_ok:
    db = generate_db()                   # collisions moment
    is_db_ok = True
    if len(db.keys()) == STAGES_COUNT+2: # with 0-stage and flag-stage
        is_db_ok = True
    

if DEBUG_VAR:
    idx=0
    for i in db.keys():
        print("{} {} --> {}".format(idx, i, db[i]))
        idx+=1
    print(len(db.keys()))
# -------------------------------------------------------------------------- #
robots_form = "User-agent: * \nDisallow: /{} \nAllow: /hint/"
@app.route("/robots.txt")
def robots_route():
    r = Response(response=robots_form.format(list(db.keys())[0]), status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r
    return render_template_string(robots_form.format(list(db.keys())[0]))

@app.route("/<id_route>")
def id_route(id_route=None):
    if id_route == flag:
        return flag
    return id_route

@app.route("/<id_route>/robots.txt")
def robot_id_route(id_route=None):
    if id_route not in db.keys():
        return "HUM4N D3T3C73D"

    return render_template_string(robots_form.format(db[id_route]))

@app.route("/hint")
def hint_route():
    return '<html><body><a href="https://pypi.org/project/requests/">Link</a></body></html>'

@app.route("/")
def index():
    return render_template("index.html")


app.run(host="0.0.0.0",
        port=1337,
        debug=DEBUG_VAR)