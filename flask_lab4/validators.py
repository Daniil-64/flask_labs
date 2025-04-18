"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    """
    Функциональный валидатор для проверки длины числа.

    Args:
        min: Минимальная длина числа
        max: Максимальная длина числа
        message: Опциональное сообщение об ошибке
    """

    def _number_length(form: FlaskForm, field: Field):
        # Если поле пустое, то не валидируем (для этого есть InputRequired)
        if field.data is None:
            return

        # Преобразуем число в строку и проверяем длину
        str_value = str(field.data)
        length = len(str_value)

        # Если длина не в заданном диапазоне, вызываем ошибку
        if length < min or length > max:
            default_message = f"Длина числа должна быть от {min} до {max} символов"
            raise ValidationError(message or default_message)

    return _number_length


class NumberLength:
    """
    Класс-валидатор для проверки длины числа.

    Attributes:
        min: Минимальная длина числа
        max: Максимальная длина числа
        message: Опциональное сообщение об ошибке
    """

    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        # Если поле пустое, то не валидируем (для этого есть InputRequired)
        if field.data is None:
            return

        # Преобразуем число в строку и проверяем длину
        str_value = str(field.data)
        length = len(str_value)

        # Если длина не в заданном диапазоне, вызываем ошибку
        if length < self.min or length > self.max:
            default_message = f"Длина числа должна быть от {self.min} до {self.max} символов"
            raise ValidationError(self.message or default_message)