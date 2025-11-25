import datetime
import random
from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

cookies = {
    'SCBFormsAlreadyPulled': 'true',
    'scbsid_old': '2746015342',
    '_ym_uid': '1763362494731409257',
    '_ym_d': '1763362494',
    '_ym_isad': '2',
    'tmr_lvid': 'dc3d52552d41c0b1486b74d1657df709',
    'tmr_lvidTS': '1763362494922',
    'domain_sid': 'HXSNT6SbUMX5m3M_z0J3F%3A1763362495693',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%224e06371f7d7a2cb29802589f261a1f8a%22%5D',
    'flomni_641ae9eee9a473ff3717a7c0': '{%22userHash%22:%22922aef0f-5cfb-4594-ad06-d9ca5e4ef0e6%22}',
    '_cmg_csstGoGam': '1763368201',
    '_comagic_idGoGam': '11633662251.16060834806.1763368201',
    'SCBporogAct': '5000',
    'sma_session_id': '2499336757',
    'SCBfrom': 'https%3A%2F%2Faprelevka.fskfamily.ru%2F%3Futm_source%3Dyandex%26utm_medium%3Dcpc%26utm_campaign%3Dmg_ya_srch_aprelevka-club_brand_mmo%7Ccid%3A703731572%26utm_content%3Dcid%3A703731572%7Cre%3A205655441884%7Cgid%3A5655441884%7Cadid%3A17326177838%7Cdrf%3Ano%7Cst%3Asearch%7Cs%3Anone%7Cp%3A1%7Cpt%3Apremium%7Cdt%3Adesktop%7Ckw_id%3A205655441884%7Caudid%3A0%7Cgeo%3A162046%7Cbr_v1_utp%3Astart-prodazh%26utm_term%3D---autotargeting%26yclid%3D11419853193726394367',
    'PHPSESSID': '7vUa99bn5L7FcfPpv9w54zwrJwXxifdg',
    '_ym_visorc': 'w',
    'SCBstart': '1763370023580',
    'sma_postview_ready': '1',
    'tmr_detect': '0%7C1763370037572',
    'SCBindexAct': '4999',
    'sma_index_activity': '4392',
}

headers = {
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://aprelevka.fskfamily.ru/kvartiry/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'SCBFormsAlreadyPulled=true; scbsid_old=2746015342; _ym_uid=1763362494731409257; _ym_d=1763362494; _ym_isad=2; tmr_lvid=dc3d52552d41c0b1486b74d1657df709; tmr_lvidTS=1763362494922; domain_sid=HXSNT6SbUMX5m3M_z0J3F%3A1763362495693; SCBnotShow=-1; smFpId_old_values=%5B%224e06371f7d7a2cb29802589f261a1f8a%22%5D; flomni_641ae9eee9a473ff3717a7c0={%22userHash%22:%22922aef0f-5cfb-4594-ad06-d9ca5e4ef0e6%22}; _cmg_csstGoGam=1763368201; _comagic_idGoGam=11633662251.16060834806.1763368201; SCBporogAct=5000; sma_session_id=2499336757; SCBfrom=https%3A%2F%2Faprelevka.fskfamily.ru%2F%3Futm_source%3Dyandex%26utm_medium%3Dcpc%26utm_campaign%3Dmg_ya_srch_aprelevka-club_brand_mmo%7Ccid%3A703731572%26utm_content%3Dcid%3A703731572%7Cre%3A205655441884%7Cgid%3A5655441884%7Cadid%3A17326177838%7Cdrf%3Ano%7Cst%3Asearch%7Cs%3Anone%7Cp%3A1%7Cpt%3Apremium%7Cdt%3Adesktop%7Ckw_id%3A205655441884%7Caudid%3A0%7Cgeo%3A162046%7Cbr_v1_utp%3Astart-prodazh%26utm_term%3D---autotargeting%26yclid%3D11419853193726394367; PHPSESSID=7vUa99bn5L7FcfPpv9w54zwrJwXxifdg; _ym_visorc=w; SCBstart=1763370023580; sma_postview_ready=1; tmr_detect=0%7C1763370037572; SCBindexAct=4999; sma_index_activity=4392',
}

params = {
    'PAGEN_1': '1',
}

flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s






web_site = f'https://aprelevka.fskfamily.ru/kvartiry/'
driver = webdriver.Chrome()
driver.get(url=web_site)
time.sleep(9)

while True:
    try:
        # Ищем кнопку КАЖДЫЙ раз заново (важно!)
        btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-pagination-action="show-more"]'))
        )

        # Прокручиваем к кнопке — обязательно!
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)

        # Ждём кликабельности
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-pagination-action="show-more"]'))
        )

        # Пробуем кликнуть через JS
        driver.execute_script("arguments[0].click();", btn)

        time.sleep(1.5)  # ждём подгрузку

    except StaleElementReferenceException:
        # элемент пропал и перерисовался — просто повторяем цикл
        print("Элемент устарел → обновляем ссылку и продолжаем...")
        time.sleep(1)
        continue

    except TimeoutException:
        print("Кнопки больше нет — всё загружено.")
        break

page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript

soup = BeautifulSoup(page_content, 'html.parser')
items = soup.find_all('a', class_='cards-item')

print(len(items))

for i in items:

    url = ''
    developer = "ФСК"
    project = 'Апрелевка Клаб'
    korpus = i.find('div', class_='cards-item__amount').text.strip().split()[-1]
    section = ''
    type = 'Квартиры'
    finish_type = 'Без отделки'
    room_count_finding = i.find_all('div', class_=['cards-item__info-item', 'cards-item__rooms'])
    room_count_list = []
    for r in room_count_finding:
        room_count_list.append(r.text.strip().split())
    room_count = room_count_list[1][0]
    flat_number = ''
    try:
        area = float(room_count_list[2][0].replace(',', '.'))
    except:
        area = ''
    try:
        old_price = int(i.find('div', class_='cards-item__price-current').text.strip().replace(' ', '').replace('р.', ''))
        print(old_price)
    except:
        old_price = ''
    try:
        price = int()
    except:
        price = ''
    try:
        floor = int()
    except:
        floor = ''


    english = ''
    promzona = ''
    mestopolozhenie = ''
    subway = ''
    distance_to_subway = ''
    time_to_subway = ''
    mck = ''
    distance_to_mck = ''
    time_to_mck = ''
    bkl = ''
    distance_to_bkl = ''
    time_to_bkl = ''
    status = ''
    start = ''
    comment = ''
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    price_per_metr = ''
    discount = ''
    price_per_metr_new = ''


    print(
        f"{project}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)

save_flats_to_excel(flats, project, developer)



