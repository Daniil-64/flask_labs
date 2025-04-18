"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: str) -> float:
    """
    Вычисляет средний размер файлов на основе вывода команды ls -l

    Args:
        ls_output (str): Результат выполнения команды ls -l

    Returns:
        float: Средний размер файлов в байтах или 0.0, если файлов нет
    """
    lines = ls_output.strip().split('\n')

    # Пропускаем заголовок (первую строку)
    if lines and lines[0].startswith('total'):
        lines = lines[1:]

    file_sizes = []

    # Извлекаем размеры файлов
    for line in lines:
        if not line.strip():
            continue

        parts = line.split()

        # Проверяем, что строка содержит достаточно полей и это обычный файл
        # Формат ls -l:
        # права_доступа кол-во_ссылок владелец группа размер месяц день время_или_год имя
        if len(parts) >= 5:
            # Проверяем первый символ прав доступа: '-' для обычных файлов
            if parts[0][0] == '-':
                try:
                    # Размер файла находится в 5-м столбце (индекс 4)
                    file_size = int(parts[4])
                    file_sizes.append(file_size)
                except (ValueError, IndexError):
                    pass

    # Вычисляем средний размер
    if file_sizes:
        return sum(file_sizes) / len(file_sizes)
    else:
        return 0.0  # Если нет файлов или не удалось получить их размер


if __name__ == '__main__':
    data: str = sys.stdin.read()
    mean_size: float = get_mean_size(data)
    print(f"Средний размер файла: {mean_size:.2f} байт")