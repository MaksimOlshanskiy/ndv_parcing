import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from functions import save_flats_to_excel
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException, NoSuchElementException

cookies = {
    'SCBFormsAlreadyPulled': 'true',
    'scbsid_old': '2746015342',
    '_ym_uid': '1756294367437085348',
    '_ym_d': '1764247193',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'smFpId_old_values': '%5B%225a4ba48b0c99505318ede61cd1067357%22%5D',
    'ced': '2k7csd5c5u0i8nb63v77odqprepd88l9',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_cssttGbx8': '1764592723',
    '_comagic_idtGbx8': '10113416032.14188502537.1764592723',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1764679123649%2C%22sl%22%3A%7B%22224%22%3A1764592723649%2C%221228%22%3A1764592723649%7D%7D',
    'adrdel': '1764592723989',
    'cookie': 'yes',
    'sma_session_id': '2517111582',
    'SCBfrom': 'https%3A%2F%2Fxn----7sbocpkbcearp8a9etgj.xn--p1ai%2F%3Futm_source%3Dyandex%26utm_medium%3Dcpc%26utm_campaign%3Dy_m108_lk_search_brand_mmo%7C702816452%26utm_term%3D%25D0%25BB%25D0%25B5%25D1%2581%25D0%25BD%25D0%25B0%25D1%258F%2520%25D0%25BA%25D0%25BE%25D0%25BB%25D0%25BB%25D0%25B5%25D0%25BA%25D1%2586%25D0%25B8%25D1%258F%26utm_content%3Dtext_3%7Cgid%7C5631389295%7Caid%7Cno%7Cphr%7C55441187380%7Crt%7C55441187380%7Cdvc%7Cdesktop%7Cpos%7Cpremium1%7Cmch%7C%7Csrc%7Cnone%26calltouch_tm%3Dyd_c%3A702816452_gb%3A5631389295_ad%3A17250595806_ph%3A55441187380_st%3Asearch_pt%3Apremium_p%3A1_s%3Anone_dt%3Adesktop_reg%3A213_ret%3A55441187380_apt%3Anone%26cm_id%3D702816452_5631389295_17250595806_55441187380_55441187380_none_search_type1_no_desktop_premium_213%26etext%3D2202.P2AA4T06IXGLrNltphfV6lKDhwTZuGFAVXJflTFSTfgu24uL9o8bofzF4PMdrDLgeHFld25sbGhnbHdwY2hwdQ.92550066637a0f234f81f60283e95ba64cec2232%26yclid%3D3512435045737168895',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'SCBstart': '1764592727752',
    'SCBindexAct': '1089',
    'sma_index_activity': '1489',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryjNbBccuNnMynzBE4',
    'Origin': 'https://xn----7sbocpkbcearp8a9etgj.xn--p1ai',
    'Referer': 'https://xn----7sbocpkbcearp8a9etgj.xn--p1ai/catalog/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'SCBFormsAlreadyPulled=true; scbsid_old=2746015342; _ym_uid=1756294367437085348; _ym_d=1764247193; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; smFpId_old_values=%5B%225a4ba48b0c99505318ede61cd1067357%22%5D; ced=2k7csd5c5u0i8nb63v77odqprepd88l9; _ym_isad=2; _ym_visorc=w; _cmg_cssttGbx8=1764592723; _comagic_idtGbx8=10113416032.14188502537.1764592723; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1764679123649%2C%22sl%22%3A%7B%22224%22%3A1764592723649%2C%221228%22%3A1764592723649%7D%7D; adrdel=1764592723989; cookie=yes; sma_session_id=2517111582; SCBfrom=https%3A%2F%2Fxn----7sbocpkbcearp8a9etgj.xn--p1ai%2F%3Futm_source%3Dyandex%26utm_medium%3Dcpc%26utm_campaign%3Dy_m108_lk_search_brand_mmo%7C702816452%26utm_term%3D%25D0%25BB%25D0%25B5%25D1%2581%25D0%25BD%25D0%25B0%25D1%258F%2520%25D0%25BA%25D0%25BE%25D0%25BB%25D0%25BB%25D0%25B5%25D0%25BA%25D1%2586%25D0%25B8%25D1%258F%26utm_content%3Dtext_3%7Cgid%7C5631389295%7Caid%7Cno%7Cphr%7C55441187380%7Crt%7C55441187380%7Cdvc%7Cdesktop%7Cpos%7Cpremium1%7Cmch%7C%7Csrc%7Cnone%26calltouch_tm%3Dyd_c%3A702816452_gb%3A5631389295_ad%3A17250595806_ph%3A55441187380_st%3Asearch_pt%3Apremium_p%3A1_s%3Anone_dt%3Adesktop_reg%3A213_ret%3A55441187380_apt%3Anone%26cm_id%3D702816452_5631389295_17250595806_55441187380_55441187380_none_search_type1_no_desktop_premium_213%26etext%3D2202.P2AA4T06IXGLrNltphfV6lKDhwTZuGFAVXJflTFSTfgu24uL9o8bofzF4PMdrDLgeHFld25sbGhnbHdwY2hwdQ.92550066637a0f234f81f60283e95ba64cec2232%26yclid%3D3512435045737168895; SCBnotShow=-1; SCBporogAct=5000; SCBstart=1764592727752; SCBindexAct=1089; sma_index_activity=1489',
}

params = {
    'nc_ctpl': '228',
    'isNaked': '1',
}

files = [
    ('building[]', (None, '1')),
    ('building[]', (None, '2')),
    ('building[]', (None, '3')),
    ('building[]', (None, '4')),
    ('building[]', (None, '5')),
    ('rooms[]', (None, '1')),
    ('rooms[]', (None, '2')),
    ('rooms[]', (None, '3')),
    ('price-from', (None, '8.83')),
    ('price-to', (None, '22.98')),
    ('square-from', (None, '28.40')),
    ('square-to', (None, '79.90')),
    ('finishes', (None, '1')),
    ('sorting', (None, '1')),
    ('more', (None, '0')),
]



flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


driver = webdriver.Chrome()
driver.get("https://lyesnaya.ru/catalog/")

wait = WebDriverWait(driver, 5)  # небольшое ожидание

prev_count = 0

while True:
    try:
        # считаем, сколько товаров отображается
        items = driver.find_elements(By.CSS_SELECTOR, ".catalog-item")
        curr_count = len(items)

        # если после предыдущего клика число элементов не изменилось → конец
        if curr_count == prev_count and curr_count != 0:
            print("Товары больше не подгружаются. Выход из цикла.")
            break

        prev_count = curr_count

        # ждём, пока кнопка станет кликабельной
        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-more-btn]"))
        )
        time.sleep(2)

        try:
            button.click()
        except Exception:
            button = driver.find_element(By.CSS_SELECTOR, "button[data-more-btn]")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            driver.execute_script("arguments[0].click();", button)

        # ждём подгрузку новых карточек
        time.sleep(2)

    except TimeoutException:
        print("Кнопка 'Показать ещё' больше не найдена. Выход из цикла.")
        break

driver.quit()


page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
soup = BeautifulSoup(page_content, 'html.parser')
flats_soup = soup.find_all('a', class_="flat-card catalog-view__item")
for i in flats_soup:

    url = ''
    date = datetime.date.today()
    project = ("Обручева 30")
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
    developer = "ЛСР"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    korpus = ''
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    finish_type = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    type = 'Квартиры'
    room_count = ''
    area = ''
    price_per_metr = ''
    old_price = i.find('span', class_='flat-card__price-current').text.strip().replace(' ', '').replace('₽', '')
    discount = ''
    price_per_metr_new = ''
    price = ''
    section = ''
    floor = ''
    flat_number = ''

    print(
        f"{project}, квартира {flat_number}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
              distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
              konstruktiv,
              klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
              price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)







save_flats_to_excel(flats, project, developer)