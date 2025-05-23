from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from config import URL


driver = webdriver.Chrome()
driver.get(URL)
wait = WebDriverWait(driver, 10)
driver.find_element(By.ID, 'consentBtnall').click()

time.sleep(3)

from_input = driver.find_element(By.ID, "connection-from")
from_input.send_keys("Ostrava")

to_input = driver.find_element(By.ID, "connection-to")
to_input.send_keys("Karlovy Vary")



calendar_input = wait.until(EC.element_to_be_clickable((By.NAME, "calendar")))
calendar_input.click()
date_input = wait.until(EC.presence_of_element_located((By.NAME, "calendar")))
date_input.clear()
date_input.send_keys("18/06/2025")
date_input.send_keys(Keys.TAB)

time_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.timepicker")))
time_input.clear()
time_input.send_keys("15:30")
time_input.send_keys(Keys.TAB)




search_button = driver.find_element(By.CLASS_NAME, "btn.btn--filled.btn--green.btn--with-icon.search-btn")
search_button.click()

time.sleep(5)

routes = driver.find_elements(By.CLASS_NAME, "overview-connection")

if routes:
    print(f"Найдено маршрутов: {len(routes)}")


    first_route = routes[0].text
    print("Первый маршрут:", first_route)


    if "přestup" in first_route.lower():
        print("Маршрут с пересадкой!")
    else:
        print("Прямой маршрут!")

else:
    print("Маршруты не найдены.")

driver.quit()
