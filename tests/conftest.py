import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Импортируем локаторы из папки selenium_tests/locators
from selenium_tests.locators.login_page_locators import LoginPageLocators


@pytest.fixture
def driver():
    """Фикстура для создания и закрытия браузера с отключенным Google Password Manager."""
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


def login(driver, username, password):
    """Функция для авторизации на сайте, используется во многих тестах."""
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(LoginPageLocators.USERNAME_INPUT))
    driver.find_element(*LoginPageLocators.USERNAME_INPUT).send_keys(username)
    driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(password)
    driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()