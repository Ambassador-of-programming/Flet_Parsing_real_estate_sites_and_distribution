import flet as ft


class Appbar:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.bottom_appbar = ft.BottomAppBar(
            bgcolor=ft.colors.TERTIARY_CONTAINER,
            content=ft.Row(
                controls=[
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.icons.HOME, icon_color=ft.colors.BLUE_200,
                                  on_click=lambda x: page.go("/main_menu")),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.icons.WORK_HISTORY, icon_color=ft.colors.BLUE_200,
                                  on_click=lambda x: page.go("/settings")),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.icons.QUERY_STATS, icon_color=ft.colors.BLUE_200,
                                  on_click=lambda x: page.go("/settings")),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.icons.SETTINGS, icon_color=ft.colors.BLUE_200,
                                  on_click=lambda x: page.go("/settings")),
                    ft.Container(expand=True),
                ]
            ),
            height=65,
        )

    async def content(self) -> ft.AppBar:
        return self.bottom_appbar
