import allure
from conftest import login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.suite("Успешные сценарии")
@allure.title("Тест на успешную покупку")
@allure.severity(allure.severity_level.BLOCKER)
@allure.label("owner", "Oleg Stolyarchuk")
class TestSuccessfulPurchase:

    @allure.step("Полный цикл покупки: от авторизации до подтверждения заказа")
    def test_successful_purchase(self, driver):
        login(driver, "standard_user", "secret_sauce")

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

        with allure.step("Добавляем товар в корзину"):
            driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))

        with allure.step("Переходим в корзину"):
            driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']").click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

        with allure.step("Оформляем покупку"):
            driver.find_element(By.XPATH, "//button[@id='checkout']").click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "first-name")))

        with allure.step("Заполняем данные покупателя"):
            driver.find_element(By.ID, "first-name").send_keys("Test")
            driver.find_element(By.ID, "last-name").send_keys("User")
            driver.find_element(By.ID, "postal-code").send_keys("12345")

        with allure.step("Переходим к обзору заказа"):
            driver.find_element(By.ID, "continue").click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "finish")))

        with allure.step("Завершаем покупку"):
            driver.find_element(By.ID, "finish").click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))

        with allure.step("Проверяем сообщение об успешной покупке"):
            success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
            assert "Thank you for your order" in success_message