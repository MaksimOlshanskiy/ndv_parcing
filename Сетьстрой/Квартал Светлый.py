import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests

cookies = {
    'PHPSESSID': 'ba6a7a761a176c6cbc875a85fc67d076',
    '_ga': 'GA1.1.2069892075.1743596770',
    '_ym_uid': '1743596771118852710',
    '_ym_d': '1743596771',
    '_ct_ids': 'b2mclhb1%3A54606%3A540448718',
    '_ct_session_id': '540448718',
    '_ct_site_id': '54606',
    '_ct': '2200000000349027082',
    '_ym_isad': '2',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_visorc': 'w',
    'cted': 'modId%3Db2mclhb1%3Bclient_id%3D2069892075.1743596770%3Bya_client_id%3D1743596771118852710',
    'call_s': '___b2mclhb1.1743598579.540448718.340494:971980.347373:988893|2___',
    '_ga_KX7EM742R5': 'GS1.1.1743596769.1.1.1743596801.28.0.121099151',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://xn----7sbagds2abmd3cpjg0l.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn----7sbagds2abmd3cpjg0l.xn--p1ai/apartments/?filter[price][min]=0&filter[price][max]=10400000&filter[area][min]=23.1&filter[area][max]=61.6&filter[floor][min]=2&filter[floor][max]=17&filter[building]=all&filter[sort_price]=&filter[sort_area]=',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=ba6a7a761a176c6cbc875a85fc67d076; _ga=GA1.1.2069892075.1743596770; _ym_uid=1743596771118852710; _ym_d=1743596771; _ct_ids=b2mclhb1%3A54606%3A540448718; _ct_session_id=540448718; _ct_site_id=54606; _ct=2200000000349027082; _ym_isad=2; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_visorc=w; cted=modId%3Db2mclhb1%3Bclient_id%3D2069892075.1743596770%3Bya_client_id%3D1743596771118852710; call_s=___b2mclhb1.1743598579.540448718.340494:971980.347373:988893|2___; _ga_KX7EM742R5=GS1.1.1743596769.1.1.1743596801.28.0.121099151',
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


while True:

    response = requests.post(
        'https://xn----7sbagds2abmd3cpjg0l.xn--p1ai/ajax/apartments.json/',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    print(response.status_code)
    items = response.json()['items']
    soup = BeautifulSoup(response.text, 'html.parser')
    flats_soup = soup.find_all('tr', class_= 'cat-tbl__item')
    print(flats_soup)


    for i in flats_soup:
        print(i.text)
        url = ''

        date = datetime.date.today()
        project = i.find('span', class_= 'catalogCard__text').text.replace('«', '').replace('»', '').replace('КД ', '').replace('ЖК ', '')

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
        developer = "Атлант"
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
        if project == 'Новое Вашутино':
            type = 'Апартаменты'
        else:
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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Атлант"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)