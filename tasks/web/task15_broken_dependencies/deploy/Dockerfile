FROM python:3.12-alpine

RUN apk add --update-cache \
    bash \
  && pip install uvicorn fastapi \
  && rm -rf /var/cache/apk/*

WORKDIR /app
COPY . /app

CMD ["uvicorn", "api:app", "--port", "8000", "--host", "0.0.0.0"]

