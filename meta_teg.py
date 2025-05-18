from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config import URL
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument(
    "--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")



driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def check_og_tags():
    og_props = ["og:title", "og:description", "og:image"]
    for prop in og_props:
        try:
            meta = driver.find_element(By.CSS_SELECTOR, f'meta[property="{prop}"]')
            content = meta.get_attribute("content")
            print(f" Найден {prop}: {content}")
        except NoSuchElementException:
            print(f" META-тег {prop} не найден на странице")


driver.get(URL)
check_og_tags()