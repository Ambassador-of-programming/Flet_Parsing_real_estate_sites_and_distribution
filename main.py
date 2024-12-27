import flet as ft
from navigation.FletRouter import Router
from navigation.bar import Appbar


async def main(page: ft.Page):
    page.title = 'Flet_Parsing_real_estate_sites_and_distribution'
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = 'HIDDEN'
    page.padding = 0
    page.platform = ft.PagePlatform.WINDOWS
    page.window.width = 640
    page.window.height = 640
    page.bgcolor = "#F0F4F8"

    page.adaptive = True

    router = Router(page)
    page.on_route_change = router.route_change

    appbar = Appbar(page)
    page.appbar = await appbar.content()

    page.go('/main_menu')

if __name__ == "__main__":
    ft.app(target=main)