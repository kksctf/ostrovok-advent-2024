FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /python-docker

RUN pip3 install flask==3.0.3

COPY ./app .

CMD [ "python3", "main.py"]