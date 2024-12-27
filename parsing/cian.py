import multiprocessing
import time
import urllib.parse
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from undetected_chromedriver import By
from parsing.modules.str_int_phone import extract_digits
from parsing.modules.csv import append_to_csv
from parsing.rest_api.api import send_message
from parsing.modules.txt_read import read_text_file
from datetime import datetime


def init_driver(proxy=None):
    options_chrome = uc.ChromeOptions()
    options_chrome.add_argument("--window-position=-32000,-32000")
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


def pagination(link, base_url, result_queue):
    links = set()
    driver = init_driver()
    link_next = link

    while True:
        driver.get(link_next)
        time.sleep(10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        general = soup.find(
            'div', attrs={'data-name': 'SearchEngineResultsPage'})

        links_div = general.find('div', class_='_93444fe79c--wrapper--W0WqH')
        if links_div:
            articles = links_div.find_all(
                'article', attrs={'data-name': 'CardComponent'})
            for article in articles:
                a_tag = article.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    href = a_tag['href']
                    full_url = urllib.parse.urljoin(base_url, href)
                    links.add(full_url)

        pagination = general.find(
            'div', attrs={'data-name': 'PaginationSection'})
        if pagination:
            next_link = pagination.find('a', string='Дальше')
            if next_link and 'href' in next_link.attrs:
                link_next = urllib.parse.urljoin(base_url, next_link['href'])
                result_queue.put(links)
            else:
                break
        else:
            break

    driver.quit()


def parsing_info(links_queue, watsapp_tokens, text_message, time_start: dict):
    old_links = set()
    while True:
        try:
            now_time = datetime.now().hour
            if now_time >= int(time_start['start']) and now_time < int(time_start['end']):

                # Пытаемся получить ссылку без блокировки
                links = set(links_queue.get(block=False))
                for old in old_links:
                    links.discard(old)

                driver = init_driver()

                for link in links:
                    # Обработка ссылки
                    driver.get(link)
                    time.sleep(10)
                    try:
                        driver.find_element(
                            By.CSS_SELECTOR, 'button[class="a10a3f92e9--button--KVooB a10a3f92e9--button--gs5R_ a10a3f92e9--M--I5Xj6 a10a3f92e9--button--wvpRY a10a3f92e9--full-width--LjV3t"]').click()
                        time.sleep(6)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        general = soup.find(
                            'div', attrs={'id': 'frontend-offer-card'})
                        phone = general.find(
                            'div', attrs={'data-name': 'Phones'}).text
                        phone = extract_digits(phone)
                        old_links.add(link)

                        # Раскомментируйте следующие строки, если хотите отправлять сообщения
                        try:
                            send_message(phone_number=phone, message=text_message,
                                         instance_id=watsapp_tokens['instance_id'], access_token=watsapp_tokens['access_token'])
                        except Exception as e:
                            continue

                    except Exception as e:
                        continue

        except multiprocessing.queues.Empty:
            time.sleep(10)  # Ждем 5 секунд перед следующей попыткой

        except Exception as e:
            time.sleep(10)  # Ждем 5 секунд перед следующей попыткой


class Cian:
    def __init__(self, link: str, watsapp_tokens: dict, times: dict, text_message: str, proxy=None):
        self.link = link
        self.watsapp_tokens = watsapp_tokens
        self.text_message = read_text_file(text_message)
        self.base_url = 'https://www.cian.ru'
        self.proxy = proxy
        self.time = times

    def start_multiprocessing(self, pid):
        links_queue = multiprocessing.Queue()

        p1 = multiprocessing.Process(target=pagination, args=(
            self.link, self.base_url, links_queue))
        p2 = multiprocessing.Process(target=parsing_info, args=(
            links_queue, self.watsapp_tokens, self.text_message, self.time))

        p1.start()
        p2.start()

        pid.put([p1.pid, p2.pid])

        p1.join()
        p2.join()
