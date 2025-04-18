"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""


def get_summary_rss(ps_output_file_path: str) -> str:
    # Читаем файл и пропускаем первую строку с заголовками
    with open(ps_output_file_path, 'r') as file:
        lines = file.readlines()[1:]

    total_rss = 0

    # Суммируем значения в столбце RSS
    for line in lines:
        columns = line.split()
        # RSS находится в 6-м столбце (индекс 5)
        total_rss += int(columns[5])

    # Переводим в человекочитаемый формат
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']
    unit_index = 0

    # Переводим в более крупные единицы измерения
    while total_rss >= 1024 and unit_index < len(units) - 1:
        total_rss /= 1024
        unit_index += 1

    # Форматируем результат: два знака после запятой и единица измерения
    return f"{total_rss:.2f} {units[unit_index]}"


if __name__ == '__main__':
    # Путь к файлу вынесен в отдельную переменную
    # Используем абсолютный путь относительно текущей директории скрипта
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path: str = os.path.join(current_dir, 'output_file.txt')

    # Если файл не существует, создаем его
    if not os.path.exists(path):
        print(f"Файл {path} не найден. Пожалуйста, создайте его командой:")
        print(f"ps aux > {path}")
        exit(1)

    summary_rss: str = get_summary_rss(path)
    print(summary_rss)