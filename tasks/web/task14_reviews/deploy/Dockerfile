FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /python-docker

RUN pip3 install flask flask_login flask_sqlalchemy

COPY . .

CMD [ "python3", "app.py"]