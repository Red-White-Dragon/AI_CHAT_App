import flet as ft  # Импорт библиотеки Flet для GUI

from router import Router  # Импорт класса Router из локального модуля
import src.api
import src.pages
import src.ui
import src.utils
from src.ui.app_style import AppStyles

async def main(page: ft.Page):
    """
    Основная асинхронная функция для инициализации приложения Flet.

    Args:
        page (ft.Page): Объект страницы Flet.
    """
    try:
        Router(page)  # Инициализация маршрутизатора
    except Exception as e:
        print(f"Ошибка инициализации: {e}")  # Логирование ошибок


if __name__ == "__main__":
    ft.app(
        target=main, assets_dir="assets"
    )  # Запуск приложения с указанием директории ресурсов
