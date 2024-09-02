#!/usr/bin/env python

# Idea

# У нас два слоя таска - есть front для door services и что-то на бекенде.
# Два раза надо проэксплуатировать SSRF - в одном случае мы это понимаем по информации с ручки /available, во второй - по query параметру? TODO: продумать office сервис
# В офисе происходит прямой доступ к фс без фильтрации урла и можно вытащить file:///etc/flag.txt

import urllib.parse
from fastapi import FastAPI, Response
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles 
from mimetypes import guess_type
import os
import httpx as http
import urllib
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates


DEBUG_VAR = True


class Service(BaseModel):
    id: int
    is_public: bool
    protocol: str
    name: str
    addr: str


app = FastAPI(title="task13_microservices", docs_url=None, redoc_url=None, openapi_url=None)
templates = Jinja2Templates(directory=".")
app.mount("/static", StaticFiles(directory="static"))

@app.get("/favicon.ico")
def get_favicon(req: Request) -> RedirectResponse:
    return RedirectResponse(url="/static/favicon.ico")


@app.get("/available")
def available_services() -> list[Service]:
    services = [
        Service(id=0, is_public=True, protocol="OpenAPI", name="ChaikaCleaning", addr="cleaning-chaika-local"),
        Service(id=1, is_public=True, protocol="OpenAPI", name="ChaikaDoormanCargo", addr="doorman-chaika-local"),
        Service(id=2, is_public=True, protocol="OpenAPI", name="ChaikaFlagsLaundry", addr="laundry-chaika-local"),
        Service(id=3, is_public=False, protocol="OpenAPI",name="ChaikaOffices", addr="offices-chaika-local")
    ]
    return services

@app.get("/request/{href:path}")
def make_request(req:Request, href:str | None = None) -> dict:
    if href != None:
        try:
            href = urllib.parse.unquote(href)
            r = http.get(url=href)
            return {"Status": "Ok", "Data":r.text}
        except Exception as e:
            return {"Status": "Not ok", "Error":str(e)}
    return {"Status": "href not found"}  # Must be hint

@app.get("/")
def index(req: Request):
    return templates.TemplateResponse(request=req, name="index.html")
