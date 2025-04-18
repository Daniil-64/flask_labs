import datetime
import random
import re
import os
from flask import Flask

app = Flask(__name__)

# Глобальные переменные
cars = ["Chevrolet", "Renault", "Ford", "Lada"]
cat_breeds = ["корниш-рекс", "русская голубая", "шотландская вислоухая", "мейн-кун", "манчкин"]

# Загрузка списка слов из файла "Война и мир" при запуске приложения
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

def get_words_from_book():
    """Функция для получения списка слов из книги"""
    try:
        with open(BOOK_FILE, 'r', encoding='utf-8') as book:
            content = book.read()
            # Используем регулярное выражение для извлечения слов и удаления знаков препинания
            words = re.findall(r'\b[А-Яа-яA-Za-z]+\b', content)
            return words
    except FileNotFoundError:
        # Возвращаем список с одним элементом в случае отсутствия файла
        return ["FileNotFound"]

# Загружаем слова при старте приложения
book_words = get_words_from_book()

@app.route('/hello_world')
def hello_world():
    """Возвращает текст 'Привет, мир!'"""
    return "Привет, мир!"

@app.route('/cars')
def get_cars():
    """Возвращает список машин через запятую"""
    return ", ".join(cars)

@app.route('/cats')
def get_cats():
    """Возвращает случайную породу кошек из списка"""
    return random.choice(cat_breeds)

@app.route('/get_time/now')
def get_time_now():
    """Возвращает текущее время"""
    current_time = datetime.datetime.now()
    return f"Точное время: {current_time}"

@app.route('/get_time/future')
def get_time_future():
    """Возвращает время через час"""
    current_time = datetime.datetime.now()
    future_time = current_time + datetime.timedelta(hours=1)
    return f"Точное время через час будет {future_time}"

@app.route('/get_random_word')
def get_random_word():
    """Возвращает случайное слово из книги 'Война и мир'"""
    return random.choice(book_words)

@app.route('/counter')
def counter():
    """Счетчик просмотров страницы"""
    counter.visits += 1
    return f"Эта страница была открыта {counter.visits} раз"

# Инициализация счетчика
counter.visits = 0

if __name__ == '__main__':
    app.run(debug=True)