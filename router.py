from flet_route import Routing, path  # Импорт классов для маршрутизации
import flet as ft  # Основной импорт библиотеки Flet для создания UI
from typing import List  # Для аннотации типов (списки маршрутов)

# Импорт страниц приложения
from src.pages.starting_page import StartingPage  # Главная страница
from src.pages.registration_page import RegistrationPage  # Страница регистрации
from src.pages.entrance_page import EntrancePage  # Страница входа
from src.pages.interface_page import InterfacePage


class Router:
    """
    Класс для управления маршрутизацией в приложении.
    Использует библиотеку flet_route для определения маршрутов и их обработчиков.
    """

    def __init__(self, page: ft.Page):
        """
        Инициализация маршрутизатора.

        Args:
            page (ft.Page): Экземпляр страницы Flet, на которой будет происходить маршрутизация.
        """
        self.page = page

        # Список маршрутов приложения.
        # Каждый маршрут определяется как объект `path` с URL, флагом очистки и обработчиком.
        self.app_routes: List[path] = [
            path(
                url="/",
                clear=True,
                view=lambda page, params, basket: StartingPage().view(
                    page, params, basket
                ),
            ),
            path(
                url="/registration",
                clear=True,
                view=lambda page, params, basket: RegistrationPage().view(
                    page, params, basket
                ),
            ),
            path(
                url="/entrance",
                clear=True,
                view=lambda page, params, basket: EntrancePage().view(
                    page, params, basket
                ),
            ),
            path(
                url="/interface",
                clear=True,
                view=lambda page, params, basket: InterfacePage().view(
                    page, params, basket
                ),
            ),
        ]

        # Инициализация маршрутизации с передачей страницы и списка маршрутов
        Routing(page=self.page, app_routes=self.app_routes)

        # Переход на текущий маршрут (или на начальный, если его нет)
        self.page.go(self.page.route)
