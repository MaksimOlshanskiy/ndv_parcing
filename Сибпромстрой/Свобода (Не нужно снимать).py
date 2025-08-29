import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By



import requests

import requests

from functions import save_flats_to_excel

"""
Свобода снимается файлом moscow
"""

cookies = {
    '_gid': 'GA1.2.712955819.1743077089',
    'tmr_lvid': '0ba93a2232def7fd1f999fc186b673ce',
    'tmr_lvidTS': '1743077089086',
    '_ct': '700000001758094219',
    '_ym_uid': '1743077090805092488',
    '_ym_d': '1743077090',
    '_ct_ids': '77ba1244%3A25573%3A2127075920_3043f8f3%3A21807%3A1845087207_87ac37e1%3A24913%3A1845087206',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'domain_sid': 'Fmo_C21mO5RoY2Pd3UYjj%3A1743077089886',
    'cted': 'modId%3D87ac37e1%3Bclient_id%3D1564843785.1743077089%3Bya_client_id%3D1743077090805092488%7CmodId%3D3043f8f3%3Bclient_id%3D1564843785.1743077089%3Bya_client_id%3D1743077090805092488%7CmodId%3D77ba1244%3Bclient_id%3D1564843785.1743077089%3Bya_client_id%3D1743077090805092488',
    'amo-livechat-id': 'PosVy-pkQxl7DYwfoEw_B',
    'sps_cookie_agree': '1',
    '_ga_XLSXEK9Z8E': 'GS1.1.1743077088.1.1.1743077132.16.0.0',
    '_ga': 'GA1.1.1564843785.1743077089',
    '_ct_session_id': '1845087206',
    '_ct_site_id': '24913',
    'call_s': '___77ba1244.1743078932.2127075920.79670:334333|3043f8f3.1743078932.1845087207.97369:312754.99980:320195.335242:960093|87ac37e1.1743078932.1845087206.75686:472208.150954:472175.150955:472201|2___',
    'tmr_detect': '0%7C1743077134780',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://www.sibpromstroy.ru/projects/zhk-svoboda/k1/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '_gid=GA1.2.712955819.1743077089; tmr_lvid=0ba93a2232def7fd1f999fc186b673ce; tmr_lvidTS=1743077089086; _ct=700000001758094219; _ym_uid=1743077090805092488; _ym_d=1743077090; _ct_ids=77ba1244%3A25573%3A2127075920_3043f8f3%3A21807%3A1845087207_87ac37e1%3A24913%3A1845087206; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_isad=2; _ym_visorc=w; domain_sid=Fmo_C21mO5RoY2Pd3UYjj%3A1743077089886; cted=modId%3D87ac37e1%3Bclient_id%3D1564843785.1743077089%3Bya_client_id%3D1743077090805092488%7CmodId%3D3043f8f3%3Bclient_id%3D1564843785.1743077089%3Bya_client_id%3D1743077090805092488%7CmodId%3D77ba1244%3Bclient_id%3D1564843785.1743077089%3Bya_client_id%3D1743077090805092488; amo-livechat-id=PosVy-pkQxl7DYwfoEw_B; sps_cookie_agree=1; _ga_XLSXEK9Z8E=GS1.1.1743077088.1.1.1743077132.16.0.0; _ga=GA1.1.1564843785.1743077089; _ct_session_id=1845087206; _ct_site_id=24913; call_s=___77ba1244.1743078932.2127075920.79670:334333|3043f8f3.1743078932.1845087207.97369:312754.99980:320195.335242:960093|87ac37e1.1743078932.1845087206.75686:472208.150954:472175.150955:472201|2___; tmr_detect=0%7C1743077134780',
}

params = {
    '_wrapper_format': 'drupal_ajax',
    'view_name': 'flat_search_project_building',
    'view_display_id': 'block_2',
    'view_args': '22825/36840',
    'view_path': '/node/36840',
    'view_base_path': '',
    'view_dom_id': '3e51ced2f135aff9677cce6b90b609a47f234bad0b5d842045d8111efb33ced3',
    'pager_element': '0',
    'page': '0',
    '_drupal_ajax': '1',
    'ajax_page_state[theme]': 'sps_bs5sass',
    'ajax_page_state[theme_token]': '',
    'ajax_page_state[libraries]': 'eJx1UltuxCAMvBAbvnoeZIjD0hocYSe76emXblKpzeMHi5lBHo-BosmzWlhrN3DNxqMqVofPkQV7NyRqV7EwKTuZfE56JYlYsAJd0YKEQR0QucIFjSf4XqxP3MEnPI1nVtEKo_NQa2K7utmjkdgD3UQXSiUe-YwiEFEcpXjXI1-4R4NtYF0qDlixBNws2nPYECw8qeuTBJ6xLra5D0xGRnFePgSkxZM51HwLd9B_-M7unPAh9n2uU_8FMvcToXmg_xndbnXV7cGWZW52ux4VEkknMB9f7kXKMZ40-JWlMk6aQb4uFVu4l_y64gP93uQZ2K0fynFL-wX4YAFj',
}




flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

page_counter = 0
driver = webdriver.Chrome()

while True:

    web_site = f'https://www.sibpromstroy.ru/flat-search/?f%5B0%5D=city_region%3A32&f%5B1%5D=project%3A22825&page={page_counter}'

    driver.get(url=web_site)
    page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
    soup = BeautifulSoup(page_content, 'html.parser')
    flats_soup = soup.find_all('div', class_=["node__content row"])
    for i in flats_soup:

        url = ''
        date = datetime.date.today()
        project = "Свобода"
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
        developer = "Сибпромстрой"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = extract_digits_or_original(i.find('span', class_="flat--addr--building").text.strip())
        konstruktiv = ''
        klass = ''
        finish_type = i.find('div', class_="flat--stats--facing col-8 col-lg-9 col-xxl-10").text.strip().replace('Отделка: ', '')
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        room_count = extract_digits_or_original(i.find('span', class_="flat--stats--rooms").text.strip())
        area = float(i.find('span', class_="flat--stats--area").text.strip().replace(' м²', ''))
        price_per_metr = ''
        old_price = int(i.find('div', class_= 'flat--prices--full-price fw-bold me-md-3 me-lg-0').text.replace(' ₽', '').replace(' ', ''))
        srok_sdachi = ''
        discount = ''
        price_per_metr_new = ''
        price = ''
        section = ''
        floor = ''

        flat_number = ''

        print(
            f"{project}, квартира {flat_number}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, секция {section}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not flats_soup:
        break


    print('--------------------------------------------------------------------------------')

    page_counter += 1
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)