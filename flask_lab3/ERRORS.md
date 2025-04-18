# Ошибки в классе Person

В ходе тестирования класса `Person` были обнаружены следующие ошибки:

## 1. Ошибка в методе `get_age`

### Исходный код
```python
def get_age(self):
    now = datetime.datetime.now()
    return self.yob - now.year
```

### Проблема
Неправильный расчет возраста. Вычитается текущий год из года рождения, что дает отрицательное число.

### Исправление
```python
def get_age(self):
    now = datetime.datetime.now()
    return now.year - self.yob
```

### Объяснение
Для вычисления возраста человека нужно вычитать год рождения из текущего года, а не наоборот.

## 2. Ошибка в методе `set_name`

### Исходный код
```python
def set_name(self, name):
    self.name = self.name
```

### Проблема
Метод не обновляет атрибут `name`. Он просто присваивает текущее имя самому себе.

### Исправление
```python
def set_name(self, name):
    self.name = name
```

### Объяснение
Для установки нового имени нужно присвоить новое значение (параметр `name`) атрибуту `self.name`.

## 3. Ошибка в методе `set_address`

### Исходный код
```python
def set_address(self, address):
    self.address == address
```

### Проблема
Метод использует оператор сравнения (`==`) вместо оператора присваивания (`=`), поэтому не обновляет адрес.

### Исправление
```python
def set_address(self, address):
    self.address = address
```

### Объяснение
Оператор `==` используется для сравнения, возвращая булево значение. Для присваивания значения нужно использовать оператор `=`.

## 4. Ошибка в методе `is_homeless`

### Исходный код
```python
def is_homeless(self):
    '''
    returns True if address is not set, false in other case
    '''
    return address is None
```

### Проблема
Метод ссылается на неопределенную переменную `address` вместо атрибута экземпляра `self.address`. Также проверяется только случай, когда адрес равен `None`, но не учитывается пустая строка.

### Исправление
```python
def is_homeless(self):
    '''
    returns True if address is not set, false in other case
    '''
    return self.address is None or self.address == ''
```

### Объяснение
- Правильный атрибут для проверки - `self.address`, а не просто `address`.
- Согласно документации метода, он должен возвращать `True`, если адрес не установлен. Поскольку значение по умолчанию - пустая строка (`''`), нужно проверять как на `None`, так и на пустую строку.