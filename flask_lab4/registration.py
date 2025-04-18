"""
В эндпоинт /registration добавьте все валидаторы, о которых говорилось в последнем видео:

1) email (текст, обязательно для заполнения, валидация формата);
2) phone (число, обязательно для заполнения, длина — десять символов, только положительные числа);
3) name (текст, обязательно для заполнения);
4) address (текст, обязательно для заполнения);
5) index (только числа, обязательно для заполнения);
6) comment (текст, необязательно для заполнения).
"""

from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Email, NumberRange, Optional
from validators import number_length, NumberLength

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    # Email: текст, обязательно, валидация формата
    email = StringField(validators=[
        InputRequired(message="Email обязателен для заполнения"),
        Email(message="Некорректный формат email")
    ])

    # Phone: число, обязательно, 10 символов, положительное
    # Используем оба типа валидаторов из hw2_validators
    phone = IntegerField(validators=[
        InputRequired(message="Телефон обязателен для заполнения"),
        NumberRange(min=0, message="Телефон должен быть положительным числом"),
        number_length(min=10, max=10, message="Телефон должен состоять из 10 цифр"),
        NumberLength(min=10, max=10, message="Телефон должен состоять из 10 цифр")
    ])

    # Name: текст, обязательно
    name = StringField(validators=[
        InputRequired(message="Имя обязательно для заполнения")
    ])

    # Address: текст, обязательно
    address = StringField(validators=[
        InputRequired(message="Адрес обязателен для заполнения")
    ])

    # Index: только числа, обязательно
    index = IntegerField(validators=[
        InputRequired(message="Индекс обязателен для заполнения")
    ])

    # Comment: текст, необязательно
    comment = StringField(validators=[
        Optional()
    ])


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data

        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)