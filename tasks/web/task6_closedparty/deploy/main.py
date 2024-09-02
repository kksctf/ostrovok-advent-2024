#!/usr/bin/env python

# Idea
# У нас пати у чаек. Крабы хотят туда попасть.
# Вход защищен печенькой - jwt кукой
# Чтобы решить таск - надо ее подделать.
# Благо нам известны:
# -- Сорцы. Оставить роут и настройки приложения, чтобы вытащить алгоритм генерации JWT_SECRET_KEY.
# -- По ручке /banned нам будет отдаваться список "непрошенных" чаек. Для того, чтобы не перебирать все возможные варианты,
#    а найти сразу нужный.

# TODO:
# Выдать участникам версии библиотек:
# flask==3.0.3
# flask_jwt_extended==4.6.0
# pyjwt==2.9.0

from flask import Flask, request, redirect, make_response , jsonify, send_from_directory
from flask_jwt_extended import create_access_token, get_jwt , jwt_required, JWTManager, set_access_cookies
import random
import string
import os

flag = r'CTF{EXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG'].replace('"','')
DEBUG_VAR = False

app = Flask("task6_closedparty",
            template_folder=".",
            static_folder="./static")
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

app.config["JWT_SECRET_KEY"] = ''.join([random.choice(string.ascii_letters) for i in range(4)])
app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
jwt = JWTManager(app)
banned_tokens = []

print("SECRET",app.config["JWT_SECRET_KEY"])



@app.route("/")
def index():
    anon_token = create_access_token(identity="Crab#Unknown", additional_claims={"Guest":"Mr. Crabs", "Status":"Not invited to party."}) 
    if DEBUG_VAR:
        print("Generated token:", anon_token)

    resp = make_response(redirect("/enter"))
    set_access_cookies(resp, anon_token)
    return resp

@app.route("/banned")
def banned_list_route():
    return banned_tokens,200

@app.route("/enter", methods=["GET", "POST"])
@jwt_required()
def enter_route():
    if request.cookies["access_token_cookie"] in banned_tokens:
        return "You're banned! Pshel von! Status:{}".format(current_user["Status"]), 404
    
    current_user = get_jwt()
    if "crab" in current_user["Guest"].strip().lower():
        return "Crabs are not allowed", 404

    return jsonify(logged_in_as=current_user["Guest"], flag=flag), 200


if __name__ == "__main__":
    with app.app_context():
        banned_tokens = [create_access_token(identity="Seagull#3316", additional_claims={"Guest":"Mr. Krilleater", "Status":"Banned. Reason: Messed with the Boss."}),
                        create_access_token(identity="Seagull#1238", additional_claims={"Guest":"Mrs. Krilleater", "Status":"Banned. Reason: Messed with the Boss."}),
                        create_access_token(identity="Seagull#6943", additional_claims={"Guest":"Mr. Chayka", "Status":"Banned. Reason: Eats too much fish."})]
        app.run(host="0.0.0.0",
        port=1337,
        debug=DEBUG_VAR)