import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from parsing.modules.str_int_phone import extract_digits
from parsing.rest_api.api import send_message


def init_driver(proxy=None):
    options_chrome = uc.ChromeOptions()
    # options_chrome.add_argument("--window-position=-32000,-32000")
    if proxy is not None:
        options_chrome.add_argument(
            f"--proxy-server={proxy['type']}://{proxy['ip']}:{proxy['port']}")

    driver = uc.Chrome(
        driver_executable_path='chrome_windows/chromedriver-win64/chromedriver.exe',
        browser_executable_path='chrome_windows/chrome-win64/chrome.exe',
        options=options_chrome,
        use_subprocess=True,
        version_main=131,
        headless=False,
    )
    return driver


def login():
    coocs = []
    driver = init_driver()
    driver.get(url='https://smartagent.ru/')
    time.sleep(20)
    for i in driver.get_cookies():
        coocs.append(i)
    driver.quit()

    return coocs


def pagination(driver, ads, processed_ids, collected_data, message: str, instance_id, access_token):
    """
    Обработка списка объявлений с пропуском уже обработанных
    """
    for ad in ads:
        try:
            # Получаем ID объявления
            ad_id = ad.get_attribute('id')

            # Пропускаем уже обработанные объявления
            if ad_id in processed_ids:
                continue

            processed_ids.add(ad_id)
            print(f"\nОбработка объявления {ad_id}")

            # Проверяем наличие иконки проверенного телефона
            verified_icons = ad.find_elements(
                By.CSS_SELECTOR, 'i[data-hint="Прямой проверенный телефон"]')
            if not verified_icons:
                print("Пропускаем: нет иконки проверенного телефона")
                continue

            print("Найден проверенный телефон")

            # Проверяем наличие нужной кнопки
            phone_buttons = ad.find_elements(
                By.CSS_SELECTOR, 'div.v-ad-phone__pane.trigger button.l.l_dashed.l_blue')
            if not phone_buttons:
                print("Пропускаем: нет кнопки нужной структуры")
                continue

            phone_button = phone_buttons[0]
            if not (phone_button.is_displayed() and phone_button.is_enabled()):
                print("Пропускаем: кнопка не активна или не видима")
                continue

            # Собираем информацию об объявлении
            ad_info = {}

            # Прокручиваем к кнопке
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", phone_button)
            time.sleep(random.uniform(1, 2))

            # Проверяем, что кнопка все еще существует и доступна
            try:
                WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'div.v-ad-phone__pane.trigger button.l.l_dashed.l_blue'))
                )
            except:
                print("Кнопка стала недоступна после прокрутки")
                continue

            # Кликаем на кнопку
            print("Кликаем на кнопку показа телефона...")
            ActionChains(driver).move_to_element(
                phone_button).click().perform()
            time.sleep(random.uniform(2, 3))

            selectors = [
                'call-call-plugin',  # Новая структура
                # 'button.v-ad-number__trigger call-call-plugin',  # Альтернативный вариант
                # '.v-ad-number__trigger call-call-plugin'  # Еще один вариант
            ]

            for selector in selectors:
                try:
                    phone_element = ad.find_element(By.CSS_SELECTOR, selector)
                    phone = phone_element.text.strip()
                    if phone and not phone.startswith('+7 (ххх)'):
                        phone_int = extract_digits(phone)
                        print(phone_int)
                        send = send_message(
                            phone_number=phone_int, message=message, instance_id=instance_id, access_token=access_token)
                        print(send)
                        collected_data.append(phone_int)
                except:
                    continue

            time.sleep(random.uniform(1, 2))

        except Exception as e:
            print(f"Ошибка при обработке объявления: {str(e)}")
            continue


def get_phones_with_scroll(url, cookies, message, instance_id, access_token, limit_phone=10):
    """
    Функция для получения телефонов с поддержкой бесконечного скроллинга
    """

    driver = init_driver()

    collected_data = []
    processed_ids = set()  # Множество для хранения обработанных ID объявлений

    # Устанавливаем куки
    driver.get(url='https://smartagent.ru/')
    for i in cookies:
        driver.add_cookie(i)

    driver.get(url)
    time.sleep(3)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Получаем текущие объявления
        ads = driver.find_elements(By.CSS_SELECTOR, 'section.v-preview-ad')
        print(f"\nНайдено объявлений: {len(ads)}")

        # Обрабатываем текущие объявления
        pagination(driver, ads, processed_ids, collected_data,
                   message, instance_id, access_token)

        # Скроллим вниз
        print("\nСкроллим страницу вниз...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(random.uniform(5, 8))  # Ждем загрузки новых объявлений

        # Проверяем, изменилась ли высота страницы
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Достигнут конец страницы")
            break

        last_height = new_height

        # Дополнительная проверка лимита
        if len(collected_data) >= int(limit_phone):
            print(f"Достигнут лимит в {limit_phone} номеров")
            break

    return collected_data


def save_phones(phones, filename='phones.txt'):
    """
    Сохраняет телефоны в файл
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for item in phones:
            if 'phone' in item:
                f.write(f"{item['phone']}\n")
    print(f"Сохранено {len(phones)} телефонов в файл {filename}")


