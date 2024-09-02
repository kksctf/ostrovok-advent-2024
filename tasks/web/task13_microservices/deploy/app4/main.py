#!/usr/bin/env python

# Idea

from fastapi import FastAPI, Response
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles 
from mimetypes import guess_type
import os
import urllib
import httpx as http

from pydantic import BaseModel

from httpx_file import FileTransport
from httpx import Client
client = Client(mounts={'file://': FileTransport()})


app = FastAPI(title="task13_microservices_service4")

flag = r'CTF{EXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG'].replace('"','')
###
f = open("/etc/flag.txt", "w")
f.write(flag)
f.close()
###

@app.get("/")
def index(req: Request):
    return {"message": "Hello from Offices"}

@app.get("/getoffice")
def get_cleaning(req:Request) -> Response:
    return {"Status": "Ok", "Data":"Use /file to get file from host in inner network"}

@app.get("/file/{href:path}")
def make_request(req:Request, href:str | None = None) -> dict:
    if href != None:
        try:
            href = urllib.parse.unquote(href)
            r = client.get(url=href)
            return {"Status": "Ok", "Data":r.text}
        except Exception as e:
            return {"Status": "Not ok", "Error":str(e)}
    return {"Status": "href not found"}  # Must be hint