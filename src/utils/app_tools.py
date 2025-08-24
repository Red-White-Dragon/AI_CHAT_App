import re
import random
import string
import flet as ft
from flet_route import Basket


class Validator:

    def validation_name(self, name: str) -> bool:
        name_pattern = re.compile(r"^[a-zA-Zа-яА-Я]+$")
        return bool(re.match(name_pattern, name))

    def validation_family(self, family: str) -> bool:
        family_pattern = re.compile(r"^[a-zA-Zа-яА-Я]+$")
        return bool(re.match(family_pattern, family))

    def validation_api_key(self, api_key: str) -> bool:
        api_key_pattern = re.compile(r"^sk-[a-zA-Z0-9_-]{60,100}$")
        return bool(re.match(api_key_pattern, api_key))

    def validation_password(self, password: str) -> bool:
        password_pattern = re.compile(
            r"^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*_)[a-zA-Z0-9_]{10,100}$"
        )
        return bool(re.match(password_pattern, password))

    def registration_valid(
        self, name: str, family: str, api_key: str, password: str
    ) -> list:
        registration_error_text = []
        if not all([name, family, api_key, password]):
            registration_error_text.append("Заполните все поля!!!")
        if not self.validation_name(name):
            registration_error_text.append(
                "Введите имя (русские или английские буквы)."
            )
        if not self.validation_family(family):
            registration_error_text.append(
                "Введите фамилию (русские или английские буквы)."
            )
        if not self.validation_api_key(api_key):
            registration_error_text.append("Введите ключ OpenRouter.")
        if not self.validation_password(password):
            registration_error_text.append(
                "Введите пароль (обязательно: английские буквы, цифры, символы подчеркивания; не менее 10 символов)."
            )
        return registration_error_text

    def entrance_valid(self, name: str, family: str, password: str) -> list:
        entrance_error_text = []
        if not all([name, family, password]):
            entrance_error_text.append("Заполните все поля!!!")
        if not self.validation_name(name):
            entrance_error_text.append("Введите имя (русские или английские буквы).")
        if not self.validation_family(family):
            entrance_error_text.append(
                "Введите фамилию (русские или английские буквы)."
            )
        if not self.validation_password(password):
            entrance_error_text.append(
                "Введите пароль (обязательно: английские буквы, цифры, символы подчеркивания; не менее 10 символов)."
            )
        return entrance_error_text


def restore_basket(basket: Basket, key: str, text_field: ft.Control) -> None:
    if basket.get(key):
        text_field.value = basket.get(key)


def generate_password(text_field: ft.Control) -> None:
    letters = string.ascii_letters
    digits = string.digits
    underscore = "_"

    all_chars = letters + digits + underscore

    password = [random.choice(letters), random.choice(digits), underscore]

    password += random.choices(all_chars, k=7)

    random.shuffle(password)

    generated_password = "".join(password)
    text_field.value = generated_password
    text_field.update()