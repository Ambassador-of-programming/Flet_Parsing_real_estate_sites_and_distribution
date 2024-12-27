import flet as ft


async def settings(page: ft.Page):

    class Settings:
        def __init__(self, page: ft.Page):
            self.page = page
            self.links = {}
            self.platforms = ["Циан", "Авито", "Юла", "Яндекс.Недвижимость"]
            self.time = ['0', "1", "2", "3", "4", "5", "6", "7", "8", "9",
                         "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                         "20", "21", "22", "23"
                         ]
            self.proxy = ['HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5']
            self.selected_file_path = None

            self.title = ft.Text("Настройки", size=32, weight=ft.FontWeight.BOLD,
                                 color="#1E3A8A", text_align=ft.TextAlign.CENTER)
            self.platform_dropdown = ft.Dropdown(
                width=150,
                options=[ft.dropdown.Option(platform)
                         for platform in self.platforms],
                label="Выберите платформу",
                hint_text="Платформа",
                border_color="#1E3A8A",
                color="white",
                bgcolor="#1E3A8A",
                focused_bgcolor="#2A4A9A",
                focused_color="white",
                text_style=ft.TextStyle(color="white"),
            )
            self.url_input_platform = ft.TextField(
                label="Добавить ссылку на объект",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=250
            )
            self.add_button_platform = ft.ElevatedButton(
                "Сохранить",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                ),
                visible=True,
                on_click=self.add_link_clicked
            )

            self.time_start = ft.Dropdown(
                width=150,
                options=[ft.dropdown.Option(time) for time in self.time],
                label="Выберите начало",
                border_color="#1E3A8A",
                color="white",
                bgcolor="#1E3A8A",
                focused_bgcolor="#2A4A9A",
                focused_color="white",
                text_style=ft.TextStyle(color="white"),
            )
            self.time_end = ft.Dropdown(
                width=150,
                options=[ft.dropdown.Option(time) for time in self.time],
                label="Выберите конец",
                border_color="#1E3A8A",
                color="white",
                bgcolor="#1E3A8A",
                focused_bgcolor="#2A4A9A",
                focused_color="white",
                text_style=ft.TextStyle(color="white"),
            )
            self.add_button_time = ft.ElevatedButton(
                "Сохранить",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                ),
                visible=True,
                on_click=self.add_time
            )

            self.proxy_dropdown = ft.Dropdown(
                width=150,
                options=[ft.dropdown.Option(platform)
                         for platform in self.proxy],
                label="Выберите тип",
                border_color="#1E3A8A",
                color="white",
                bgcolor="#1E3A8A",
                focused_bgcolor="#2A4A9A",
                focused_color="white",
                text_style=ft.TextStyle(color="white"),
            )
            self.proxy_ip = ft.TextField(
                label="Добавить IP",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=150
            )
            self.proxy_port = ft.TextField(
                label="Добавить PORT",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=150
            )
            self.add_button_proxy = ft.ElevatedButton(
                "Сохранить",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                ),
                visible=True,
                on_click=self.proxy_event
            )

            self.instance_id = ft.TextField(
                label="Добавить instance_id",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=150
            )
            self.access_token = ft.TextField(
                label="Добавить access_token",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=150
            )
            self.add_button_watsapp = ft.ElevatedButton(
                "Сохранить",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                ),
                visible=True,
                on_click=self.watsapp_event
            )

            self.clear_all_client_storage = ft.ElevatedButton(
                "Очистить всё",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                ),
                visible=True,
                on_click=self.client_storage_event
            )

            self.pick_files_dialog = ft.FilePicker(
                on_result=self.pick_files_result)
            self.page.overlay.append(self.pick_files_dialog)

            self.add_text_button = ft.ElevatedButton(
                "Добавить текст сообщения",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                ),
                on_click=self.open_file_picker,
                icon=ft.icons.FILE_DOWNLOAD
            )
            self.result_text = ft.Text(
                "", color="#1E3A8A", size=16, text_align=ft.TextAlign.CENTER)

        async def add_time(self, e):
            if all([self.time_start.value, self.time_end.value]):
                await page.client_storage.set_async('time',
                                                    {'start': self.time_start.value,
                                                     'end': self.time_end.value}
                                                    )

        async def client_storage_event(self, event):
            await page.client_storage.clear_async()

        async def watsapp_event(self, event):
            if all([self.instance_id.value, self.access_token.value]):
                await page.client_storage.set_async('watsapp',
                                                    {'instance_id': self.instance_id.value,
                                                     'access_token': self.access_token.value,
                                                     }
                                                    )

        async def proxy_event(self, event):
            if all([self.proxy_dropdown.value, self.proxy_ip.value, self.proxy_port.value]):
                await page.client_storage.set_async('proxy',
                                                    {'type': self.proxy_dropdown.value,
                                                     'ip': self.proxy_ip.value,
                                                     'port': self.proxy_port.value,
                                                     }
                                                    )

        async def add_link_clicked(self, e):
            if all([self.url_input_platform.value, self.platform_dropdown.value]):
                if self.platform_dropdown.value == 'Циан':
                    await page.client_storage.set_async('cian', self.url_input_platform.value)

        def pick_files_result(self, e: ft.FilePickerResultEvent):
            if e.files:
                self.selected_file_path = e.files[0].path
                page.client_storage.set('text_message', e.files[0].path)
            else:
                self.selected_file_path = None

        async def open_file_picker(self, e):
            await self.pick_files_dialog.pick_files_async(allow_multiple=False)

    settings_instance = Settings(page)

    return ft.Container(
        content=ft.Container(
            content=ft.Column(
                [
                    settings_instance.title,
                    ft.Container(height=20),
                    ft.Text("Управление ссылками на объекты", size=18,
                            color="#64748B", italic=True, text_align=ft.TextAlign.CENTER),
                    ft.Row([
                        settings_instance.platform_dropdown,
                        settings_instance.url_input_platform,
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    settings_instance.add_button_platform,
                    ft.Divider(height=1, color="#CCCCCC"),

                    ft.Text("Управление Прокси", size=18, color="#64748B",
                            italic=True, text_align=ft.TextAlign.CENTER),
                    ft.Row([
                        settings_instance.proxy_dropdown,
                        settings_instance.proxy_ip,
                        settings_instance.proxy_port,
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    settings_instance.add_button_proxy,
                    ft.Divider(height=1, color="#CCCCCC"),

                    ft.Text("Управление WhatsApp подключением", size=18,
                            color="#64748B", italic=True, text_align=ft.TextAlign.CENTER),
                    ft.Row([
                        settings_instance.instance_id,
                        settings_instance.access_token,
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    settings_instance.add_button_watsapp,
                    ft.Divider(height=1, color="#CCCCCC"),

                    ft.Text("Управление временем начала и конца", size=18,
                            color="#64748B", italic=True, text_align=ft.TextAlign.CENTER),
                    ft.Row([
                        settings_instance.time_start,
                        settings_instance.time_end,
                    ], alignment=ft.MainAxisAlignment.CENTER),

                    settings_instance.add_button_time,
                    ft.Divider(height=1, color="#CCCCCC"),

                    ft.Text("Управление текстом сообщения", size=18,
                            color="#64748B", italic=True, text_align=ft.TextAlign.CENTER),
                    settings_instance.add_text_button,
                    ft.Divider(height=1, color="#CCCCCC"),

                    ft.Text("Управление Клиентским хранилищем", size=18,
                            color="#64748B", italic=True, text_align=ft.TextAlign.CENTER),
                    settings_instance.clear_all_client_storage,
                    ft.Divider(height=1, color="#CCCCCC"),

                    ft.Container(height=20),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            padding=20,
            expand=True,
            alignment=ft.alignment.center,
        ),
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#F0F4F8", "#E2E8F0"]
        )
    )
