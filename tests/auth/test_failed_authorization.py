import allure
from conftest import login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_tests.locators.login_page_locators import LoginPageLocators


@allure.suite("Негативные сценарии")
@allure.title("Тест на неуспешную авторизацию")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "Oleg Stolyarchuk")
class TestFailedAuthorization:

    @allure.step("Вводим неверные данные и проверяем сообщение об ошибке")
    def test_failed_authorization(self, driver):
        login(driver, "invalid_user", "wrong_password")

        with allure.step("Проверка появления сообщения об ошибке"):
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located(LoginPageLocators.ERROR_MESSAGE))

        with allure.step("Проверка текста ошибки"):
            error_message = driver.find_element(*LoginPageLocators.ERROR_MESSAGE)
            assert "Username and password do not match" in error_message.text