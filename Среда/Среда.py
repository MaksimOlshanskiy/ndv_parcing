'''

Нужно обновлять cookie и headers

'''

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random

cookies = {
    '__js_p_': '356,86400,1,0,0',
    '__jhash_': '792',
    '__jua_': 'Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F137.0.0.0%20Safari%2F537.36',
    '__hash_': 'cf4f68f68a876c52a79beac25b74bc66',
    '__lhash_': '28dad3360ec92d6b6be76cf3433419b6',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1751028759098%2C%22sl%22%3A%7B%22224%22%3A1750942359098%2C%221228%22%3A1750942359098%7D%7D',
    'adrdel': '1750942359490',
    '_ga': 'GA1.1.531695832.1750942360',
    'scbsid_old': '2746015342',
    'tmr_lvid': '264deae7a4cd3a9d92d563d67bdba7e6',
    'tmr_lvidTS': '1743082464542',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    '_ct_ids': '5wfm9jtf%3A67186%3A225717261',
    '_ct_session_id': '225717261',
    '_ct_site_id': '67186',
    'call_s': '___5wfm9jtf.1750944160.225717261.401330:1128693|2___',
    '_ct': '2800000000151489421',
    '_ym_uid': '1743082465444153846',
    '_ym_d': '1750942361',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_isad': '2',
    'domain_sid': 'rz11zN0wchT0nNAfs1mRu%3A1750942361478',
    '_ym_visorc': 'w',
    'cookieConsent': 'true',
    'cted': 'modId%3D5wfm9jtf%3Bclient_id%3D531695832.1750942360%3Bya_client_id%3D1743082465444153846',
    'tmr_detect': '0%7C1750942362735',
    'sma_session_id': '2340110960',
    'SCBfrom': 'https%3A%2F%2Fsreda.ru%2Fflats%3FfiltersFlat%3D%257B%2522default%2522%253A0%252C%2522block_id_list%2522%253A%255B%25222192%2522%255D%257D%26gridType%3Dlist',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%22d3b2a7a62667c988953915d7d3b4139e%22%5D',
    'SCBstart': '1750942365129',
    'SCBindexAct': '330',
    '_ga_CW8DX22VWK': 'GS2.1.s1750942360$o1$g1$t1750942365$j55$l0$h0',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'SCBindexAct': '545',
    'sma_index_activity': '997',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://sreda.ru/flats',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    # 'cookie': '__js_p_=356,86400,1,0,0; __jhash_=792; __jua_=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F137.0.0.0%20Safari%2F537.36; __hash_=cf4f68f68a876c52a79beac25b74bc66; __lhash_=28dad3360ec92d6b6be76cf3433419b6; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1751028759098%2C%22sl%22%3A%7B%22224%22%3A1750942359098%2C%221228%22%3A1750942359098%7D%7D; adrdel=1750942359490; _ga=GA1.1.531695832.1750942360; scbsid_old=2746015342; tmr_lvid=264deae7a4cd3a9d92d563d67bdba7e6; tmr_lvidTS=1743082464542; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; _ct_ids=5wfm9jtf%3A67186%3A225717261; _ct_session_id=225717261; _ct_site_id=67186; call_s=___5wfm9jtf.1750944160.225717261.401330:1128693|2___; _ct=2800000000151489421; _ym_uid=1743082465444153846; _ym_d=1750942361; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_isad=2; domain_sid=rz11zN0wchT0nNAfs1mRu%3A1750942361478; _ym_visorc=w; cookieConsent=true; cted=modId%3D5wfm9jtf%3Bclient_id%3D531695832.1750942360%3Bya_client_id%3D1743082465444153846; tmr_detect=0%7C1750942362735; sma_session_id=2340110960; SCBfrom=https%3A%2F%2Fsreda.ru%2Fflats%3FfiltersFlat%3D%257B%2522default%2522%253A0%252C%2522block_id_list%2522%253A%255B%25222192%2522%255D%257D%26gridType%3Dlist; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%22d3b2a7a62667c988953915d7d3b4139e%22%5D; SCBstart=1750942365129; SCBindexAct=330; _ga_CW8DX22VWK=GS2.1.s1750942360$o1$g1$t1750942365$j55$l0$h0; SCBFormsAlreadyPulled=true; sma_postview_ready=1; SCBindexAct=545; sma_index_activity=997',
}

params = {
    'default': '1',
    'limit': '500',
    'offset': '0',
}





flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://sreda.ru/api/flat/search', params=params, cookies=cookies, headers=headers)
    print(response.status_code)


    items = response.json()['data']['list']


    for i in items:

        url = ''
        developer = "Среда"
        project = i['name']
        korpus = i['bulk_name'].replace('Корпус', '').strip()
        type = 'Квартиры'
        if i['finish']['isFinish'] is True:
            finish_type = 'С отделкой'
        elif i['finish']['isFinish'] is True and i['finish']['furniture'] is True:
            finish_type = 'С отделкой и доп опциями'
        elif i['finish']['whiteBox'] is True:
            finish_type = 'Предчистовая'
        else:
            finish_type = 'Без отделки'
        room_count = i['rooms']
        try:
            area = float(i['area'])
        except:
            area = i['area']
        try:
            old_price = round(int(i['price']) * 100 / (100-i['discount']))
        except:
            old_price = ''
        try:
            price = int(i['price'])
        except:
            price = ''
        section = ''
        try:
            floor = int(i['floor'])
        except:
            floor = ''
        flat_number = ''

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
        srok_sdachi = i['settlement_date']
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''
        date = datetime.now().date()


        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not items:
        break
    params['offset'] = str(int(params['offset']) + 500)
    sleep_time = random.uniform(1, 5)
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

current_date = datetime.now().date()

# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

