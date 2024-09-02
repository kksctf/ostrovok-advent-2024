FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

COPY . .

RUN pip3 install -r requirements.txt
RUN pip install fastapi uvicorn httpx jinja2

CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "1337"]