FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /python-docker

RUN pip3 install flask==3.0.3
RUN pip3 install pyjwt==2.9.0
RUN pip3 install flask_jwt_extended==4.6.0

COPY . .

CMD [ "python3", "main.py"]