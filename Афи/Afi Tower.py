import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests

cookies = {
    'PHPSESSID': 'zw39082pWx8pAKfGHBuDhAoZQ75HKnMs',
    'scbsid_old': '2746015342',
    '_cmg_csstS0cfD': '1751363409',
    '_comagic_idS0cfD': '10727269081.15013256636.1751363409',
    '_slid': '67e145e9c43eb1caaf5ed242',
    '_slsession': 'a89d4890-7da2-4149-8f23-29e9f9cbdc3a',
    '_ym_uid': '1742816746489519570',
    '_ym_d': '1751363410',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_slid_server': '67e145e9c43eb1caaf5ed242',
    'sma_session_id': '2344782810',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    'SCBnotShow': '-1',
    'SCBstart': '1751363453574',
    'smFpId_old_values': '%5B%22d9eadf726ef363c2da5f2fae87307f58%22%5D',
    'SCBporogAct': '5000',
    'sma_index_activity': '32012',
    'SCBindexAct': '2798',
}

headers = {
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://afitower.ru/?utm_source=yandex&utm_medium=cpc&utm_campaign=vim|brand_manual_site_search_mmo|118267340|search&utm_term=%D0%B6%D0%BA%20%D0%B0%D1%84%D0%B8%20%D1%82%D0%B0%D1%83%D1%8D%D1%80&utm_content=5543281619|16894430087|54336079432|none|desktop|16894430087|type1|54336079432|54336079432|1|premium|213|no&cm_id=118267340_5543281619_16894430087_54336079432_54336079432_none_search_type1_no_desktop_premium_213&yclid=14973195589236555775',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=zw39082pWx8pAKfGHBuDhAoZQ75HKnMs; scbsid_old=2746015342; _cmg_csstS0cfD=1751363409; _comagic_idS0cfD=10727269081.15013256636.1751363409; _slid=67e145e9c43eb1caaf5ed242; _slsession=a89d4890-7da2-4149-8f23-29e9f9cbdc3a; _ym_uid=1742816746489519570; _ym_d=1751363410; _ym_isad=2; _ym_visorc=w; _slid_server=67e145e9c43eb1caaf5ed242; sma_session_id=2344782810; SCBfrom=https%3A%2F%2Fyandex.ru%2F; SCBnotShow=-1; SCBstart=1751363453574; smFpId_old_values=%5B%22d9eadf726ef363c2da5f2fae87307f58%22%5D; SCBporogAct=5000; sma_index_activity=32012; SCBindexAct=2798',
}

params = {
    'utm_source': 'yandex',
    'utm_medium': 'cpc',
    'utm_campaign': 'vim|brand_manual_site_search_mmo|118267340|search',
    'utm_term': 'жк афи тауэр',
    'utm_content': '5543281619|16894430087|54336079432|none|desktop|16894430087|type1|54336079432|54336079432|1|premium|213|no',
    'cm_id': '118267340_5543281619_16894430087_54336079432_54336079432_none_search_type1_no_desktop_premium_213',
    'yclid': '14973195589236555775',
    'sort': 'price',
    'sortBy': 'asc',
    'square[]': ['24', '117'],
    'stock': 'all',
    'floor[]': ['2', '52'],
    'price[]': ['12', '54'],
    'pageView': 'params',
    'numberFlat': '',
    'assignment': 'false',
    'page': '1',
    'offset': '8',
    'showMore': 'true'
}



flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
page_counter = 1

while True:

    response = requests.get(
        'https://afitower.ru/',
        cookies=cookies,
        headers=headers,
        params=params)
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    flats_soup = soup.find_all('a', class_=["room-preview"])

    for i in flats_soup:

        try:
            if i.find(class_=['room-preview__bottom', 'room-preview__bottom-bron']).text == 'резерв':
                continue
        except:
            ''

        url = ''
        date = datetime.date.today()
        project = 'Afi Tower'
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
        developer = "AFI"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = '1'
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        if i.select('.room-preview__description .list__item')[2].text == 'чистовая':
            finish_type = 'С отделкой'
        if i.select('.room-preview__description .list__item')[2].text == 'white box':
            finish_type = 'Предчистовая'
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        room_count = ''
        area = float(i.select('.room-preview__description .list__item')[0].text.replace(' м²', ''))
        try:
            old_price = int(i.find(class_='room-preview__price-sale').text.replace(' ', '').replace('₽', ''))
        except:
            old_price = ''
        discount = ''
        price_per_metr = ''
        price_per_metr_new = ''
        try:
            price = int(i.find(class_='room-preview__price-old').text.replace(' ', '').replace('₽', ''))
        except:
            price = ''
        section = ''
        floor = i.select('.room-preview__description .list__item')[1].text.replace(' этаж', '')
        flat_number = ''

        print(
            f"{project}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
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

    params['page'] = str(int(params['page']) + 1)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


df = pd.DataFrame(flats, columns=['Дата обновления',
                              'Название проекта',
                              'на англ',
                              'промзона',
                              'Местоположение',
                              'Метро',
                              'Расстояние до метро, км',
                              'Время до метро, мин',
                              'МЦК/МЦД/БКЛ',
                              'Расстояние до МЦК/МЦД, км',
                              'Время до МЦК/МЦД, мин',
                              'БКЛ',
                              'Расстояние до БКЛ, км',
                              'Время до БКЛ, мин',
                              'статус',
                              'старт',
                              'Комментарий',
                              'Девелопер',
                              'Округ',
                              'Район',
                              'Адрес',
                              'Эскроу',
                              'Корпус',
                              'Конструктив',
                              'Класс',
                              'Срок сдачи',
                              'Старый срок сдачи',
                              'Стадия строительной готовности',
                              'Договор',
                              'Тип помещения',
                              'Отделка',
                              'Кол-во комнат',
                              'Площадь, кв.м',
                              'Цена кв.м, руб.',
                              'Цена лота, руб.',
                              'Скидка,%',
                              'Цена кв.м со ск, руб.',
                              'Цена лота со ск, руб.',
                              'секция',
                              'этаж',
                              'номер'])

current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)