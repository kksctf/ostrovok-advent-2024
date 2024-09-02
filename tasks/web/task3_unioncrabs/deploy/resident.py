import flet as ft
from pydantic import BaseModel, SkipValidation, Field
from typing import Tuple


class HotelResident(BaseModel): 
    is_worker: bool
    Name: str = Field(strict=False) 
    suit_type: str = Field(strict=False) 
    additional_data: str = Field(strict=False)
    image_url: str = Field(strict=False)
    
    def init_from_sql(self, sql_data: Tuple[str, str, str, str]):
        self.Name = sql_data[0]
        self.suit_type =  sql_data[1]
        self.additional_data =  sql_data[2]
        self.image_url =  sql_data[3]
        
    def render_flet_obj(self):
        controls = []
        image = ft.Container()
        
        image.margin = ft.margin.all(5)
        image.width = 100
        image.height = 100
        image.image_src = self.image_url
        image.border_radius = 300
        controls.append(ft.Column(controls=[image]))
        
        controls.append(
            ft.SelectionArea(content=ft.Column(
                [
                    ft.Row(
                        controls=[
                            ft.Text("ФИО:", weight=ft.FontWeight.BOLD, selectable=True),
                            ft.Text(self.Name),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("Номер:", weight=ft.FontWeight.BOLD, selectable=True),
                            ft.Text(self.suit_type),
                        ]
                    ),
                    
                    ft.Row(
                        controls=[
                            ft.Text("Доп. Инфо:", weight=ft.FontWeight.BOLD, selectable=True),
                            ft.Text(self.additional_data),
                        ]
                    ),
                ]
            )
            )
        )
        row = ft.Row(controls=controls)
        container = ft.Container(content=row)
        container.border = ft.border.symmetric(
            vertical=ft.border.BorderSide(1, "#ffaaaa")
        )
        container.border_radius = 5
        return container