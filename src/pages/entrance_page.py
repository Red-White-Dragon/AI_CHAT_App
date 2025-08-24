import os
import flet as ft
from flet_route import Params, Basket
from src.ui.app_style import AppStyles
from src.utils.app_tools import Validator, restore_basket
from src.utils.app_cache import AppCache


class EntrancePage:
    """
    Класс для отображения и обработки страницы входа пользователя.
    """

    def view(
        self,
        page: ft.Page,  # Объект текущей страницы
        params: Params,  # Параметры маршрута
        basket: Basket,  # Корзина для хранения данных между страницами
    ) -> ft.View:
        """
        Создаёт и возвращает представление страницы входа.

        Args:
            page: Объект страницы Flet.
            params: Параметры маршрута.
            basket: Корзина для хранения данных между страницами.

        Returns:
            ft.View: Представление страницы входа.
        """
        # Инициализация вспомогательных классов
        validator = Validator()  # Класс для валидации данных
        cache = AppCache()  # Класс для работы с кэшем приложения

        # Установка заголовка страницы
        page.title = "Форма входа"
        
        if page.platform.value in ["windows", "macos", "linux"]:
            # --- Обработчик изменения размера окна ---
            def on_resize(e):
                """
                Обновляет размеры элементов при изменении размера окна.
                """
                basket.width = page.window.width
                basket.height = page.window.height
                background.width = basket.get("width")
                background.height = basket.get("height")
                page_body.width = basket.get("width") * 0.8
                page_body.height = basket.get("height") * 0.8
                page.update()

            page.on_resized = on_resize

        # --- Обработчики событий ---
        def link_entrance(e: ft.ControlEvent) -> None:
            """
            Обработчик входа пользователя.
            Проверяет введённые данные и выполняет вход.
            """
            name = name_input.value
            family = family_input.value
            password = password_input.value

            # Валидация введённых данных
            entrance_error_text = validator.entrance_valid(name, family, password)

            if not entrance_error_text:
                # Получение API-ключа пользователя
                api_key = cache.get_user_api_key(name, family, password)
                if api_key:
                    basket.key = api_key
                    e.page.go("/interface")
                else:
                    # Ошибка: пользователь не найден
                    text_error.value = (
                        "Пользователь не найден. Используйте форму регистрации"
                    )
                    text_error.size = 18
                    text_error.update()
                    page_body_ref.current.scroll_to(
                        offset=0,
                        key=text_error.key,
                        duration=500,
                    )
            else:
                # Отображение ошибок валидации
                text_error.value = "\n".join(entrance_error_text)
                text_error.size = 18
                text_error.update()
                page_body_ref.current.scroll_to(
                    offset=0,
                    key=text_error.key,
                    duration=500,
                )

        def link_starting(e: ft.ControlEvent) -> None:
            """
            Переход на стартовую страницу с сохранением введённых данных.
            """
            basket.entrance_name = name_input.value
            basket.entrance_family = family_input.value
            basket.entrance_password = password_input.value
            e.page.go("/")

        def link_registration(e: ft.ControlEvent) -> None:
            """
            Переход на страницу регистрации с сохранением введённых данных.
            """
            basket.entrance_name = name_input.value
            basket.entrance_family = family_input.value
            basket.entrance_password = password_input.value
            e.page.go("/registration")

        # --- Элементы интерфейса ---
        # Заголовок страницы
        text_title = ft.Text(
            value="ВХОД",
            size=30,
            color=AppStyles.white_color,
            font_family="LumiosTypewriter",
            text_align=ft.TextAlign.CENTER,
            **AppStyles.text_fields_style,
        )

        # Текст для отображения ошибок
        text_error = ft.Text(
            size=0,
            color=AppStyles.light_salmon_color,
            font_family="LumiosTypewriter",
            text_align=ft.TextAlign.CENTER,
            **AppStyles.text_fields_style,
        )

        # Подсказка и поле ввода имени
        name_hint = ft.Text(
            value="Введите ваше имя:",
            size=20,
            color=AppStyles.white_color,
            font_family="Bahnschrift",
            text_align=ft.TextAlign.START,
            **AppStyles.text_fields_style,
        )
        name_input = ft.TextField(
            expand=True,
            **AppStyles.input_field_style,
        )

        # Подсказка и поле ввода фамилии
        family_hint = ft.Text(
            value="Введите вашу фамилию:",
            size=20,
            color=AppStyles.white_color,
            font_family="Bahnschrift",
            text_align=ft.TextAlign.START,
            **AppStyles.text_fields_style,
        )
        family_input = ft.TextField(
            expand=True,
            **AppStyles.input_field_style,
        )

        # Подсказка и поле ввода пароля
        password_hint = ft.Text(
            value="Введите пароль от аккаунта:",
            size=20,
            color=AppStyles.white_color,
            font_family="Bahnschrift",
            text_align=ft.TextAlign.START,
            **AppStyles.text_fields_style,
        )
        password_input = ft.TextField(
            can_reveal_password=True,
            password=True,
            expand=True,
            **AppStyles.input_field_style,
        )

        # Колонка для полей ввода
        column_fields = ft.Column(
            controls=[
                name_hint,
                name_input,
                family_hint,
                family_input,
                password_hint,
                password_input,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )

        # Кнопка входа
        entrance_button = ft.FilledButton(
            text="Войти",
            style=ft.ButtonStyle(**AppStyles.button_blue_style),
            on_click=lambda e: link_entrance(e),
            width=220,
        )

        # Кнопка возврата на стартовую страницу
        return_button = ft.FilledButton(
            text="Стартовая страница",
            style=ft.ButtonStyle(**AppStyles.button_white_style),
            on_click=lambda e: link_starting(e),
            width=220,
        )

        # Ссылка на форму регистрации
        about_registration = ft.Text(
            spans=[
                ft.TextSpan(
                    "Нет аккаунта? ",
                    style=ft.TextStyle(
                        color=AppStyles.white_color,
                        size=20,
                        font_family="Bahnschrift",
                    ),
                ),
                ft.TextSpan(
                    "Форма регистрации",
                    style=ft.TextStyle(
                        color=AppStyles.light_blue_color,
                        size=20,
                        font_family="Bahnschrift",
                    ),
                    on_click=lambda e: link_registration(e),
                ),
            ],
            **AppStyles.text_fields_style,
        )

        # --- Компоновка страницы ---
        page_body_ref = ft.Ref[ft.Column]()

        # Контейнер для основного контента
        page_body = ft.Container(
            content=ft.Column(
                [
                    text_title,
                    text_error,
                    column_fields,
                    entrance_button,
                    return_button,
                    about_registration,
                ],
                ref=page_body_ref,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                spacing=20,
                expand=True,
            ),
            width=page.width * 0.8,
            height=page.height * 0.8,
            **AppStyles.page_body_style,
        )

        # Фоновое изображение
        background = ft.Image(
            src=os.path.join("images", "Matrix_blue.png"),
            fit=ft.ImageFit.FILL,
            width=page.width,
            height=page.height,
        )

        # Стек для наложения фона и контента
        stack = ft.Stack(
            controls=[
                background,
                page_body,
            ],
            alignment=ft.alignment.center,
            expand=True,
        )

        # --- Восстановление введённых данных при переходе между страницами ---
        restore_basket(basket, "entrance_name", name_input)
        restore_basket(basket, "entrance_family", family_input)
        restore_basket(basket, "entrance_password", password_input)

        # --- Возврат представления ---
        return ft.View(
            "/entrance",
            controls=[stack],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            padding=0,
        )
