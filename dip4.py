from selenium import webdriver
import time
import random

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Опции браузера
options = webdriver.ChromeOptions()
options.add_argument(
    "--disable-blink-features=AutomationControlled")  # Отключение автоматического определения бот-активности
options.add_argument("--start-maximized")  # Запуск браузера в полноэкранном режиме

# Инициализация браузера
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def add_to_cart_test():
    driver.get("https://www.cd.cz/fanshop/")

    time.sleep(3)
    # Согласие с куки
    try:
        coockie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='dm-cookie-popup-accept-cookies']")))
        coockie_btn.click()
    except TimeoutException:
        print("Куки уже приняты или кнопка не найдена.")
        time.sleep(3)

    try:
        categories = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@class="nav-item parent dropdown leo-1"]')))

        if categories:
            random_category = random.choice(categories)
            random_category.click()
            print("Перешли в рандомную категорию.")
        else:
            print("Категории не найдены.")
            driver.quit()
            return

        added_products = 0
        total_product_count = 5


        time.sleep(3)

        while added_products < total_product_count:
            add_to_cards_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//span[@class="leo-bt-cart-content"]'))
            )

            for add_to_card_button in add_to_cards_buttons:
                if added_products >= total_product_count:
                    break

                try:
                    time.sleep(1)
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",
                                          add_to_card_button)  # Прокрутка
                    driver.execute_script("arguments[0].click();", add_to_card_button)  # Фокусировка
                    time.sleep(3)


                    added_products += 1
                except Exception:
                    continue

        print(f"Тест завершён: добавлено {added_products} товаров в корзину.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        driver.quit()

add_to_cart_test()