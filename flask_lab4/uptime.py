"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

import subprocess
import shlex
from flask import Flask

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    """
    Возвращает информацию о времени работы системы (uptime)

    Returns:
        Строка с информацией о времени работы системы
    """
    # Используем флаг -p для получения информации только о времени в "pretty" формате
    command = shlex.split("uptime -p")

    try:
        # Выполняем команду и захватываем вывод
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # Убираем "up " из результата, так как команда возвращает "up X days, Y hours, Z minutes"
        uptime_output = result.stdout.strip().replace("up ", "")

        return f"Current uptime is {uptime_output}"
    except subprocess.CalledProcessError as e:
        # В случае ошибки возвращаем сообщение об ошибке
        return f"Error getting uptime: {e}", 500
    except Exception as e:
        # Обработка других возможных ошибок
        return f"Unexpected error: {e}", 500


if __name__ == '__main__':
    app.run(debug=True)