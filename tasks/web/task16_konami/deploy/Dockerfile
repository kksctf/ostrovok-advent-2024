FROM python:3.12-alpine

RUN pip install uvicorn fastapi

RUN mkdir /app
COPY main.py /app

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
