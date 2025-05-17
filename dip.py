from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Открываем браузер
driver = webdriver.Chrome()

try:
    driver.get("https://www.cd.cz/")  # Открываем сайт

    # Согласие с куки, кликаем на кнопку для подтверждения
    driver.find_element(By.ID, 'consentBtnall').click()
    time.sleep(3)

    # Ввод станции отправления
    from_input = driver.find_element(By.ID, "connection-from")  # Заменить на правильный ID
    from_input.send_keys("Praha")

    # Ввод станции назначения
    to_input = driver.find_element(By.ID, "connection-to")  # Заменить на правильный ID
    to_input.send_keys("Brno")

    # Подтверждение поиска
    # to_input.send_keys(Keys.RETURN)
    search_button = driver.find_element(By.CLASS_NAME, "btn.btn--filled.btn--green.btn--with-icon.search-btn")  # Заменить на правильный ID
    search_button.click()
    time.sleep(5)  # Ждем загрузки результатов

    # Проверяем, появились ли маршруты
    results = driver.find_elements(By.CLASS_NAME, "overview-schedule--simple")  # Заменить на правильный класс
    assert len(results) > 0, "Маршруты не найдены!"

    print("Тест успешен: маршруты найдены.")

finally:
    driver.quit()
