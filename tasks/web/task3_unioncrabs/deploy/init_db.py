#!/usr/bin/env python

import sqlite3 as sql
from resident import HotelResident
import os 
import random

flag = r'CTF{EXAMPLEEXAMPLEEXAMPLEEXAMPLEEXAMPLEEXAMPLE}' if 'FLAG' not in os.environ else os.environ['FLAG'].replace('"','')
static_format = "/static/{}{}.jpg"

def destruct_db(cur:sql.Cursor):
    cur.execute("DROP TABLE IF EXISTS crabs")
    cur.execute("DROP TABLE IF EXISTS seagulls")


def init_db(cur:sql.Cursor):
    cur.execute("CREATE TABLE IF NOT EXISTS crabs(Name, Suit, AddInfo, ImageURL, is_worker)")
    cur.execute("CREATE TABLE IF NOT EXISTS seagulls(Name, Suit, AddInfo, ImageURL, is_worker)")


def insert_resident(cur: sql.Cursor, res: HotelResident):
    print((res.Name, res.suit_type, res.additional_data, res.image_url))
    if res.is_worker:
        cur.execute("INSERT INTO seagulls(Name, Suit, AddInfo, ImageURL, is_worker) VALUES(?,?,?,?,?)", (res.Name, res.suit_type, res.additional_data, res.image_url, res.is_worker))
        
    else:

        cur.execute("INSERT INTO crabs(Name, Suit, AddInfo, ImageURL, is_worker) VALUES(?,?,?,?,?)", (res.Name, res.suit_type, res.additional_data, res.image_url, res.is_worker))
        
    


def generate_resident(id:int, is_worker: bool, is_boss: bool) -> HotelResident:
    if is_boss:
        url = static_format.format("s", "10")
        suit = "Главный насест"
        add_i = "The Boss, key="+flag
    elif is_worker:
        url = static_format.format("s",id)
        suit = "Насесты для сотрудников"
        add_i = "Сотрудник отеля"
    else:
        url = static_format.format("c", id)
        suit = random.choice(["Стандартное гнездо", "Люкс скворечник", "Люкс насест"])
        add_i = random.choice(["Многодетный отец (мать?)",
                           "Панцирный модник",
                           "Гурман-Экспериментатор",
                           "Солдат на пенсии",
                           "Философ-отшельник",
                           "Краб-качок",
                           "Обожает рыбалку",
                           "Морской хипстер",
                           "Краб-гурман",
                           "Вечно недовольный",
                           "Сладкоежка",
                           "Ветеран морских приключений",
                           "Коллекционер ракушек",
                           "Философ-одиночка",
                           "Клешня-тиндер-свайпер",
                           "Краб, который не краб"])
    
    name = "{} {}".format(random.choice(["Maeve","Carley","Elle","Sandra","Ross","Trinity","Shane","Deangelo","Harley","Baron","Kira","Kaeden","Maritza","Camila","Blake","Janessa","Jorden","Cason","Jaidyn","Delaney","Aditya","Eden","Ulises","Raelynn","Bailey","Jazlynn","Leo","Lea","Lukas","Jocelynn"]), 
                          random.choice(["Márquez","Gil","Gallego","Pascual","Pérez","Vega","Romero","Moreno","Herrero","Moya","Mora","Ramírez","Ortega","Herrera","Marín","Crespo","Reyes","Castro","Muñoz","Rubio","López","Pastor","Ruiz","Serrano","Jiménez","Navarro","Ortiz","Rey","Ibáñez","Santos"]))
    
    return HotelResident(Name=name,suit_type=suit, additional_data=add_i, image_url=url, is_worker=is_worker)
        
def generate_db():
    con = sql.connect("residents.db")
    cur = con.cursor()
    destruct_db(cur)
    init_db(cur)
    ids = [i for i in range(1,9)]
    print("[+] Adding crabs")
    random.shuffle(ids)
    for i in ids:
        insert_resident(cur, generate_resident(i,False, False))
    print("[+] Adding seagulls")
    random.shuffle(ids)
    for i in ids:
        insert_resident(cur, generate_resident(i,True, False))
    print("[+] Adding boss with flag")
    insert_resident(cur, generate_resident(i,True, True))
    con.commit()
    print("[+] Done")
    
if __name__ == "__main__":
    generate_db()