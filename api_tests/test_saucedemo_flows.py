import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==========================================
# БЛОК 1: ЛОКАТОРЫ (все в одном файле)
# ==========================================
class LoginPageLocators:
    """Класс для хранения локаторов элементов на странице авторизации."""
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

class InventoryPageLocators:
    """Класс для хранения локаторов элементов на странице каталога товаров."""
    PAGE_TITLE = (By.CLASS_NAME, "title")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.XPATH, "//a[@class='shopping_cart_link']")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    ADD_TO_CART_BUTTON = (By.XPATH, "//button[text()='Add to cart']")

# ==========================================
# БЛОК 2: ФИКСТУРА ДЛЯ ПОДГОТОВКИ БРАУЗЕРА
# ==========================================
@pytest.fixture
def driver():
    """
    Фикстура для создания и закрытия браузера.
    Включает настройки для отключения всплывающих окон Google Password Manager.
    """
    # Отключение Google Password Manager и всплывающих уведомлений
    options = webdriver.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-save-password-bubble")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

# ==========================================
# БЛОК 3: ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ АВТОРИЗАЦИИ
# ==========================================
def login(driver, username, password):
    """
    Выполняет вход на сайт SauceDemo.
    Открывает главную страницу, ожидает загрузки поля логина,
    вводит переданные логин и пароль и нажимает кнопку входа.
    """
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoginPageLocators.USERNAME_INPUT))
    driver.find_element(*LoginPageLocators.USERNAME_INPUT).send_keys(username)
    driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(password)
    driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

# ==========================================
# СЦЕНАРИЙ 1: Успешная покупка
# ==========================================
def test_successful_purchase(driver):
    """
    Проверка полного пути покупки:
    1. Авторизация
    2. Добавление товара в корзину
    3. Переход в корзину
    4. Оформление заказа (Checkout)
    5. Проверка успешного завершения
    """
    # 1. Авторизуемся на сайте с валидными учётными данными
    login(driver, "standard_user", "secret_sauce")

    # 2. Ожидаем загрузки страницы каталога
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

    # 3. Добавляем первый попавшийся товар в корзину
    driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()

    # 4. Ожидаем появления бейджа корзины
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))

    # 5. Переходим в корзину
    driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']").click()

    # 6. Ожидаем страницу корзины
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

    # 7. Оформить покупку: нажать Checkout
    driver.find_element(By.XPATH, "//button[@id='checkout']").click()

    # 8. Ожидаем страницу заполнения информации
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "first-name")))

    # 9. Заполняем поля формы
    driver.find_element(By.ID, "first-name").send_keys("Test")
    driver.find_element(By.ID, "last-name").send_keys("User")
    driver.find_element(By.ID, "postal-code").send_keys("12345")

    # 10. Нажимаем кнопку Continue
    driver.find_element(By.ID, "continue").click()

    # 11. Ожидаем страницу обзора заказа
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "finish")))

    # 12. Нажимаем кнопку Finish
    driver.find_element(By.ID, "finish").click()

    # 13. Ожидаем страницу завершения заказа
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))

    # 14. Проверяем сообщение об успехе (Assert)
    success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "Thank you for your order" in success_message, f"Ошибка: получено сообщение {success_message}"

# ==========================================
# СЦЕНАРИЙ 2: Очищение корзины
# ==========================================
def test_clean_cart(driver):
    """
    Проверка полного очищения корзины:
    1. Авторизация
    2. Добавление всех товаров
    3. Открытие корзины
    4. Удаление всех товаров
    5. Проверка, что корзина пуста
    6. Проверка, что вернулись на каталог
    """
    # 1. Авторизуемся
    login(driver, "standard_user", "secret_sauce")

    # 2. Ожидаем страницу каталога
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

    # 3. Добавляем первый товар
    driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))

    # 4. Открываем корзину
    driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']").click()

    # 5. Ожидаем страницу корзины (Your Cart)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

    # 6. Удаляем товар
    driver.find_element(By.XPATH, "//button[text()='Remove']").click()

    # 7. Проверяем, что корзина пуста (бейдж исчез)
    WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))

    # 8. Нажимаем кнопку Continue Shopping
    driver.find_element(By.XPATH, "//button[@id='continue-shopping']").click()

    # 9. Ожидаем страницу каталога
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

    # 10. Проверяем, что вернулись на страницу выбора товаров
    title = driver.find_element(By.CLASS_NAME, "title").text
    assert title == "Products", f"Ошибка: ожидался заголовок Products, получен {title}"

# ==========================================
# СЦЕНАРИЙ 3: Неуспешная авторизация
# ==========================================
def test_failed_authorization(driver):
    """
    Проверка негативного сценария:
    1. Попытка входа с неверными данными
    2. Проверка появления корректного сообщения об ошибке
    """
    # 1. Попытаемся войти с неправильными данными
    login(driver, "invalid_user", "wrong_password")

    # 2. Ожидаем появления плашки с ошибкой
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located(LoginPageLocators.ERROR_MESSAGE))

    # 3. Проверяем содержание сообщения об ошибке (Assert)
    error_message = driver.find_element(*LoginPageLocators.ERROR_MESSAGE)
    assert "Username and password do not match" in error_message.text, \
        f"Ошибка: текст ошибки не совпадает. Получено: {error_message.text}"