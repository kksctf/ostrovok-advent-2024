import flet as ft
import flet.fastapi as flet_fastapi

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request

from pydantic import BaseModel

import sqlite3 as sql
from typing import Tuple

import init_db
from resident import HotelResident

app = flet_fastapi.FastAPI()


### Web API
@app.get("/")
async def index():
    return RedirectResponse("/app")


@app.get("/app/favicon.png")
@app.get("/app/icons/loading-animation.png")
def get_favicon(req: Request) -> RedirectResponse:
    return RedirectResponse(url=req.url_for("static", path="favicon.ico"))


@app.get("/app/static/{res}")
def get_static_file(res: str, req: Request):
    return RedirectResponse(url=req.url_for("static", path=res))


### FLET APPLICATION


def get_object() -> HotelResident:
    ex = HotelResident(
        is_worker=False,
        Name="Aboba",
        suit_type="Standart",
        additional_data="Test User",
        image_url="https://upload.wikimedia.org/wikipedia/en/thumb/f/f8/Mr._Krabs.svg/220px-Mr._Krabs.svg.png",
    )
    return ex


async def flet_app(page: ft.Page):
    page.title = "Chayka Systems"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.fonts = {
        "PT": "/static/pt-root-ui_light.ttf",
        "Spoof": "/static/Spoof-Regular.ttf",
    }
    page.theme = page.dark_theme = ft.Theme(color_scheme_seed="white", font_family="PT")
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    top_container = ft.Container()
    top_container.height = 150
    top_container.border = ft.border.symmetric(
        vertical=ft.border.BorderSide(1, "#8EB3EB")
    )
    text_field = ft.TextField(
        hint_text="Фамилия клиента...",
        width=750,
        border_color="#8EB3EB",
        bgcolor="white",
    )
    tbox = ft.Text("")
    
    def search_on_change(e):
        residents=[]
        main_rows.controls = []
        try:   
            con = sql.connect("residents.db")
            cur = con.cursor()
            for row in cur.execute(
                "SELECT Name, Suit, AddInfo, ImageURL, is_worker FROM crabs WHERE Name LIKE '%"+text_field.value+"%'"
            ):
                residents.append(
                    HotelResident(
                        Name=row[0],
                        suit_type=row[1],
                        additional_data=row[2],
                        image_url=row[3],
                        is_worker=row[4],
                    )
                )
            if len(residents) > 0:
                print(residents[0])
            con.close()
            
            for resid in residents:
                main_rows.controls.append(resid.render_flet_obj())
        except Exception as e:
            main_rows.controls.append(ft.Text(value=str(e), size=16, color="red"))
            
        page.update()

    text_field.on_change = search_on_change # fix of search button
    top_container.content = ft.Column(
        [
            ft.Text(
                "ChaykaHotels! :: Клиенты",
                color="#0D41D2",
                size=35,
                font_family="Spoof",
            ),
            text_field,
            #ft.ElevatedButton(text="Поиск", on_click=search_on_change),
            tbox
        ],
        alignment=ft.alignment.center,
    )
    await page.add_async(top_container)
    await page.add_async(ft.Row(height=15))

    main_rows = ft.Column()
    main_rows.width = 700

    # TODO: Change to select where=* and add on_click methond on button with TextField
    # TODO: короче добавить вулну

    # for row in cur.execute(
    #     "SELECT Name, Suit, AddInfo, ImageURL, is_worker FROM seagulls"
    # ):
    #     ft_obj = HotelResident(
    #         Name=row[0],
    #         suit_type=row[1],
    #         additional_data=row[2],
    #         image_url=row[3],
    #         is_worker=row[4],
    #     )
    #     main_rows.controls.append(ft_obj.render_flet_obj())
    search_on_change(None)
    await page.add_async(main_rows)
    await page.update_async()


init_db.generate_db()
app.mount("/app", flet_fastapi.app(flet_app))
app.mount("/static", StaticFiles(directory="static"), name="static")

# uvicorn main:app --reload --port 1337
