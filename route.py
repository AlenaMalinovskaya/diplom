from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from config import URL

driver = webdriver.Chrome()

try:
    driver.get(URL)

    driver.find_element(By.ID, 'consentBtnall').click()
    time.sleep(3)


    from_input = driver.find_element(By.ID, "connection-from")
    from_input.send_keys("Plzen")


    to_input = driver.find_element(By.ID, "connection-to")
    to_input.send_keys("Ostrava")


    search_button = driver.find_element(By.CLASS_NAME, "btn.btn--filled.btn--green.btn--with-icon.search-btn")
    search_button.click()
    time.sleep(5)


    results = driver.find_elements(By.CLASS_NAME, "overview-schedule--simple")
    assert len(results) > 0, "Маршруты не найдены!"

    print("Тест успешен: маршруты найдены.")

finally:
    driver.quit()
