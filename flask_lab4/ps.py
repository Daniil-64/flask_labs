"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""

import subprocess
import shlex
from typing import List
from flask import Flask, request

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    """
    Запускает команду ps с переданными аргументами и возвращает её вывод

    Args:
        arg: Аргументы командной строки для команды ps (передаются через URL параметры)

    Returns:
        Результат работы команды ps с переданными аргументами
    """
    # Получаем список аргументов из запроса
    args: List[str] = request.args.getlist('arg')

    if not args:
        return "Please provide arguments for the ps command (e.g. /ps?arg=a&arg=u&arg=x)", 400

    # Базовая команда
    command = ["ps"]

    # Защищаем аргументы от инъекций, добавляя их к команде
    for arg in args:
        # Экранируем потенциально опасный ввод
        safe_arg = shlex.quote(arg)
        # Удаляем кавычки, которые добавляет shlex.quote, так как subprocess.run
        # не воспринимает аргументы с кавычками как отдельные аргументы
        safe_arg = safe_arg.strip("'")
        command.append(safe_arg)

    try:
        # Выполняем команду
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Форматируем вывод внутри тега <pre> для лучшей читаемости
        formatted_output = f"<pre>{result.stdout}</pre>"

        return formatted_output
    except subprocess.CalledProcessError as e:
        # Обрабатываем ошибки выполнения команды
        error_output = f"<pre>Error executing command: {e}\n{e.stderr}</pre>"
        return error_output, 500
    except Exception as e:
        # Обрабатываем другие ошибки
        return f"<pre>Unexpected error: {e}</pre>", 500


if __name__ == "__main__":
    app.run(debug=True)