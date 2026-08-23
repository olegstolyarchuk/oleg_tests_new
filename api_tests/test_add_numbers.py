import pytest

# Метод сложения
def add_numbers(*args):
    """Складывает любое количество чисел."""
    return sum(args)

# Фикстура с параметризацией
@pytest.fixture(params=[
    (2, 3),  # Простые положительные числа
    (-5, 10, -2),  # Числа с разными знаками
    (0, 0),  # Нули
    (1.5, 2.5, 4)  # Добавил плавающие точки
])

# Фикстура
def numbers_fixture(request):
    """Фикстура возвращает наборы чисел для тестирования."""
    return request.param

# Тесты, использующие фикстуру
def test_add_positive_numbers(numbers_fixture):
    """Тест проверяет сложение нескольких наборов чисел."""
    numbers = numbers_fixture
    result = add_numbers(*numbers)

    # Вычисляем ожидаемый результат через обычный sum для сравнения
    expected = sum(numbers)

    # Обработка ошибки
    assert result == expected, f"Ошибка: {numbers} должно быть равно {expected}"

# Тест на проверку конкретного примера из задания (два простых числа)
def test_two_simple_numbers():
    assert add_numbers(2, 3) == 5

@pytest.mark.parametrize("num1, num2", [(5, 7), (10, -3)])
def test_parametrize_example(num1, num2):
    assert add_numbers(num1, num2) == num1 + num2