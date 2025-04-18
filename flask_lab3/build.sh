#!/bin/bash

# Скрипт для запуска статического анализа и тестов программы дешифратора

# Определение переменных
PYTHON_FILE="decrypt.py"
TEST_FILE="test_decrypt.py"
JSON_OUTPUT="pylint_report.json"
REQUIRED_SCORE=7.0  # Минимальный проходной балл для pylint

echo "==============================================="
echo "Начало проверки программы $PYTHON_FILE"
echo "==============================================="

# Шаг 1: Запуск pylint для статического анализа кода
echo "1. Запуск статического анализа кода (pylint)..."
echo "-----------------------------------------------"

pylint "$PYTHON_FILE" --output-format=json:"$JSON_OUTPUT",colorized --reports=y --score=y

# Сохраняем код возврата pylint
PYLINT_RESULT=$?

# Определение статуса на основе кода возврата
if [[ $PYLINT_RESULT -eq 0 ]]; then
    PYLINT_STATUS="OK"
elif [[ $PYLINT_RESULT -eq 1 ]]; then
    PYLINT_STATUS="ПРЕДУПРЕЖДЕНИЕ: Выдано критическое сообщение"
elif [[ $PYLINT_RESULT -eq 2 ]]; then
    PYLINT_STATUS="ОШИБКА: Выдано сообщение об ошибке"
elif [[ $PYLINT_RESULT -eq 4 ]]; then
    PYLINT_STATUS="ОШИБКА: Произошла критическая ошибка"
elif [[ $PYLINT_RESULT -eq 8 ]]; then
    PYLINT_STATUS="ОШИБКА: Модуль не удалось проверить"
elif [[ $PYLINT_RESULT -eq 16 ]]; then
    PYLINT_STATUS="ОШИБКА: Ошибка использования"
elif [[ $PYLINT_RESULT -eq 32 ]]; then
    PYLINT_STATUS="ОШИБКА: Использование неподдерживаемого параметра"
else
    PYLINT_STATUS="НЕИЗВЕСТНЫЙ РЕЗУЛЬТАТ ($PYLINT_RESULT)"
fi

echo "Результат статического анализа: $PYLINT_STATUS"
echo "Отчет pylint сохранен в файл $JSON_OUTPUT"
echo ""

# Шаг 2: Запуск модульных тестов
echo "2. Запуск модульных тестов..."
echo "-----------------------------------------------"

python -m unittest "$TEST_FILE"

# Сохраняем код возврата модульных тестов
TEST_RESULT=$?

# Определение статуса на основе кода возврата
if [[ $TEST_RESULT -eq 0 ]]; then
    TEST_STATUS="OK"
else
    TEST_STATUS="ОШИБКА: Не все тесты пройдены"
fi

echo "Результат модульных тестов: $TEST_STATUS"
echo ""

# Шаг 3: Определение общего результата
echo "3. Общий результат..."
echo "-----------------------------------------------"

# Тесты считаются успешными, если pylint не выдал критических ошибок (код < 4)
# и все модульные тесты пройдены
if [[ $PYLINT_RESULT -lt 4 && $TEST_RESULT -eq 0 ]]; then
    echo "ОБЩИЙ РЕЗУЛЬТАТ: ОК"
    FINAL_STATUS=0
else
    echo "ОБЩИЙ РЕЗУЛЬТАТ: Имеются ошибки"
    FINAL_STATUS=1
fi

echo "==============================================="

# Возвращаем общий статус
exit $FINAL_STATUS