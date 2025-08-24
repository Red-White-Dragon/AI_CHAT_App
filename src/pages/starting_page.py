import os
import flet as ft
from flet_route import Params, Basket
from src.ui.app_style import AppStyles


class StartingPage:
    """Класс для отображения и обработки стартовой страницы приложения."""

    def view(
        self,
        page: ft.Page,  # Объект текущей страницы
        params: Params,  # Параметры маршрута
        basket: Basket,  # Корзина для хранения данных между страницами
    ) -> ft.View:
        """
        Создаёт и возвращает представление стартовой страницы.

        Args:
            page: Объект страницы Flet.
            params: Параметры маршрута.
            basket: Корзина для хранения данных между страницами.

        Returns:
            ft.View: Представление стартовой страницы.
        """
        
        # Установка заголовка страницы
        page.title = "Стартовая страница"
        # Загрузка стилей шрифтов
        page.fonts = AppStyles.fonts_styles

        # Настройка параметров окна в зависимости от платформы
        if page.platform.value in ["windows", "macos", "linux"]:
            
            page.window.icon = os.path.join("images", "Matrix_blue.ico")
            page.window.width = (
                basket.get("width") if basket.get("width") else AppStyles.page_width
            )
            page.window.height = (
                basket.get("height") if basket.get("height") else AppStyles.page_height
            )
            page.window.full_screen = False
            page.window.resizable = True
            page.window.maximizable = True
            
            # --- Обработчик изменения размера окна ---
            def on_resize(e):
                """
                Обновляет размеры элементов при изменении размера окна.
                Сохраняет текущие размеры в корзину (basket).
                """
                basket.width = page.window.width
                basket.height = page.window.height
                background.width = basket.get("width")
                background.height = basket.get("height")
                page_body.width = basket.get("width") * 0.6
                page_body.height = basket.get("height") * 0.7
                page.update()

            page.on_resized = on_resize

        # --- Обработчики событий ---
        def link_registration(e: ft.ControlEvent) -> None:
            """Обработчик нажатия на кнопку 'Регистрация'. Переход на страницу регистрации."""
            e.page.go("/registration")

        def link_entrance(e: ft.ControlEvent) -> None:
            """Обработчик нажатия на кнопку 'Вход'. Переход на страницу входа."""
            e.page.go("/entrance")

        # --- Элементы интерфейса ---
        ## Заголовок страницы
        text_title = ft.Text(
            value="AI CHAT",
            size=30,
            color=AppStyles.light_blue_color,
            font_family="Trafaret",
            text_align=ft.TextAlign.CENTER,
            **AppStyles.text_fields_style,
        )

        ## Аннотация (описание приложения)
        text_annotation = ft.Text(
            value="Приложение для доступа к нейросетям от OpenAI",
            size=25,
            color=ft.Colors.WHITE,
            font_family="LumiosTypewriter",
            text_align=ft.TextAlign.CENTER,
            **AppStyles.text_fields_style,
        )

        ## Колонка для заголовка и аннотации
        column_texts = ft.Column(
            controls=[text_title, text_annotation],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        )

        ## Кнопка регистрации
        registration_button = ft.FilledButton(
            text="Регистрация",
            style=ft.ButtonStyle(**AppStyles.button_white_style),
            on_click=lambda e: link_registration(e),
            width=220,
        )

        ## Кнопка входа
        entrance_button = ft.FilledButton(
            text="Вход",
            style=ft.ButtonStyle(**AppStyles.button_blue_style),
            on_click=lambda e: link_entrance(e),
            width=220,
        )

        ## Колонка для кнопок
        column_buttons = ft.Column(
            controls=[registration_button, entrance_button],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        ## Основная колонка с контентом
        column_content = ft.Column(
            controls=[column_texts, column_buttons],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            expand=True,
        )

        # --- Компоновка страницы ---
        ## Контейнер для основного контента
        page_body = ft.Container(
            content=column_content,
            width=page.width * 0.6,
            height=page.height * 0.7,
            **AppStyles.page_body_style,
        )

        ## Фоновое изображение
        background = ft.Image(
            src=os.path.join("images", "Matrix_blue.png"),
            fit=ft.ImageFit.FILL,
            width=page.width,
            height=page.height,
        )

        ## Стек для наложения фона и контента
        stack = ft.Stack(
            controls=[
                background,
                page_body,
            ],
            alignment=ft.alignment.center,
            expand=True,
        )

        # --- Возврат представления ---
        return ft.View(
            route="/",
            controls=[stack],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            padding=0,
        )
