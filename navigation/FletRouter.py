# FletRouter.py
import flet as ft
from pages import main, settings


class Router:
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes = {
            '/main_menu': main.main_menu,
            '/settings': settings.settings
        }
        self.current_route = None

    async def route_change(self, route):
        await self.remove_current_route()

        route_name = route.route
        if route_name in self.routes:
            if self.routes[route_name]:
                new_page = await self.routes[route_name](self.page)
                self.current_route = new_page
                await self.page.add_async(new_page)
            else:
                await self.page.add_async(ft.Text("Страница в разработке"))
        else:
            await self.page.add_async(ft.Text("404 - Страница не найдена"))

    async def remove_current_route(self):
        if self.current_route:
            # Вызываем метод очистки, если он существует
            if hasattr(self.current_route, 'cleanup') and callable(self.current_route.cleanup):
                await self.current_route.cleanup()
            await self.page.remove_async(self.current_route)
            self.current_route = None
