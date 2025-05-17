# Импортируем нужные модули для работы с браузером и веб-элементами
from selenium import webdriver
import time
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument(
    "--disable-blink-features=AutomationControlled")  # Отключение автоматического определения бот-активности
options.add_argument("--start-maximized")  # Запуск браузера в полноэкранном режиме



driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def check_og_tags():
    og_props = ["og:title", "og:description", "og:image"]
    for prop in og_props:
        try:
            meta = driver.find_element(By.CSS_SELECTOR, f'meta[property="{prop}"]')
            content = meta.get_attribute("content")
            print(f"✅ Найден {prop}: {content}")
        except NoSuchElementException:
            print(f"❌ META-тег {prop} не найден на странице")

# пример использования сразу после driver.get(URL)
driver.get("https://www.cd.cz")
check_og_tags()