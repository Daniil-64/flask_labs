"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask

app = Flask(__name__)

# Для оптимизации, будем хранить траты по структуре:
# {year: {month: {day: amount}}}
# А также кэшировать суммы по месяцам и годам
storage = {}
monthly_sums = {}  # {year: {month: sum}}
yearly_sums = {}   # {year: sum}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    """
    Добавляет информацию о трате за определенный день

    Args:
        date: Дата в формате YYYYMMDD
        number: Сумма траты в рублях

    Returns:
        Сообщение о добавлении траты
    """
    # Проверка формата даты
    if len(date) != 8 or not date.isdigit():
        return "Ошибка: неверный формат даты. Используйте YYYYMMDD", 400

    # Парсим дату из формата YYYYMMDD
    try:
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:8])

        # Базовая проверка корректности даты
        if month < 1 or month > 12 or day < 1 or day > 31:
            return "Ошибка: некорректная дата", 400
    except ValueError:
        return "Ошибка при разборе даты", 400

    # Используем setdefault для создания вложенных словарей при необходимости
    year_data = storage.setdefault(year, {})
    month_data = year_data.setdefault(month, {})

    # Добавляем или обновляем трату за день
    if day in month_data:
        month_data[day] += number
    else:
        month_data[day] = number

    # Обновляем кэшированные суммы
    # Для месяца
    monthly_sums.setdefault(year, {})
    if month in monthly_sums[year]:
        monthly_sums[year][month] += number
    else:
        monthly_sums[year][month] = number

    # Для года
    if year in yearly_sums:
        yearly_sums[year] += number
    else:
        yearly_sums[year] = number

    return f"Добавлена трата в размере {number} рублей за {date}"


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    # Используем кэшированную сумму за год, если она есть
    if year in yearly_sums:
        return f"Сумма трат за {year} год: {yearly_sums[year]} рублей"
    return f"За {year} год не было трат"


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    # Используем кэшированную сумму за месяц, если она есть
    if year in monthly_sums and month in monthly_sums[year]:
        return f"Сумма трат за {month}/{year}: {monthly_sums[year][month]} рублей"
    return f"За {month}/{year} не было трат"


if __name__ == "__main__":
    app.run(debug=True)