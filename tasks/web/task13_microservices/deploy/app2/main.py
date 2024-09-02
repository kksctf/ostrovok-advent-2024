#!/usr/bin/env python

# Idea

from fastapi import FastAPI, Response
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles 
from mimetypes import guess_type

from pydantic import BaseModel

app = FastAPI(title="task13_microservices_service2")
    

@app.get("/")
def index(req: Request):
    return {"message": "Hello from ChaikaDoormanCargo. Cost: 10$."}

@app.get("/getdoorman")
def get_cleaning(req:Request) -> Response:
    return {"Status": "Not working today"}