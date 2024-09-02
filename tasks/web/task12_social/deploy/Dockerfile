FROM python:3.12-alpine 

WORKDIR /app

RUN pip3 install fastapi uvicorn cryptography pydantic pydantic-settings

COPY ./service.py .
COPY ./static /app/static

RUN ls -la /app

ENTRYPOINT [ "python3", "-m", "uvicorn", "service:app"]
CMD ["--host=0.0.0.0", "--port=8080"]
