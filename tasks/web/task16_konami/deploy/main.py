import os

import uvicorn
from fastapi import FastAPI

app = FastAPI()

FLAG = os.environ.get("FLAG", "crab{default_flag}")
RANDOM_STRING_SEQ = os.environ.get("RANDOM_STRING_SEQ", "Y3JhYnJhdmVfZ3VsbHNsYXZl")


@app.get("/")
def root():
    return {"message": ""}


@app.get("/spa")
def spa():
    return {"message": "Ваша сауна с фирменным ароматическими маслом 'МорскаяТина' уже ждет вас на -1 этаже!"}


@app.get("/get_wifi")
def get_wifi():
    return {"message": "Пароль от wifi - 'chaiki_rulyat'"}


@app.get("/cleaning")
def clean_room():
    return {"message": "Ваш номер скоро будет убран, ждите чайку горничную"}


@app.get("/book_parking")
def book_parking():
    return {"message": "Предварительно забронировали вам ракушко-место на подземной ракушечной парковке"}


@app.get("/order_lobsters")
def order_lobsters():
    return {"message": "Спасибо за заказ!\nСвежие лобстеры скоро будут доставлены в ваш номер."}


@app.get(f"/{RANDOM_STRING_SEQ}", include_in_schema=False)
def secret():
    return {"message": f"jopa {FLAG}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7516)
