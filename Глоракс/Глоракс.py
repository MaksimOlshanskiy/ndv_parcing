import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random
from bs4 import BeautifulSoup
import requests


import requests

import requests

cookies = {
    'i18n_redirected': 'ru',
    'lang': 'ru',
    '_ct_ids': 'st7roc76%3A42076%3A800874820',
    '_ct_session_id': '800874820',
    '_ct_site_id': '42076',
    '_ct': '1600000000531391973',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    '_ym_uid': '1744296710108808929',
    '_ym_d': '1751360525',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    '_ymab_param': 'iCOCykgPnJlSOBT9ungO1EuygSy168_lMZmeBaJU0dleDq7D4ilz1A0HtHY-uwvmsXQ-083yyyAj0T9V5NFmCdnJ4n8',
    '_ct_server': '1600000000531391973',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '_gcl_au': '1.1.1845648855.1751360526',
    '_ga': 'GA1.1.698110849.1751360526',
    'tmr_lvid': '9487df9146174b34570d8e7c2ce3fd17',
    'tmr_lvidTS': '1744296713801',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1751446926379%2C%22sl%22%3A%7B%22224%22%3A1751360526379%2C%221228%22%3A1751360526379%7D%7D',
    'adrdel': '1751360526504',
    'PSKCbotm': 'CTgkWoWPnzXyAMMNjw5PEuKCERGsYTR5',
    'domain_sid': 'sQPU-uVJcdLFf3wQaUWr3%3A1751360527314',
    'city': '1',
    'sub_city': '3',
    'cted': 'modId%3Dst7roc76%3Bya_client_id%3D1744296710108808929%3Bclient_id%3D698110849.1751360526%7CmodId%3Ddmhpx7b1%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dvdjwu4hh%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dtl9rlo2g%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dw4i0f2gp%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dsti3b1rz%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dqsm27o3s%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3D4ybduhc8%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dzhanf8k7%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929',
    'PageNumber': '2',
    'call_s': '___st7roc76.1751362375.800874820.433320:1217700.442253:1246351.442905:1248402.453856:1282882.473836:1345934.473838:1345957.479915:1364938|2___',
    '_ga_MDT6W94XFL': 'GS2.1.s1751360526$o1$g1$t1751360576$j10$l0$h0',
    'tmr_detect': '0%7C1751360578097',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://glorax.com/apartments-filter/apartamenty-v-moskve',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': 'i18n_redirected=ru; lang=ru; _ct_ids=st7roc76%3A42076%3A800874820; _ct_session_id=800874820; _ct_site_id=42076; _ct=1600000000531391973; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; _ym_uid=1744296710108808929; _ym_d=1751360525; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_isad=2; _ym_visorc=b; _ymab_param=iCOCykgPnJlSOBT9ungO1EuygSy168_lMZmeBaJU0dleDq7D4ilz1A0HtHY-uwvmsXQ-083yyyAj0T9V5NFmCdnJ4n8; _ct_server=1600000000531391973; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _gcl_au=1.1.1845648855.1751360526; _ga=GA1.1.698110849.1751360526; tmr_lvid=9487df9146174b34570d8e7c2ce3fd17; tmr_lvidTS=1744296713801; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1751446926379%2C%22sl%22%3A%7B%22224%22%3A1751360526379%2C%221228%22%3A1751360526379%7D%7D; adrdel=1751360526504; PSKCbotm=CTgkWoWPnzXyAMMNjw5PEuKCERGsYTR5; domain_sid=sQPU-uVJcdLFf3wQaUWr3%3A1751360527314; city=1; sub_city=3; cted=modId%3Dst7roc76%3Bya_client_id%3D1744296710108808929%3Bclient_id%3D698110849.1751360526%7CmodId%3Ddmhpx7b1%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dvdjwu4hh%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dtl9rlo2g%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dw4i0f2gp%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dsti3b1rz%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dqsm27o3s%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3D4ybduhc8%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929%7CmodId%3Dzhanf8k7%3Bclient_id%3D698110849.1751360526%3Bya_client_id%3D1744296710108808929; PageNumber=2; call_s=___st7roc76.1751362375.800874820.433320:1217700.442253:1246351.442905:1248402.453856:1282882.473836:1345934.473838:1345957.479915:1364938|2___; _ga_MDT6W94XFL=GS2.1.s1751360526$o1$g1$t1751360576$j10$l0$h0; tmr_detect=0%7C1751360578097',
}

params = {
    'limit': '21',
    'offset': '0',
    'booked': 'false',
    'city': '1',
    'project': '33',
    'order': 'price',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:
    response = requests.get('https://glorax.com/api/apartments/', params=params, cookies=cookies, headers=headers)
    items = response.json()['results']

    for i in items:

        url = ''
        developer = "Glorax"
        project = i['project_name']
        korpus = i['building_number']
        if i['type'] == 'apartments':
            type = 'Апартаменты'
        if i['type'] == 'apartments':
            type = 'Квартиры'
        finish_type = 'Без отделки'
        room_count = i['rooms']
        try:
            area = i['area']
        except:
            area = ''
        try:
            old_price = float(i['original_price'])
        except:
            old_price = ''
        try:
            price = float(i['price'])
        except:
            price = ''
        section = ''
        try:
            floor = int(i['floor'])
        except:
            floor = ''
        flat_number = i['number']


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
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]


        flats.append(result)
    if not items:
        break
    params['offset'] = str(int(params['offset']) + 21)


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


# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

