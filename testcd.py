import pytest                                   # Подключаем фреймворк для запуска тестов
import time                                     # Для паузы после действий (на случай анимаций/задержек)
from selenium import webdriver                  # Браузерный драйвер
from selenium.webdriver.chrome.service import Service  # Сервис для управления ChromeDriver
from selenium.webdriver.chrome.options import Options  # Настройки браузера Chrome
from selenium.webdriver.common.by import By     # Для поиска элементов на странице
from selenium.webdriver.support.ui import WebDriverWait         # Ожидания элементов
from selenium.webdriver.support import expected_conditions as EC  # Условия для ожидания
from selenium.webdriver.common.action_chains import ActionChains  # Для наведения курсора
from webdriver_manager.chrome import ChromeDriverManager         # Установка ChromeDriver автоматически
from config import URL, correct_login, incorrect_password        # Конфигурационные данные из файла config.py

@pytest.fixture
def driver():
    options = Options()                                      # Создаём объект опций для Chrome
    options.add_argument("--start-maximized")                # Запуск браузера в развернутом виде
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  # Инициализация драйвера
    yield driver                                             # Возвращаем драйвер в тест
    driver.quit()                                            # После теста закрываем браузер

def test_incorrect_login(driver):
    wait = WebDriverWait(driver, 10)                         # Явное ожидание до 10 секунд
    driver.get(URL)                                          # Открытие нужной страницы сайта

    # Принятие cookies, если кнопка есть
    wait.until(EC.element_to_be_clickable((By.ID, "consentBtnall"))).click()      # Ждём и кликаем на кнопку согласия
    wait.until(EC.invisibility_of_element_located((By.ID, "consentBtnall")))      # Ждём исчезновения баннера

    # Поиск кнопки входа
    login_buttons = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class,'userbox--toggle')]"))  # Находим все кнопки входа
    )
    visible_login_button = next((btn for btn in login_buttons if btn.is_displayed()), None)  # Берём первую видимую кнопку
    assert visible_login_button, "❌ Кнопка входа не найдена"                                 # Проверка: кнопка найдена

    ActionChains(driver).move_to_element(visible_login_button).perform()                     # Наводим курсор на кнопку
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", visible_login_button)  # Скроллим к кнопке
    visible_login_button.click()                                                             # Кликаем по кнопке

    # Вводим логин и пароль
    email_field = wait.until(EC.visibility_of_element_located((By.ID, "emailld")))           # Ждём появления поля email
    password_field = wait.until(EC.element_to_be_clickable((By.ID, "passwordld")))           # Ждём кликабельность поля пароля
    email_field.clear()                                                                      # Очищаем поле email
    email_field.send_keys(correct_login)                                                     # Вводим email
    password_field.clear()                                                                   # Очищаем поле пароля
    password_field.send_keys(incorrect_password)                                             # Вводим заведомо неверный пароль

    # Поиск и нажатие на кнопку "Přihlásit"
    submit_buttons = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "button.btn.btn--blue.btn--filled.btn--full-width")                # Ищем все кнопки входа
    ))
    submit_btn = next((btn for btn in submit_buttons if btn.is_displayed()), None)           # Берём первую видимую
    assert submit_btn, "❌ Кнопка 'Přihlásit' не найдена"                                     # Проверяем, что она есть

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)     # Скроллим к кнопке
    driver.execute_script("arguments[0].click();", submit_btn)                               # Кликаем через JavaScript

    time.sleep(2)  # Делаем небольшую паузу, чтобы ошибка успела отобразиться

    # Собираем все элементы, содержащие возможные фразы ошибки
    parts = ['nesprávný', 'příliš velkého', 'uzamčen']                                       # Части слов, по которым ищем ошибку
    xpath = "//*[" + " or ".join([f"contains(text(), '{p}')" for p in parts]) + "]"          # Динамически формируем XPath
    error_blocks = driver.find_elements(By.XPATH, xpath)                                     # Находим все подходящие блоки
    print(f"🔎 Всего найдено элементов с 'nesprávný': {len(error_blocks)}")                  # Выводим количество найденных
    for block in error_blocks:
        print("-", repr(block.text))                                                         # Печатаем текст каждого

    # Список возможных ожидаемых сообщений
    expected_errors = [
        "Zadali jste nesprávný e-mail nebo heslo.",                                           # Ошибка при неправильных данных
        "Z důvodu příliš velkého počtu chybných přihlášení byl účet uzamčen na 60 minut."     # Ошибка при блокировке аккаунта
    ]

    found = False                                                                             # Флаг, нашли ли ошибку
    for block in error_blocks:
        text = block.text.strip()                                                             # Получаем текст блока
        for expected in expected_errors:
            if expected in text and block.is_displayed():                                     # Сравниваем с ожидаемыми
                found = True
                print("✅ Найдено сообщение об ошибке:", expected)                            # Успех — сообщение найдено
                break

    if not found:
        driver.save_screenshot("error_screen.png")                                            # Если ничего не найдено — делаем скрин
        print("📸 Скриншот сохранён: error_screen.png")

    assert found, "❌ Ни одно из ожидаемых сообщений об ошибке не найдено!"                   # Итоговая проверка теста
