FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

COPY . .

RUN pip3 install -r requirements.txt
RUN pip install fastapi uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "80"]