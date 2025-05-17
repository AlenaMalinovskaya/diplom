from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Открываем браузер
driver = webdriver.Chrome()
driver.get("https://www.cd.cz/")  # Открываем сайт

# Согласие с куки, кликаем на кнопку для подтверждения
driver.find_element(By.ID, 'consentBtnall').click()

time.sleep(3)  # Ждем загрузки

# Ввод станции отправления
from_input = driver.find_element(By.ID, "connection-from")  # Заменить на правильный ID
from_input.send_keys("Praha")

# Ввод станции назначения
to_input = driver.find_element(By.ID, "connection-to")  # Заменить на правильный ID
to_input.send_keys("Plzen")
search_button = driver.find_element(By.CLASS_NAME, "btn.btn--filled.btn--green.btn--with-icon.search-btn")  # Заменить на правильный ID
search_button.click()

time.sleep(5)  # Ждем загрузки маршрутов

# Ищем список маршрутов
routes = driver.find_elements(By.CLASS_NAME, "overview-connection")  # Заменить на правильный класс

if routes:
    print(f"Найдено маршрутов: {len(routes)}")

    # Проверяем первый маршрут
    first_route = routes[0].text
    print("Первый маршрут:", first_route)

    # Проверяем, есть ли пересадка (например, ищем слово "přestup" (пересадка на чешском))
    if "přestup" in first_route.lower():
        print("Маршрут с пересадкой!")
    else:
        print("Прямой маршрут!")

else:
    print("Маршруты не найдены.")

driver.quit()
