import flet as ft


class AppStyles:
    """
    Класс для хранения стилей приложения.
    Содержит цвета, размеры, шрифты и стили для различных элементов интерфейса.
    """

    # --- Цвета ---
    light_black_color: str = "#0E0E0E"  # Светло-черный (основной темный цвет)
    light_black_trans_color: str = "#BC0E0E0E"  # Светло-черный прозрачный (для фонов)
    white_color: str = "#FFFFFF"  # Белый (для текста и акцентных элементов)
    light_blue_color: str = "#42A5F5"  # Голубовато-зелёный (акцентный цвет)
    light_salmon_color: str = (
        "#EF9A9A"  # Светло-лососевый (для ошибок и предупреждений)
    )

    # --- Размеры ---
    page_width: int = 700  # Ширина окна приложения
    page_height: int = 700  # Высота окна приложения

    # --- Шрифты ---
    fonts_styles: dict = {
        "Trafaret": "fonts/TrafaretKit.ttf",  # Шрифт для заголовков
        "LumiosTypewriter": "fonts/LumiosTypewriter-New.ttf",  # Моноширинный шрифт для текста
        "Bahnschrift": "fonts/Bahnschrift.ttf",  # Универсальный шрифт для кнопок и полей
    }

    # --- Стили страниц ---
    ## Стиль текстовых полей
    text_fields_style: dict = {
        "weight": ft.FontWeight.W_500,  # Насыщенность шрифта
        "selectable": True,  # Разрешить выделение текста
        "no_wrap": False,  # Перенос текста при необходимости
    }

    # Стиль полей ввода
    input_field_style: dict = {
        "border_width": 0,  # Толщина границы
        "filled": True,  # Заполнять цветом
        "fill_color": white_color,  # Цвет заполнения
        "text_size": 20,  # Размер шрифта
        "text_style": ft.TextStyle(
            font_family="LumiosTypewriter",  # Семейство шрифта
            color=light_black_color,  # Цвет текста
            weight=ft.FontWeight.W_500,
        ),
        "border_radius": ft.border_radius.all(20),  # Скругление углов
        "content_padding": ft.padding.only(
            top=16, left=5, right=5, bottom=16
        ),  # Отступы внутри поля
        "multiline": True,  # Включает перенос текста на новую строку
    }

    ## Стиль контейнеров с содержимым страниц
    page_body_style: dict = {
        "alignment": ft.alignment.center,
        "bgcolor": light_black_trans_color,  # Фоновый цвет (прозрачный темный)
        "border": ft.border.all(  # Сплошная граница со всех сторон
            color=light_blue_color,  # Цвет границы
            width=3,  # Ширина границы
        ),
        "border_radius": 20,  # Скругление углов
        "padding": ft.padding.only(
            top=30, left=20, right=20, bottom=30
        ),  # Внутренние отступы
    }

    # --- Стили кнопок ---
    ## Стиль белой кнопки
    button_white_style: dict = {
        "bgcolor": {
            ft.ControlState.HOVERED: white_color,  # Фон при наведении
            ft.ControlState.DEFAULT: light_black_color,  # Фон по умолчанию
        },
        "color": {
            ft.ControlState.HOVERED: light_black_color,  # Цвет текста при наведении
            ft.ControlState.DEFAULT: white_color,  # Цвет текста по умолчанию
        },
        "side": ft.BorderSide(
            color=white_color,  # Цвет границы
            width=3,  # Толщина границы
        ),
        "shape": ft.RoundedRectangleBorder(
            radius=20,  # Скругление углов
        ),
        "text_style": ft.TextStyle(
            font_family="Bahnschrift",  # Семейство шрифта
            size=20,  # Размер шрифта
            weight=ft.FontWeight.W_400,  # Насыщенность шрифта
        ),
        "padding": ft.padding.only(top=22, left=5, right=5, bottom=22),
    }

    ## Стиль синей кнопки
    button_blue_style: dict = {
        "bgcolor": {
            ft.ControlState.HOVERED: white_color,  # Фон при наведении
            ft.ControlState.DEFAULT: light_blue_color,  # Фон по умолчанию
        },
        "color": {
            ft.ControlState.HOVERED: light_blue_color,  # Цвет текста при наведении
            ft.ControlState.DEFAULT: white_color,  # Цвет текста по умолчанию
        },
        "side": ft.BorderSide(
            color=ft.Colors.WHITE,  # Цвет границы
            width=3,  # Толщина границы
        ),
        "shape": ft.RoundedRectangleBorder(
            radius=20,  # Скругление углов
        ),
        "text_style": ft.TextStyle(
            font_family="Bahnschrift",  # Семейство шрифта
            size=20,  # Размер шрифта
            weight=ft.FontWeight.W_400,  # Насыщенность шрифта
        ),
        "padding": ft.padding.only(top=22, left=5, right=5, bottom=22),
    }
    
    
    # Настройки области истории чата
    chat_history = {
        "expand": True,  # Разрешаем расширение на все доступное пространство
        "spacing": 10,  # Отступ между сообщениями в пикселях
        "height": 400,  # Фиксированная высота области чата
        "auto_scroll": True,  # Автоматическая прокрутка к новым сообщениям
        "padding": 20,  # Внутренние отступы области чата
    }
    
    # Настройки кнопки сохранения диалога
    SAVE_BUTTON = {
        "text": "Сохранить",  # Текст на кнопке
        "icon": ft.Icons.SAVE,  # Иконка сохранения
        "style": ft.ButtonStyle(  # Стиль оформления кнопки
            color=ft.Colors.WHITE,  # Цвет текста
            bgcolor=ft.Colors.BLUE_700,  # Цвет фона
            padding=ft.padding.only(top=22, left=5, right=5, bottom=22),  # Внутренние отступы
        ),
        "tooltip": "Сохранить диалог в файл",  # Всплывающая подсказка
        "width": 130,  # Ширина кнопки
    }
    
    # Настройки кнопки очистки истории
    CLEAR_BUTTON = {
        "text": "Очистить",  # Текст на кнопке
        "icon": ft.Icons.DELETE,  # Иконка удаления
        "style": ft.ButtonStyle(  # Стиль оформления кнопки
            color=ft.Colors.WHITE,  # Цвет текста
            bgcolor=ft.Colors.RED_700,  # Красный цвет фона для предупреждения
            padding=ft.padding.only(top=22, left=5, right=5, bottom=22),  # Внутренние отступы
        ),
        "tooltip": "Очистить историю чата",  # Всплывающая подсказка
        "width": 130,  # Ширина кнопки
    }
    
    # Настройки кнопки отправки сообщения
    SEND_BUTTON = {
        "text": "Отправка",  # Текст на кнопке
        "icon": ft.Icons.SEND,  # Иконка отправки сообщения
        "style": ft.ButtonStyle(  # Стиль оформления кнопки
            color=ft.Colors.WHITE,  # Цвет текста кнопки
            bgcolor=ft.Colors.BLUE_700,  # Цвет фона кнопки
            padding= ft.padding.only(top=22, left=5, right=5, bottom=22),  # Внутренние отступы
        ),
        "tooltip": "Отправить сообщение",  # Всплывающая подсказка при наведении
        "width": 130,  # Ширина кнопки
    }
    
    # Настройки кнопки показа аналитики
    ANALYTICS_BUTTON = {
        "text": "Аналитика",  # Текст на кнопке
        "icon": ft.Icons.ANALYTICS,  # Иконка аналитики
        "style": ft.ButtonStyle(  # Стиль оформления кнопки
            color=ft.Colors.WHITE,  # Цвет текста
            bgcolor=ft.Colors.GREEN_700,  # Зеленый цвет фона
            padding=ft.padding.only(top=22, left=5, right=5, bottom=22),  # Внутренние отступы
        ),
        "tooltip": "Показать аналитику",  # Всплывающая подсказка
        "width": 130,  # Ширина кнопки
    }
    
    # Настройки строки с кнопками управления
    CONTROL_BUTTONS_ROW = {
        "spacing": 20,  # Отступ между кнопками
        "alignment": ft.MainAxisAlignment.CENTER,  # Выравнивание кнопок по центру
        "wrap": True,
    }
    
    # Настройки строки с полем ввода и кнопкой отправки
    INPUT_ROW = {
        "spacing": 20,  # Отступ между элементами
        "alignment": ft.MainAxisAlignment.CENTER,  # Распределение пространства между элементами
        "width": 920,  # Общая ширина строки
        "wrap": True,
    }
    
    # Настройки колонки с элементами управления
    CONTROLS_COLUMN = {
        "spacing": 20,  # Отступ между элементами
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Выравнивание по центру по горизонтали
    }
    
    # Настройки контейнера для отображения баланса
    BALANCE_CONTAINER = {
        "padding": 10,  # Внутренние отступы
        "bgcolor": ft.Colors.GREY_900,  # Цвет фона
        "border_radius": 8,  # Радиус скругления углов
        "border": ft.border.all(1, ft.Colors.GREY_700),  # Тонкая серая граница
    }
    
    # Настройки колонки с элементами выбора модели
    MODEL_SELECTION_COLUMN = {
        "spacing": 10,  # Отступ между элементами
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Выравнивание по центру
        "width": 400,  # Ширина колонки
    }
    
    # Настройки главной колонки приложения
    MAIN_COLUMN = {
        "expand": True,  # Разрешение расширения
        "spacing": 20,  # Отступ между элементами
        "alignment": ft.MainAxisAlignment.CENTER,  # Вертикальное выравнивание по центру
        "horizontal_alignment": ft.CrossAxisAlignment.CENTER,  # Горизонтальное выравнивание по центру
        "scroll": ft.ScrollMode.AUTO,
    }
    
    # Настройки поля поиска модели
    model_search_field = {
        "width": 400,  # Ширина поля в пикселях
        "border_radius": 20,  # Радиус скругления углов
        "border_width": 3, # Ширина границы
        "border_color": light_black_color,  # Цвет границы в обычном состоянии
        "focused_border_color": light_blue_color,  # Цвет границы при фокусе
        "bgcolor": light_black_trans_color,  # Цвет фона поля
        "focused_bgcolor": light_black_color,  # Цвет фона при фокусе
        "color": white_color,  # Цвет текста
        "cursor_color": white_color,  # Цвет курсора
        "content_padding": ft.padding.only(
            top=16, left=5, right=5, bottom=16
        ),  # Отступы внутри поля
        "hint_style": ft.TextStyle(  # Стиль текста-подсказки
            size=18,  # Размер шрифта подсказки
            font_family="LumiosTypewriter", # Семейство шрифта
            color=white_color,  # Цвет текста-подсказки
        ),
        "prefix_icon": ft.Icons.SEARCH,  # Иконка поиска слева от поля
        "text_align": ft.alignment.center, # центровать содержимое
    }
    
    # Настройки выпадающего списка выбора модели
    model_dropdown = {
        "width": 400,  # Ширина списка
        "height": 45,  # Высота в закрытом состоянии
        "border_radius": 20,  # Радиус скругления углов
        "bgcolor": ft.Colors.GREY_900,  # Цвет фона
        "border_color": ft.Colors.GREY_700,  # Цвет границы
        "border_width": 3,  # Толщина границы
        "color": white_color,  # Цвет текста
        "content_padding": 10,  # Внутренние отступы
        "focused_border_color": ft.Colors.BLUE_400,  # Цвет границы при фокусе
        "focused_bgcolor": ft.Colors.GREY_800,  # Цвет фона при фокусе
    }
    
    # Настройки поля ввода сообщений
    message_input = {
        "width": 400,  # Ширина поля ввода в пикселях
        "height": 50,  # Высота поля ввода в пикселях
        "multiline": False,  # Запрет многострочного ввода
        "text_size": 16,  # Размер шрифта текста
        "color": ft.Colors.WHITE,  # Цвет вводимого текста
        "bgcolor": ft.Colors.GREY_800,  # Цвет фона поля ввода
        "border_color": ft.Colors.BLUE_400,  # Цвет границы поля
        "cursor_color": ft.Colors.WHITE,  # Цвет курсора ввода
        "content_padding": 10,  # Внутренние отступы текста
        "border_radius": 8,  # Радиус скругления углов
        "hint_text": "Введите сообщение здесь...",  # Текст-подсказка в пустом поле
        "shift_enter": True,  # Включение отправки по Shift+Enter
    }
    
    # Настройки области истории чата
    chat_history = {
        "expand": True,  # Разрешаем расширение на все доступное пространство
        "spacing": 10,  # Отступ между сообщениями в пикселях
        "height": 400,  # Фиксированная высота области чата
        "auto_scroll": True,  # Автоматическая прокрутка к новым сообщениям
        "padding": 20,  # Внутренние отступы области чата
    }