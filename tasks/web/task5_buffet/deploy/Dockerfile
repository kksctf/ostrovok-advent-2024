FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /python-docker

RUN pip3 install flask pillow

COPY . .

CMD [ "python3", "main.py"]