import allure
from conftest import login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.suite("Сценарии с корзиной")
@allure.title("Тест на очищение корзины")
@allure.severity(allure.severity_level.NORMAL)
@allure.label("owner", "Oleg Stolyarchuk")
class TestCleanCart:

    @allure.step("Добавляем товар, очищаем корзину и возвращаемся на каталог")
    def test_clean_cart(self, driver):
        login(driver, "standard_user", "secret_sauce")

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

        with allure.step("Добавляем товар в корзину"):
            driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))

        with allure.step("Открываем корзину"):
            driver.find_element(By.XPATH, "//a[@class='shopping_cart_link']").click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_item")))

        with allure.step("Удаляем товар из корзины"):
            driver.find_element(By.XPATH, "//button[text()='Remove']").click()
            WebDriverWait(driver, 30).until(EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))

        with allure.step("Возвращаемся на страницу каталога"):
            driver.find_element(By.XPATH, "//button[@id='continue-shopping']").click()
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

        with allure.step("Проверяем, что мы на странице Products"):
            title = driver.find_element(By.CLASS_NAME, "title").text
            assert title == "Products"