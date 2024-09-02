FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 7503

CMD ["uvicorn", "main:app", "--host", "0.0.0.0","--port", "1337"]