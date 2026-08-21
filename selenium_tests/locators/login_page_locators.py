from selenium.webdriver.common.by import By

class LoginPageLocators:
    # Локаторы для страницы авторизации (https://www.saucedemo.com/)

    # Поле ввода логина (input id="user-name")
    USERNAME_INPUT = (By.ID, "user-name")

    # Поле ввода пароля (input id="password")
    PASSWORD_INPUT = (By.ID, "password")

    # Кнопка входа (input id="login-button")
    LOGIN_BUTTON = (By.ID, "login-button")

    # Красная плашка с ошибкой (h3 data-test="error")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")