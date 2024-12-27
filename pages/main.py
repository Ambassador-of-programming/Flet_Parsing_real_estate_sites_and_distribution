from parsing.cian import Cian
from parsing.smartagent import get_phones_with_scroll, login
import flet as ft
import os
import signal
import multiprocessing


def run_pagination(link, watsapp_tokens, proxy, times, text_message, pid):
    cian = Cian(link=link, watsapp_tokens=watsapp_tokens,
                proxy=proxy, times=times, text_message=text_message)
    cian.start_multiprocessing(pid=pid)


async def main_menu(page: ft.Page):
    class Smartagent:
        def __init__(self, page: ft.Page):
            self.page = page

            self.limit = ft.TextField(
                label="Добавить limit",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=150
            )
            self.text_message = ft.TextField(
                label="Добавить текст",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=150
            )

            self.url = ft.TextField(
                label="Добавить url",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=True,
                width=150
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

            self.pick_files_dialog = ft.FilePicker(
                on_result=self.pick_files_result)
            self.page.overlay.append(self.pick_files_dialog)
            self.add_text_button = ft.ElevatedButton(
                "Прикрепить txt сообщения",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                ),
                on_click=self.open_file_picker,
                icon=ft.icons.FILE_DOWNLOAD,
                visible=True
            )
            self.login_button = ft.ElevatedButton(
                "Login",
                width=250,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=30),
                    elevation=5,
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                    animation_duration=300,
                ),
                # disabled=True,
                on_click=self.login_clicked,
                visible=True
            )

            self.start_button = ft.ElevatedButton(
                "Старт",
                width=250,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=30),
                    elevation=5,
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                    animation_duration=300,
                ),
                # disabled=True,
                on_click=self.start_clicked,
                visible=True
            )
            self.divider_3 = ft.Divider(
                height=1, color="#CCCCCC", visible=True)
            self.divider_4 = ft.Divider(
                height=1, color="#CCCCCC", visible=True)
            self.divider_5 = ft.Divider(
                height=1, color="#CCCCCC", visible=True)
            self.divider_6 = ft.Divider(
                height=1, color="#CCCCCC", visible=True)

            self.platform_menu = ft.ExpansionPanelList(
                controls=[
                    ft.ExpansionPanel(
                        expanded=False,
                        header=ft.Container(
                            content=ft.Text("Smartagent"),
                            alignment=ft.alignment.center
                        ),
                        content=ft.Container(
                            content=ft.Column([
                                self.login_button,

                                self.url,
                                self.limit,

                                self.instance_id,
                                self.access_token,
                                self.divider_5,

                                self.text_message,
                                self.divider_6,
                                self.start_button,
                            ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=10
                        )
                    )
                ]
            )

        def pick_files_result(self, e: ft.FilePickerResultEvent):
            if e.files:
                self.selected_file_path = e.files[0].path
            else:
                self.selected_file_path = None

        async def open_file_picker(self, e):
            await self.pick_files_dialog.pick_files_async(allow_multiple=False)

        async def login_clicked(self, event):
            self.login_button = login()

        async def start_clicked(self, e):
            print(type(self.login_button))
            print(self.login_button)
            main_pid = multiprocessing.Process(
                target=get_phones_with_scroll,
                args=(self.url.value, self.login_button, self.text_message.value, self.instance_id.value, self.access_token.value, self.limit.value))

            main_pid.start()

    class PhoneSendWhatsApp:
        def __init__(self, page: ft.Page):
            self.page = page

            self.proxy = ['HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5']
            self.proxy_ip = ft.TextField(
                label="Добавить IP",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=150
            )
            self.proxy_port = ft.TextField(
                label="Добавить PORT",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=150
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
                visible=False
            )

            self.time = ['0', "1", "2", "3", "4", "5", "6", "7", "8", "9",
                         "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                         "20", "21", "22", "23"
                         ]
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
                visible=False
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
                visible=False
            )

            self.instance_id = ft.TextField(
                label="Добавить instance_id",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=150
            )
            self.access_token = ft.TextField(
                label="Добавить access_token",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=150
            )

            self.pick_files_dialog = ft.FilePicker(
                on_result=self.pick_files_result)
            self.page.overlay.append(self.pick_files_dialog)
            self.add_text_button = ft.ElevatedButton(
                "Прикрепить Excel номера",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                ),
                on_click=self.open_file_picker,
                icon=ft.icons.FILE_DOWNLOAD,
                visible=False
            )

            self.start_button = ft.ElevatedButton(
                "Старт",
                width=250,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=30),
                    elevation=5,
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                    animation_duration=300,
                ),
                disabled=True,
                on_click=self.start_clicked,
                visible=False
            )
            self.divider_3 = ft.Divider(
                height=1, color="#CCCCCC", visible=False)
            self.divider_4 = ft.Divider(
                height=1, color="#CCCCCC", visible=False)
            self.divider_5 = ft.Divider(
                height=1, color="#CCCCCC", visible=False)
            self.divider_6 = ft.Divider(
                height=1, color="#CCCCCC", visible=False)

            self.platform_menu = ft.ExpansionPanelList(
                controls=[
                    ft.ExpansionPanel(
                        expanded=False,
                        header=ft.Container(
                            content=ft.Text("Рассылка с Excel базы"),
                            alignment=ft.alignment.center
                        ),
                        content=ft.Container(
                            content=ft.Column([
                                self.proxy_dropdown,
                                self.proxy_ip,
                                self.proxy_port,
                                self.divider_3,

                                self.time_start,
                                self.time_end,
                                self.divider_4,

                                self.instance_id,
                                self.access_token,
                                self.divider_5,

                                self.add_text_button,
                                self.divider_6,
                                self.start_button,
                            ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=10
                        )
                    )
                ]
            )

        def pick_files_result(self, e: ft.FilePickerResultEvent):
            if e.files:
                self.selected_file_path = e.files[0].path
            else:
                self.selected_file_path = None

        async def open_file_picker(self, e):
            await self.pick_files_dialog.pick_files_async(allow_multiple=False)

        async def start_clicked(self, e):
            if self.start_button.text == "Старт":
                cian_platform = await page.client_storage.get_async("cian")
                watsapp = await page.client_storage.get_async("watsapp")
                proxy = await page.client_storage.get_async("proxy")
                time = await page.client_storage.get_async("time")
                text_message = await page.client_storage.get_async("text_message")
                if all([cian_platform, watsapp, time, text_message]):
                    self.start_button.style.bgcolor = {"": "#FF5252"}
                    self.start_button.text = "Стоп"

                    main_pid = multiprocessing.Process(
                        target=run_pagination,
                        args=(cian_platform, watsapp,
                              proxy, time, text_message)
                    )

                    main_pid.start()

                    page.session.set('main_pid', main_pid.pid)

        async def dropdown_changed(self, e):
            self.divider_3.visible = True
            self.divider_4.visible = True
            self.divider_5.visible = True
            self.divider_6.visible = True

            self.proxy_dropdown.visible = True
            self.proxy_ip.visible = True
            self.proxy_port.visible = True

            self.time_start.visible = True
            self.time_end.visible = True

            self.instance_id.visible = True
            self.access_token.visible = True

            self.add_text_button.visible = True

            self.start_button.visible = True
            await page.update_async()

    class ParsingMenu:
        def __init__(self, page: ft.Page):
            self.page = page
            self.platforms = ["Циан", "Авито", "Юла", "Яндекс.Недвижимость"]

            self.dropdown = ft.Dropdown(
                width=250,
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
                on_change=self.dropdown_changed
            )

            self.url_input_platform = ft.TextField(
                label="Добавить ссылку на объект",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=250
            )

            self.proxy = ['HTTP', 'HTTPS', 'SOCKS4', 'SOCKS5']
            self.proxy_ip = ft.TextField(
                label="Добавить IP",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=150
            )
            self.proxy_port = ft.TextField(
                label="Добавить PORT",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=150
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
                visible=False
            )

            self.time = ['0', "1", "2", "3", "4", "5", "6", "7", "8", "9",
                         "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                         "20", "21", "22", "23"
                         ]
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
                visible=False
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
                visible=False
            )

            self.instance_id = ft.TextField(
                label="Добавить instance_id",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=150
            )
            self.access_token = ft.TextField(
                label="Добавить access_token",
                border_color="#1E3A8A",
                color="#1E3A8A",
                bgcolor="white",
                visible=False,
                width=150
            )

            self.pick_files_dialog = ft.FilePicker(
                on_result=self.pick_files_result)
            self.page.overlay.append(self.pick_files_dialog)
            self.add_text_button = ft.ElevatedButton(
                "Прикрепить текст сообщения",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                ),
                on_click=self.open_file_picker,
                icon=ft.icons.FILE_DOWNLOAD,
                visible=False
            )

            self.start_button = ft.ElevatedButton(
                "Старт",
                width=250,
                height=60,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=30),
                    elevation=5,
                    color={"": "white"},
                    bgcolor={"": "#4CAF50"},
                    animation_duration=300,
                ),
                disabled=True,
                on_click=self.start_clicked,
                visible=False
            )
            self.divider_1 = ft.Divider(
                height=1, color="#CCCCCC", visible=False)
            self.divider_2 = ft.Divider(
                height=1, color="#CCCCCC", visible=False)
            self.divider_3 = ft.Divider(
                height=1, color="#CCCCCC", visible=False)
            self.divider_4 = ft.Divider(
                height=1, color="#CCCCCC", visible=False)
            self.divider_5 = ft.Divider(
                height=1, color="#CCCCCC", visible=False)
            self.divider_6 = ft.Divider(
                height=1, color="#CCCCCC", visible=False)

            self.platform_menu = ft.ExpansionPanelList(
                controls=[
                    ft.ExpansionPanel(
                        expanded=False,
                        header=ft.Container(
                            content=ft.Text("Настройки парсинга"),
                            alignment=ft.alignment.center
                        ),
                        content=ft.Container(
                            content=ft.Column([
                                self.dropdown,
                                self.divider_1,

                                self.url_input_platform,
                                self.divider_2,

                                self.proxy_dropdown,
                                self.proxy_ip,
                                self.proxy_port,
                                self.divider_3,

                                self.time_start,
                                self.time_end,
                                self.divider_4,

                                self.instance_id,
                                self.access_token,
                                self.divider_5,

                                self.add_text_button,
                                self.divider_6,
                                self.start_button,
                            ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            padding=10
                        )
                    )
                ]
            )

            self.title = ft.Text("Риэлторское агентство", size=32, weight=ft.FontWeight.BOLD,
                                 color="#1E3A8A", text_align=ft.TextAlign.CENTER)
            self.subtitle = ft.Text("Ваш надежный партнер в мире недвижимости",
                                    size=16, color="#64748B", italic=True, text_align=ft.TextAlign.CENTER)
            self.logo = ft.Icon(ft.icons.HOME_WORK, size=100, color="#1E3A8A")

            self.pid = multiprocessing.Queue()
            self.selected_file_path = None

        def pick_files_result(self, e: ft.FilePickerResultEvent):
            if e.files:
                self.selected_file_path = e.files[0].path
            else:
                self.selected_file_path = None

        async def open_file_picker(self, e):
            await self.pick_files_dialog.pick_files_async(allow_multiple=False)

        async def start_clicked(self, e):
            if self.start_button.text == "Старт":
                if self.dropdown.value == 'Циан':
                    cian_platform = await page.client_storage.get_async("cian")
                    watsapp = await page.client_storage.get_async("watsapp")
                    proxy = await page.client_storage.get_async("proxy")
                    time = await page.client_storage.get_async("time")
                    text_message = await page.client_storage.get_async("text_message")
                    if all([cian_platform, watsapp, time, text_message]):
                        self.start_button.style.bgcolor = {"": "#FF5252"}
                        self.start_button.text = "Стоп"

                        main_pid = multiprocessing.Process(
                            target=run_pagination,
                            args=(cian_platform, watsapp, proxy,
                                  time, text_message, self.pid)
                        )

                        main_pid.start()

                        page.session.set('main_pid', main_pid.pid)

            else:
                pid = self.pid.get(block=False)
                if pid:
                    for pids in pid:
                        try:
                            os.kill(pids, signal.SIGTERM)
                        except ProcessLookupError:
                            print(f"Process with PID {pids} not found")
                    pid.clear()

                main_pid = page.session.get('main_pid')
                if main_pid:
                    try:
                        os.kill(main_pid, signal.SIGTERM)
                    except ProcessLookupError:
                        print(f"Process with PID {main_pid} not found")

                self.start_button.style.bgcolor = {"": "#4CAF50"}
                self.start_button.text = "Старт"
            await self.start_button.update_async()

        async def dropdown_changed(self, e):
            self.divider_1.visible = True
            self.divider_2.visible = True
            self.divider_3.visible = True
            self.divider_4.visible = True
            self.divider_5.visible = True
            self.divider_6.visible = True

            self.dropdown.visible = True
            self.url_input_platform.visible = True

            self.proxy_dropdown.visible = True
            self.proxy_ip.visible = True
            self.proxy_port.visible = True

            self.time_start.visible = True
            self.time_end.visible = True

            self.instance_id.visible = True
            self.access_token.visible = True

            self.add_text_button.visible = True

            self.start_button.visible = True
            self.start_button.disabled = not self.dropdown.value

            await page.update_async()

    parsing_instance = ParsingMenu(page)
    phone_instance = PhoneSendWhatsApp(page)
    smartagent_instance = Smartagent(page)
    return ft.Container(
        content=ft.Container(
            content=ft.Column(
                [
                    parsing_instance.logo,
                    parsing_instance.title,
                    parsing_instance.subtitle,
                    ft.Container(height=20),
                    parsing_instance.platform_menu,
                    phone_instance.platform_menu,
                    smartagent_instance.platform_menu
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=300,  # Ограничиваем ширину содержимого
            alignment=ft.alignment.center
        ),
        expand=True,
        alignment=ft.alignment.center,  # Центрируем внутренний контейнер
        padding=40,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=["#F0F4F8", "#E2E8F0"]
        )
    )
