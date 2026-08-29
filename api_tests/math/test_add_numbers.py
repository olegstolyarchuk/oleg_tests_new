import pytest

# 1. Метод сложения. Принимает любое количество чисел и складывает их.
def add_numbers(*args):
    """Складывает любое количество чисел."""
    return sum(args)

# 2. Фикстура с параметризацией. Она "подготавливает" данные для тестов.
@pytest.fixture(params=[
    (2, 3),       # Два простых положительных числа
    (-5, 10, -2), # Три числа с разными знаками
    (0, 0),       # Несколько чисел, включая нули
    (1.5, 2.5, 4) # Можно добавить плавающие точки (бонус)
])

def numbers_fixture(request):
    """Фикстура возвращает наборы чисел для тестирования."""
    return request.param

# 3. Тест, использующий фикстуру
def test_add_positive_numbers(numbers_fixture):
    """Тест проверяет сложение нескольких наборов чисел."""
    numbers = numbers_fixture
    result = add_numbers(*numbers)
    # Вычисляем ожидаемый результат для сравнения
    expected = sum(numbers)
    assert result == expected, f"Ошибка: {numbers} должно быть равно {expected}"

# 4. Тест на проверку конкретного примера из задания (два простых числа)
def test_two_simple_numbers():
    assert add_numbers(2, 3) == 5