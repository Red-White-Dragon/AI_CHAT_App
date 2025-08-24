import os  # Библиотека для работы с операционной системой
import time  # Библиотека для работы с временными метками
import json  # Библиотека для работы с JSON-данными
import asyncio  # Библиотека для асинхронного программирования
from datetime import datetime  # Класс для работы с датой и временем
import flet as ft
from flet_route import Params, Basket
from src.api.openrouter import (
    OpenRouterClient,
)  # Клиент для взаимодействия с AI через API OpenRouter
from src.ui.app_style import AppStyles  # Модуль с настройками стилей интерфейса
from src.ui.components import (
    MessageBubble,
    ModelSelector,
)  # Компоненты пользовательского интерфейса
from src.utils.app_cache import AppCache  # Модуль для кэширования истории чата
from src.utils.app_logger import AppLogger  # Модуль для логирования работы приложения
from src.utils.app_analytics import (
    AppAnalytics,
)  # Модуль для сбора и анализа статистики использования
#from src.utils.app_monitor import AppMonitor  # Модуль для мониторинга производительности


class InterfacePage:

    def view(
        self,
        page: ft.Page,  # Объект текущей страницы
        params: Params,  # Параметры маршрута
        basket: Basket,  # Корзина для хранения данных между страницами
    ) -> ft.View:

        # Инициализация основных компонентов
        api_key = basket.get("key") # Получение ключа из корзины
        basket.delete("key") # Удаление ключа из корзины
        api_client = OpenRouterClient(api_key)  # Создание клиента для работы с AI API
        cache = AppCache()  # Инициализация системы кэширования
        logger = AppLogger()  # Инициализация системы логирования
        analytics = AppAnalytics(
            cache
        )  # Инициализация системы аналитики с передачей кэша
        #monitor = AppMonitor()  # Инициализация системы мониторинга

        models = api_client.available_models # Получение списока доступных моделей

        exports_dir = "exports" # Формируем путь к папке exports
        os.makedirs(exports_dir, exist_ok=True)  # Создание директории, если её нет
        
        page.title = "Интерфейс"
        
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
        
        # --- Функции ---
        def update_balance():
            try:
                balance = api_client.get_balance()  # Запрос баланса через API
                balance_text.value = (
                    f"Баланс: {balance}"  # Обновление текста с балансом
                )
                balance_text.color = (
                    ft.Colors.GREEN_400
                )  # Установка зеленого цвета для успешного получения
            except Exception as e:
                # Обработка ошибки получения баланса
                balance_text.value = "Баланс: н/д"  # Установка текста ошибки
                balance_text.color = (
                    ft.Colors.RED_400
                )  # Установка красного цвета для ошибки
                logger.error(f"Ошибка обновления баланса: {e}")

        def load_chat_history():
            """
            Загрузка истории чата из кэша и отображение её в интерфейсе.
            Сообщения добавляются в обратном порядке для правильной хронологии.
            """
            try:
                history = cache.get_chat_history()  # Получение истории из кэша
                for msg in reversed(history):  # Перебор сообщений в обратном порядке
                    # Распаковка данных сообщения в отдельные переменные
                    _, model, user_message, ai_response, timestamp, tokens = msg
                    # Добавление пары сообщений (пользователь + AI) в интерфейс
                    chat_history.controls.extend(
                        [
                            MessageBubble(  # Создание пузырька сообщения пользователя
                                message=user_message, is_user=True
                            ),
                            MessageBubble(  # Создание пузырька ответа AI
                                message=ai_response, is_user=False
                            ),
                        ]
                    )
            except Exception as e:
                # Логирование ошибки при загрузке истории
                logger.error(f"Ошибка загрузки истории чата: {e}")

        async def send_message_click(e):
            """
            Асинхронная функция отправки сообщения.
            """
            if not message_input.value:
                return

            try:
                # Визуальная индикация процесса
                message_input.border_color = ft.Colors.BLUE_400
                page.update()

                # Сохранение данных сообщения
                start_time = time.time()
                user_message = message_input.value
                message_input.value = ""
                page.update()

                # Добавление сообщения пользователя
                chat_history.controls.append(
                    MessageBubble(message=user_message, is_user=True)
                )

                # Индикатор загрузки
                loading = ft.ProgressRing()
                chat_history.controls.append(loading)
                page.update()

                # Асинхронная отправка запроса
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: api_client.send_message(user_message, model_dropdown.value),
                )

                # Удаление индикатора загрузки
                chat_history.controls.remove(loading)

                # Обработка ответа
                if "error" in response:
                    response_text = f"Ошибка: {response['error']}"
                    tokens_used = 0
                    logger.error(f"Ошибка API: {response['error']}")
                else:
                    response_text = response["choices"][0]["message"]["content"]
                    tokens_used = response.get("usage", {}).get("total_tokens", 0)

                # Сохранение в кэш
                cache.save_message(
                    model=model_dropdown.value,
                    user_message=user_message,
                    ai_response=response_text,
                    tokens_used=tokens_used,
                )

                # Добавление ответа в чат
                chat_history.controls.append(
                    MessageBubble(message=response_text, is_user=False)
                )

                # Обновление аналитики
                response_time = time.time() - start_time
                analytics.track_message(
                    model=model_dropdown.value,
                    message_length=len(user_message),
                    response_time=response_time,
                    tokens_used=tokens_used,
                )

                # Логирование метрик
                #monitor.log_metrics(logger)
                page.update()

            except Exception as e:
                logger.error(f"Ошибка отправки сообщения: {e}")
                message_input.border_color = ft.Colors.RED_500

                # Показ уведомления об ошибке
                snack = ft.SnackBar(
                    content=ft.Text(
                        str(e), color=ft.Colors.RED_500, weight=ft.FontWeight.BOLD
                    ),
                    bgcolor=ft.Colors.GREY_900,
                    duration=5000,
                )
                page.overlay.append(snack)
                snack.open = True
                page.update()
                
        def show_error_snack(page, message: str):
            """Показ уведомления об ошибке"""
            snack = ft.SnackBar(  # Создание уведомления
                content=ft.Text(message, color=ft.Colors.RED_500),
                bgcolor=ft.Colors.GREY_900,
                duration=5000,
            )
            page.overlay.append(snack)  # Добавление уведомления
            snack.open = True  # Открытие уведомления
            page.update()  # Обновление страницы

        async def show_analytics(e):
            """Показ статистики использования"""
            stats = analytics.get_statistics()  # Получение статистики

            # Создание диалога статистики
            dialog = ft.AlertDialog(
                title=ft.Text("Аналитика"),
                content=ft.Column(
                    [
                        ft.Text(f"Всего сообщений: {stats['total_messages']}"),
                        ft.Text(f"Всего токенов: {stats['total_tokens']}"),
                        ft.Text(
                            f"Среднее токенов/сообщение: {stats['tokens_per_message']:.2f}"
                        ),
                        ft.Text(
                            f"Сообщений в минуту: {stats['messages_per_minute']:.2f}"
                        ),
                    ]
                ),
                actions=[
                    ft.TextButton("Закрыть", on_click=lambda e: close_dialog(dialog)),
                ],
            )

            page.overlay.append(dialog)  # Добавление диалога
            dialog.open = True  # Открытие диалога
            page.update()  # Обновление страницы

        async def clear_history(e):
            """
            Очистка истории чата.
            """
            try:
                cache.clear_history()  # Очистка кэша
                analytics.clear_data()  # Очистка аналитики
                chat_history.controls.clear()  # Очистка истории чата

            except Exception as e:
                logger.error(f"Ошибка очистки истории: {e}")
                show_error_snack(page, f"Ошибка очистки истории: {str(e)}")

        async def confirm_clear_history(e):
            """Подтверждение очистки истории"""

            def close_dlg(e):  # Функция закрытия диалога
                close_dialog(dialog)

            async def clear_confirmed(e):  # Функция подтверждения очистки
                await clear_history(e)
                close_dialog(dialog)

            # Создание диалога подтверждения
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Подтверждение удаления"),
                content=ft.Text("Вы уверены? Это действие нельзя отменить!"),
                actions=[
                    ft.TextButton("Отмена", on_click=close_dlg),
                    ft.TextButton("Очистить", on_click=clear_confirmed),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        def close_dialog(dialog):
            """Закрытие диалогового окна"""
            dialog.open = False  # Закрытие диалога
            page.update()  # Обновление страницы

            if dialog in page.overlay:  # Удаление из overlay
                page.overlay.remove(dialog)

        async def save_dialog(e):
            """
            Сохранение истории диалога в JSON файл.
            """
            try:
                # Получение истории из кэша
                history = cache.get_chat_history()

                # Форматирование данных для сохранения
                dialog_data = []
                for msg in history:
                    dialog_data.append(
                        {
                            "timestamp": msg[4],
                            "model": msg[1],
                            "user_message": msg[2],
                            "ai_response": msg[3],
                            "tokens_used": msg[5],
                        }
                    )

                # Создание имени файла
                filename = (
                    f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
                filepath = os.path.join(exports_dir, filename)

                # Сохранение в JSON
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(dialog_data, f, ensure_ascii=False, indent=2, default=str)

                # Создание диалога успешного сохранения
                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Диалог сохранен"),
                    content=ft.Column(
                        [
                            ft.Text("Путь сохранения:"),
                            ft.Text(
                                filepath, selectable=True, weight=ft.FontWeight.BOLD
                            ),
                        ]
                    ),
                    actions=[
                        ft.TextButton("OK", on_click=lambda e: close_dialog(dialog)),
                        ft.TextButton(
                            "Открыть папку",
                            on_click=lambda e: os.startfile(exports_dir),
                        ),
                    ],
                )

                page.overlay.append(dialog)
                dialog.open = True
                page.update()

            except Exception as e:
                logger.error(f"Ошибка сохранения: {e}")
                show_error_snack(page, f"Ошибка сохранения: {str(e)}")

        # --- Внешний вид ---
        
        # Инициализация выпадающего списка для выбора модели AI
        model_dropdown = ModelSelector(models)
        model_dropdown.value = models[0] if models else None
        
        # Создание компонента для отображения баланса API
        balance_text = ft.Text(
            value="Баланс: Загрузка...",  # Начальный текст до загрузки реального баланса
            size=16,
            color=ft.Colors.GREEN_400,
            weight=ft.FontWeight.BOLD,
        )
        update_balance()  # Первичное обновление баланса

        # Создание компонентов интерфейса
        message_input = ft.TextField(
            **AppStyles.message_input,
            on_submit=send_message_click,
        )  # Поле ввода
        
        # История чата
        chat_history = ft.ListView(**AppStyles.chat_history)

        # Загрузка существующей истории
        load_chat_history()

        # Создание кнопок управления
        save_button = ft.ElevatedButton(
            on_click=save_dialog,  # Привязка функции сохранения
            **AppStyles.SAVE_BUTTON,  # Применение стилей
            
        )

        clear_button = ft.ElevatedButton(
            on_click=confirm_clear_history,  # Привязка функции очистки
            **AppStyles.CLEAR_BUTTON,  # Применение стилей
        )

        send_button = ft.ElevatedButton(
            on_click=send_message_click,  # Привязка функции отправки
            **AppStyles.SEND_BUTTON,  # Применение стилей
        )

        analytics_button = ft.ElevatedButton(
            on_click=show_analytics,  # Привязка функции аналитики
            **AppStyles.ANALYTICS_BUTTON,  # Применение стилей
        )

        # Создание layout компонентов

        # Создание ряда кнопок управления
        control_buttons = ft.Row(
            controls=[  # Размещение кнопок в ряд
                save_button,
                analytics_button,
                clear_button,
            ],
            **AppStyles.CONTROL_BUTTONS_ROW,  # Применение стилей к ряду
        )

        # Создание строки ввода с кнопкой отправки
        input_row = ft.Row(
            controls=[message_input, send_button],  # Размещение элементов ввода
            **AppStyles.INPUT_ROW,  # Применение стилей к строке ввода
        )

        # Создание колонки для элементов управления
        controls_column = ft.Column(
            controls=[input_row, control_buttons],  # Размещение элементов управления
            **AppStyles.CONTROLS_COLUMN,  # Применение стилей к колонке
        )

        # Создание контейнера для баланса
        balance_container = ft.Container(
            content=balance_text,  # Размещение текста баланса
            **AppStyles.BALANCE_CONTAINER,  # Применение стилей к контейнеру
        )

        # Создание колонки выбора модели
        model_selection = ft.Column(
            controls=[  # Размещение элементов выбора модели
                model_dropdown.text,
                model_dropdown.search_field,
                model_dropdown,
                balance_container,
            ],
            **AppStyles.MODEL_SELECTION_COLUMN,  # Применение стилей к колонке
        )

        # Создание основной колонки приложения
        main_column = ft.Column(
            controls=[  # Размещение основных элементов
                model_selection,
                chat_history,
                controls_column,
            ],
            **AppStyles.MAIN_COLUMN,  # Применение стилей к главной колонке
        )

        page_body = ft.Container(
            content=main_column,
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

        
        # Запуск монитора
        #monitor.get_metrics()

        # Логирование запуска
        logger.info("Приложение запущено")

        return ft.View(
            "/interface",
            controls=[stack],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            padding=0,
        )