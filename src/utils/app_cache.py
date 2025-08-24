import sqlite3
import threading
import json  # Библиотека для работы с JSON форматом
from datetime import datetime  # Библиотека для работы с датой и временем


class AppCache:
    """
    Класс для кэширования данных пользователей в SQLite базе данных.
    Обеспечивает:
    - Потокобезопасное хранение данных пользователей
    - Сохранение учетных данных (имя, фамилия, API-ключ, пароль)
    - Уникальность записей пользователей
    - Получение API-ключа по учетным данным
    """

    def __init__(self):
        """
        Инициализация системы кэширования.
        Создает:
        - Файл базы данных SQLite
        - Потокобезопасное хранилище соединений
        - Необходимые таблицы в базе данных
        """
        self.db_name = "app_cache.db"  # Имя файла базы данных
        self.local = threading.local()  # Потокобезопасное хранилище соединений
        self.create_tables()  # Создание таблиц при инициализации

    def create_tables(self):
        """
        Создает таблицы в базе данных, если они не существуют.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # SQL запросы для создания таблиц
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                user_family TEXT NOT NULL,
                user_api_key TEXT NOT NULL,
                user_password TEXT NOT NULL,
                UNIQUE(user_name, user_family, user_api_key, user_password)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Уникальный ID сообщения
                model TEXT,                           -- Идентификатор модели
                user_message TEXT,                    -- Текст от пользователя
                ai_response TEXT,                     -- Ответ от AI
                timestamp DATETIME,                   -- Время создания
                tokens_used INTEGER                   -- Использовано токенов
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analytics_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                model TEXT,
                message_length INTEGER,
                response_time FLOAT,
                tokens_used INTEGER
            )
        """
        )

        conn.commit()
        conn.close()

    def get_connection(self):
        """
        Возвращает соединение с базой данных для текущего потока.
        Если соединения нет, создает новое.

        Returns:
            sqlite3.Connection: Соединение с базой данных.
        """
        if not hasattr(self.local, "connection"):
            self.local.connection = sqlite3.connect(self.db_name)
        return self.local.connection

    def save_user(self, name: str, family: str, api_key: str, password: str) -> bool:
        """
        Сохраняет данные нового пользователя в базе данных.

        Args:
            name (str): Имя пользователя.
            family (str): Фамилия пользователя.
            api_key (str): API-ключ пользователя.
            password (str): Пароль пользователя.

        Returns:
            bool: True, если пользователь успешно сохранен, иначе False.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (user_name, user_family, user_api_key, user_password)
                VALUES (?, ?, ?, ?)
                """,
                (name, family, api_key, password),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            conn.rollback()
            return False

    def get_user_api_key(self, name: str, family: str, password: str) -> str | None:
        """
        Получает API-ключ пользователя по имени, фамилии и паролю.

        Args:
            name (str): Имя пользователя.
            family (str): Фамилия пользователя.
            password (str): Пароль пользователя.

        Returns:
            str | None: API-ключ пользователя, если найден, иначе None.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT user_api_key FROM users
            WHERE user_name = ? AND user_family = ? AND user_password = ?
            """,
            (name, family, password),
        )
        result = cursor.fetchone()
        return result[0] if result else False

    def save_message(self, model, user_message, ai_response, tokens_used):
        """
        Сохранение нового сообщения в базу данных.

        Args:
            model (str): Идентификатор использованной модели
            user_message (str): Текст сообщения пользователя
            ai_response (str): Ответ AI модели
            tokens_used (int): Количество использованных токенов
        """
        conn = self.get_connection()  # Получение соединения для текущего потока
        cursor = conn.cursor()

        # Вставка новой записи в таблицу messages
        cursor.execute(
            """
            INSERT INTO messages (model, user_message, ai_response, timestamp, tokens_used)
            VALUES (?, ?, ?, ?, ?)
        """,
            (model, user_message, ai_response, datetime.now(), tokens_used),
        )
        conn.commit()  # Сохранение изменений

    def get_chat_history(self, limit=50):
        """
        Получение последних сообщений из истории чата.

        Args:
            limit (int): Максимальное количество возвращаемых сообщений

        Returns:
            list: Список кортежей с данными сообщений, отсортированных
                 по времени в обратном порядке (новые сначала)
        """
        conn = self.get_connection()  # Получение соединения для текущего потока
        cursor = conn.cursor()

        # Получение последних сообщений с ограничением по количеству
        cursor.execute(
            """
            SELECT * FROM messages 
            ORDER BY timestamp DESC 
            LIMIT ?
        """,
            (limit,),
        )
        return cursor.fetchall()  # Возврат всех найденных записей

    def save_analytics(
        self, timestamp, model, message_length, response_time, tokens_used
    ):
        """
        Сохранение данных аналитики в базу данных.

        Args:
            timestamp (datetime): Время создания записи
            model (str): Идентификатор использованной модели
            message_length (int): Длина сообщения
            response_time (float): Время ответа
            tokens_used (int): Количество использованных токенов
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO analytics_messages 
            (timestamp, model, message_length, response_time, tokens_used)
            VALUES (?, ?, ?, ?, ?)
        """,
            (timestamp, model, message_length, response_time, tokens_used),
        )
        conn.commit()

    def get_analytics_history(self):
        """
        Получение всей истории аналитики.

        Returns:
            list: Список записей аналитики
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT timestamp, model, message_length, response_time, tokens_used
            FROM analytics_messages
            ORDER BY timestamp ASC
        """
        )
        return cursor.fetchall()

    def __del__(self):
        """
        Деструктор класса.

        Закрывает соединения с базой данных при уничтожении объекта,
        предотвращая утечки ресурсов.
        """
        # Проверка наличия соединения в текущем потоке
        if hasattr(self.local, "connection"):
            self.local.connection.close()  # Закрытие соединения

    def clear_history(self):
        """
        Очистка всей истории сообщений.

        Удаляет все записи из таблицы messages,
        эффективно очищая всю историю чата.
        """
        conn = self.get_connection()  # Получение соединения
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages")  # Удаление всех записей
        conn.commit()  # Сохранение изменений

    def get_formatted_history(self):
        """
        Получение отформатированной истории диалога.

        Returns:
            list: Список словарей с данными сообщений в формате:
                {
                    "id": int,              # ID сообщения
                    "model": str,           # Использованная модель
                    "user_message": str,    # Сообщение пользователя
                    "ai_response": str,     # Ответ AI
                    "timestamp": datetime,  # Время создания
                    "tokens_used": int      # Использовано токенов
                }
        """
        conn = self.get_connection()  # Получение соединения
        cursor = conn.cursor()

        # Получение всех сообщений, отсортированных по времени
        cursor.execute(
            """
            SELECT 
                id,
                model,
                user_message,
                ai_response,
                timestamp,
                tokens_used
            FROM messages 
            ORDER BY timestamp ASC
        """
        )

        # Формирование списка словарей с данными сообщений
        history = []
        for row in cursor.fetchall():
            history.append(
                {
                    "id": row[0],  # ID сообщения
                    "model": row[1],  # Использованная модель
                    "user_message": row[2],  # Сообщение пользователя
                    "ai_response": row[3],  # Ответ AI
                    "timestamp": row[4],  # Временная метка
                    "tokens_used": row[5],  # Использовано токенов
                }
            )
        return history  # Возврат форматированной истории
