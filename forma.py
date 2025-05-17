import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service()  # Укажи путь к chromedriver, если он не в PATH
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_send_contact_form(driver):
    driver.get("https://www.cd.cz/fanshop/kontaktni-formular")

    wait = WebDriverWait(driver, 10)

    # Принятие cookie (если появляется)
    try:
        cookie_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='dm-cookie-popup-accept-cookies']"))
        )
        cookie_btn.click()
    except:
        print("Cookie кнопка не отображается или уже принята.")

    # Ввод email
    email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_input.clear()
    email_input.send_keys("test@example.com")

    # Ввод сообщения
    message_input = driver.find_element(By.ID, "contactform-message")
    message_input.send_keys("Toto je testovací zpráva pro odeslání přes Selenium.")

    # Отметить чекбокс согласия
    checkbox = driver.find_element(By.ID, "psgdpr_consent_checkbox_2")
    if not checkbox.is_selected():
        checkbox.click()

    # Отправить форму
    submit_btn = driver.find_element(By.XPATH, '//input[@value="Poslat"]')
    submit_btn.click()

    # Проверка успешной отправки (по тексту на странице или другому признаку)
    try:
        confirmation = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'úspěšně odeslán')]"))
        )
        assert "úspěšně odeslán" in confirmation.text.lower()

        print("✅ Форма успешно отправлена.")
    except Exception as e:
        driver.save_screenshot("form_error.png")
        pytest.fail(f"❌ Ошибка при проверке успешной отправки: {e}")


