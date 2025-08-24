import flet as ft
from src.ui.app_style import AppStyles


class ModelSelector(ft.Dropdown):
    
    def __init__(self, models: list):
        # Инициализация родительского класса Dropdown
        super().__init__()

        # Применение стилей из конфигурации к компоненту
        for key, value in AppStyles.model_dropdown.items():
            setattr(self, key, value)

        # Настройка внешнего вида выпадающего списка
        self.label = None  # Убираем текстовую метку
        self.hint_text = "Выбор модели"  # Текст-подсказка

        # Создание списка опций из предоставленных моделей
        self.options = [
            ft.dropdown.Option(
                key=model["id"],  # ID модели как ключ
                text=model["name"],  # Название модели как отображаемый текст
            )
            for model in models
        ]

        # Сохранение полного списка опций для фильтрации
        self.all_options = self.options.copy()

        # Установка начального значения (первая модель из списка)
        self.value = models[0]["id"] if models else None

        # Создание поля поиска для фильтрации моделей
        self.search_field = ft.TextField(
            on_change=self.filter_options,  # Функция обработки изменений
            hint_text="Поиск модели",  # Текст-подсказка в поле поиска
            **AppStyles.model_search_field  # Применение стилей из конфигурации
        )
        
        self.text = ft.Text(
            value="Введите название модели. Откройте список и выберите модель. Затем пролистайте вниз, до поля отправки сообщения.",
            size=18,
            color=AppStyles.white_color,
            font_family="LumiosTypewriter",
            text_align=ft.TextAlign.CENTER,
            width=400,
            **AppStyles.text_fields_style,
        )

    def filter_options(self, e):
        """
        Фильтрация списка моделей на основе введенного текста поиска.

        Args:
            e: Событие изменения текста в поле поиска
        """
        # Получение текста поиска в нижнем регистре
        search_text = self.search_field.value.lower() if self.search_field.value else ""

        # Если поле поиска пустое - показываем все модели
        if not search_text:
            self.options = self.all_options
        else:
            # Фильтрация моделей по тексту поиска
            # Ищем совпадения в названии или ID модели
            self.options = [
                opt
                for opt in self.all_options
                if search_text in opt.text.lower() or search_text in opt.key.lower()
            ]
        # Обновление интерфейса для отображения отфильтрованного списка
        e.page.update()


class MessageBubble(ft.Container):
    """
    Компонент "пузырька" сообщения в чате.

    Наследуется от ft.Container для создания стилизованного контейнера сообщения.
    Отображает сообщения пользователя и AI с разными стилями и позиционированием.

    Args:
        message (str): Текст сообщения для отображения
        is_user (bool): Флаг, указывающий, является ли это сообщением пользователя
    """

    def __init__(self, message: str, is_user: bool):
        # Инициализация родительского класса Container
        super().__init__()

        # Настройка отступов внутри пузырька
        self.padding = 10

        # Настройка скругления углов пузырька
        self.border_radius = 10

        # Установка цвета фона в зависимости от отправителя:
        # - Синий для сообщений пользователя
        # - Серый для сообщений AI
        self.bgcolor = ft.Colors.BLUE_700 if is_user else ft.Colors.GREY_700

        # Установка выравнивания пузырька:
        # - Справа для сообщений пользователя
        # - Слева для сообщений AI
        self.alignment = (
            ft.alignment.center_right if is_user else ft.alignment.center_left
        )

        # Настройка внешних отступов для создания эффекта диалога:
        # - Отступ слева для сообщений пользователя
        # - Отступ справа для сообщений AI
        # - Небольшие отступы сверху и снизу для разделения сообщений
        self.margin = ft.margin.only(
            left=50 if is_user else 0,  # Отступ слева
            right=0 if is_user else 50,  # Отступ справа
            top=5,  # Отступ сверху
            bottom=5,  # Отступ снизу
        )

        # Создание содержимого пузырька
        self.content = ft.Column(
            controls=[
                # Текст сообщения с настройками отображения
                ft.Text(
                    value=message,  # Текст сообщения
                    color=ft.Colors.WHITE,  # Белый цвет текста
                    size=16,  # Размер шрифта
                    selectable=True,  # Возможность выделения текста
                    weight=ft.FontWeight.W_400,  # Нормальная толщина шрифта
                )
            ],
            tight=True,  # Плотное расположение элементов в колонке
        )
