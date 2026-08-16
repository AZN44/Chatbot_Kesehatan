from ast import Await

import flet as ft
from flet.controls.material import tabs
from groq import Groq
import os
import time
import asyncio

from pydantic import SerializationInfo

API = Groq(api_key="API GROQ DISINI")


class AppC(ft.Column):
    def __init__(self, user_input):
        super().__init__()
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.MainAxisAlignment.START
        self.animate_alignment = ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT_QUINT)
        self.user_input = user_input
        self.expand = True 
        self.scroll = ft.ScrollMode.AUTO
        self.controls = []
        self.messages = [{"role": "system", "content": "Kamu adalah asisten yang membantu tentang kesehatan, dan jika ada yang tanya diluar itu maka jangan jawab."}]
        self.textawalan = ft.Text("Halo, ada yang bisa saya bantu?", size=30, color="black", text_align=ft.TextAlign.CENTER, animate_opacity=300)
        self.bubble = ft.Container(content=self.textawalan, border_radius=15, bgcolor="#D3D3D3", width=2000, height=120, alignment=ft.Alignment.CENTER, animate=ft.Animation(800, ft.AnimationCurve.EASE_OUT_BACK))
        
        self.controls = [self.bubble]

    async def kirim_click(self, e):
        if self.user_input.value:

            if hasattr(self, 'container_parent'):
                self.container_parent.alignment = ft.Alignment(0, -1)
                self.container_parent.update()

            self.alignment = ft.MainAxisAlignment.START
            self.bubble.width = 300
            self.bubble.height = 45
            self.bubble.content = ft.Text("Chatbot Seputar Kesehatan", size=16, color="black")
            self.bubble.content.size = 16
            self.bubble.bgcolor = "transparent"

            
            user_text = self.user_input.value
            self.messages.append({"role": "user", "content": user_text})
            self.controls.append(
                ft.Row(
                    controls=[
                        ft.Column([
                            ft.Text("Anda", size=10, color="black"),
                            ft.Container(
                                content=ft.Text(user_text, size=16, color="black"),
                                border_radius=15,  
                                padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                bgcolor="#D3D3D3"
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.END)
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            )
            panjang_input = len(self.user_input.value)
            loop_range = panjang_input // 2
            loop_range = int(panjang_input / 2)
            
            
            self.user_input.update()
            self.update()
            mengetik = ft.Text("Chatbot sedang mengetik.", size=10, color="gray", italic=True)
            

            for _ in range(loop_range):
                for titik in [".", "..", "..."]:
                    mengetik.value = f"Chatbot sedang mengetik{titik}"
                    self.controls.append(mengetik)
                    self.update()
                    await asyncio.sleep(0.1)
                    self.controls.remove(mengetik)
                    self.user_input.value = ""
                    self.user_input.update()
                    self.update()

            
            try:
                completion = API.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=self.messages
                )
                respon = completion.choices[0].message.content
                self.messages.append({"role": "assistant", "content": respon})
                
                self.controls.append(
                    ft.Row(
                        controls=[
                            ft.Column([
                                ft.Text("AI", size=10, color="black"),
                                ft.Container(
                                    content=ft.Text(respon, size=16, color="white"),
                                    border_radius=15,  
                                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                    bgcolor="blue",
                                    width=300 
                                ),
                            ], horizontal_alignment=ft.CrossAxisAlignment.START)
                        ],
                        alignment=ft.MainAxisAlignment.START
                    )
                )
            except Exception as ex:
                self.controls.append(ft.Text(f"Error: {ex}", color="red"))
            
            self.update()

def main(page: ft.Page):
    page.bgcolor = "#d9d0b6"
    page.title = "Chatbot Seputar Kesehatan"
    

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user_input = ft.TextField(
        hint_text="Ketik...", 
        expand=True, 
        border_radius=30,
        bgcolor="white"
    )

    chat_display = AppC(user_input)

    
    kirim_button = ft.ElevatedButton(
        "Kirim", 
        on_click=chat_display.kirim_click 
    )

    user_input.on_submit = chat_display.kirim_click

    main.container = ft.Container(content=chat_display, expand=True, bgcolor="transparent",alignment=ft.Alignment.CENTER, animate=ft.Animation(800, ft.AnimationCurve.EASE_OUT_BACK))

    chat_display.container_parent = main.container

    page.add(
        main.container,
        ft.Row([user_input, kirim_button])
    )

ft.app(target=main)
