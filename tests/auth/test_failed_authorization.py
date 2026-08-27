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