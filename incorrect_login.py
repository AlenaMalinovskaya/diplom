import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from config import URL, correct_login, incorrect_password

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

def test_incorrect_login():
    try:
        driver.get(URL)

        wait.until(EC.element_to_be_clickable((By.ID, "consentBtnall"))).click()
        wait.until(EC.invisibility_of_element_located((By.ID, "consentBtnall")))

        login_buttons = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class,'userbox--toggle')]"))
        )

        visible_login_button = next((b for b in login_buttons if b.is_displayed()), None)

        if visible_login_button:
            actions = ActionChains(driver)
            actions.move_to_element(visible_login_button).perform()
            print("Навели на видимую кнопку входа")

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", visible_login_button)
            visible_login_button.click()
            print("Кликнули на Přihlásit se")
            time.sleep(3)

            email_field = wait.until(EC.visibility_of_element_located((By.ID, "emailld")))
            password_field = wait.until(EC.element_to_be_clickable((By.ID, "passwordld")))

            email_field.clear()
            email_field.send_keys(correct_login)
            print("Ввели email")

            password_field.clear()
            password_field.send_keys(incorrect_password)
            print("Ввели неправильный пароль")

            submit_buttons = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "button.btn.btn--blue.btn--filled.btn--full-width")
            ))

            submit_btn = next((b for b in submit_buttons if b.is_displayed()), None)

            if submit_btn:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                driver.execute_script("arguments[0].click();", submit_btn)
                print(" Клик по кнопке 'Přihlásit' выполнен")
                time.sleep(3)
            else:
                print(" Кнопка отправки входа не найдена!")


        parts = ['nesprávný', 'příliš velkého', 'uzamčen']
        xpath = "//*[" + " or ".join([f"contains(text(), '{p}')" for p in parts]) + "]"
        error_blocks = driver.find_elements(By.XPATH, xpath)

        print(f" Всего найдено элементов с ошибками: {len(error_blocks)}")
        for block in error_blocks:
            print("-", repr(block.text))

        expected_errors = [
            "Zadali jste nesprávný e-mail nebo heslo.",
            "Z důvodu příliš velkého počtu chybných přihlášení byl účet uzamčen na 60 minut."
        ]

        found = False
        for block in error_blocks:
            text = block.text.strip()
            for expected in expected_errors:
                if expected in text and block.is_displayed():
                    found = True
                    print(" Найдено сообщение об ошибке:", expected)
                    break

        if not found:
            driver.save_screenshot("error_screen.png")
            print(" Скриншот сохранён: error_screen.png")

        assert found, " Ни одно из ожидаемых сообщений об ошибке не найдено!"

    except Exception as e:
        print(f" Ошибка во время выполнения теста: {e}")
    finally:
        driver.quit()
