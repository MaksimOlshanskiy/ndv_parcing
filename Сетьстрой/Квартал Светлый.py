import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

from functions import save_flats_to_excel

cookies = {
    '_ga': 'GA1.1.459138510.1750941629',
    '_ym_uid': '1743596771118852710',
    '_ym_d': '1750941629',
    '_ct': '2200000000382242926',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'PHPSESSID': 'fda652259759872d10f127a02fbe7a09',
    'cted': 'modId%3Db2mclhb1%3Bclient_id%3D459138510.1750941629%3Bya_client_id%3D1743596771118852710',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ct_ids': 'b2mclhb1%3A54606%3A608845184',
    '_ct_session_id': '608845184',
    '_ct_site_id': '54606',
    '_ga_KX7EM742R5': 'GS2.1.s1753454046$o3$g1$t1753454124$j58$l0$h660008952',
    'call_s': '___b2mclhb1.1753455924.608845184.340494:1009627.347373:988893|2___',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://xn----7sbagds2abmd3cpjg0l.xn--p1ai',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://xn----7sbagds2abmd3cpjg0l.xn--p1ai/apartments/?filter[price][min]=0&filter[price][max]=10400000&filter[area][min]=23.1&filter[area][max]=61.6&filter[floor][min]=2&filter[floor][max]=17&filter[building]=all&filter[sort_price]=&filter[sort_area]=',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '_ga=GA1.1.459138510.1750941629; _ym_uid=1743596771118852710; _ym_d=1750941629; _ct=2200000000382242926; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; PHPSESSID=fda652259759872d10f127a02fbe7a09; cted=modId%3Db2mclhb1%3Bclient_id%3D459138510.1750941629%3Bya_client_id%3D1743596771118852710; _ym_isad=2; _ym_visorc=w; _ct_ids=b2mclhb1%3A54606%3A608845184; _ct_session_id=608845184; _ct_site_id=54606; _ga_KX7EM742R5=GS2.1.s1753454046$o3$g1$t1753454124$j58$l0$h660008952; call_s=___b2mclhb1.1753455924.608845184.340494:1009627.347373:988893|2___',
}

data = {
    'filter[price][min]': '0',
    'filter[price][max]': '10400000',
    'filter[area][min]': '23.1',
    'filter[area][max]': '61.6',
    'filter[floor][min]': '2',
    'filter[floor][max]': '17',
    'filter[building]': 'all',
    'filter[sort_price]': '',
    'filter[sort_area]': '',
}


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

developer = "Сетьстрой"

while True:

    web_site = f'https://xn----7sbagds2abmd3cpjg0l.xn--p1ai/apartments/?filter[price][min]=0&filter[price][max]=10400000&filter[area][min]=23.1&filter[area][max]=61.6&filter[floor][min]=2&filter[floor][max]=17&filter[building]=all&filter[sort_price]=&filter[sort_area]='
    driver = webdriver.Chrome()
    driver.get(url=web_site)
    page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript



    soup = BeautifulSoup(page_content, 'html.parser')
    flats_soup = soup.find_all('tr', class_= ['cat-tbl__item'])
    print(flats_soup)


    for i in flats_soup:

        url = ''

        date = datetime.date.today()
        project = 'Квартал Светлый'

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
        try:
            korpus = ''
        except ValueError:
            korpus = ''
        konstruktiv = ''
        klass = ''
        elements = i.find_all('span', class_='badge__text')
        finish_type = elements[1].text
        srok_sdachi = ''

        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        if extract_digits_or_original(i.find('span', class_= 'catalogCard__smallText').text.split()[0]) == 'Студия':
            room_count = 0
        else:
            room_count = extract_digits_or_original(i.find('span', class_= 'catalogCard__smallText').text.split()[0])
        area = float(i.find('span', class_= 'catalogCard__bigText').text.replace(' м2', ''))
        price_per_metr = ''
        old_price = int(i.find('span', class_= 'catalogCard__smallText catalogCard__smallText-old-price').text.replace(' ', '').replace('₽', ''))

        discount = ''
        price_per_metr_new = ''
        price = int(i.find('span', class_= 'catalogCard__bigText textRed').text.replace(' ', '').replace('₽', ''))
        section = ''
        try:
            floor = int(i.find('div', class_= ['catalogCard__textCol catalogCard__textCol--right']).text.replace(' этаж', ''))
        except ValueError:
            floor = int(i.find('div', class_= ['catalogCard__textCol catalogCard__textCol--right']).text.split()[0])
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

    if not flats_soup:
        break
    data['page'] = str(int(data['page']) +1)

    print('--------------------------------------------------------------------------------')

    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)