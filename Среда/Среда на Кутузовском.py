import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random

cookies = {
    '__lhash_': 'f87f015cf5f727d88c300986b1a38b24',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1743168863280%2C%22sl%22%3A%7B%22224%22%3A1743082463280%2C%221228%22%3A1743082463280%7D%7D',
    'scbsid_old': '2746015342',
    '_ga': 'GA1.1.981675103.1743082464',
    'tmr_lvid': '264deae7a4cd3a9d92d563d67bdba7e6',
    'tmr_lvidTS': '1743082464542',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    '_ym_uid': '1743082465444153846',
    '_ym_d': '1743082465',
    '_ym_isad': '2',
    'cted': 'modId%3D5wfm9jtf%3Bclient_id%3D981675103.1743082464%3Bya_client_id%3D1743082465444153846',
    '_ct_site_id': '67186',
    '_ct': '2800000000118582218',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'domain_sid': 'rz11zN0wchT0nNAfs1mRu%3A1743082465657',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    'adrdel': '1743143321567',
    'sma_session_id': '2240520345',
    'SCBporogAct': '5000',
    '__js_p_': '594,1800,0,0,0',
    '__jhash_': '999',
    '__jua_': 'Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F134.0.0.0%20Safari%2F537.36',
    '__hash_': '8b94736c295cb4d0678d32f0b72775bc',
    '_ym_visorc': 'w',
    '_ct_ids': '5wfm9jtf%3A67186%3A176584982',
    '_ct_session_id': '176584982',
    'SCBstart': '1743151598337',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'SCBindexAct': '2776',
    'call_s': '___5wfm9jtf.1743153404.176584982.401330:1245457|2___',
    '_ga_CW8DX22VWK': 'GS1.1.1743151595.4.1.1743151605.0.0.0',
    'tmr_detect': '0%7C1743151606409',
    'SCBindexAct': '4143',
    'sma_index_activity': '2964',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://sreda.ru/flats?filtersFlat=%7B%22discount%22%3A0%7D',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '__lhash_=f87f015cf5f727d88c300986b1a38b24; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1743168863280%2C%22sl%22%3A%7B%22224%22%3A1743082463280%2C%221228%22%3A1743082463280%7D%7D; scbsid_old=2746015342; _ga=GA1.1.981675103.1743082464; tmr_lvid=264deae7a4cd3a9d92d563d67bdba7e6; tmr_lvidTS=1743082464542; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; _ym_uid=1743082465444153846; _ym_d=1743082465; _ym_isad=2; cted=modId%3D5wfm9jtf%3Bclient_id%3D981675103.1743082464%3Bya_client_id%3D1743082465444153846; _ct_site_id=67186; _ct=2800000000118582218; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; domain_sid=rz11zN0wchT0nNAfs1mRu%3A1743082465657; SCBnotShow=-1; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; adrdel=1743143321567; sma_session_id=2240520345; SCBporogAct=5000; __js_p_=594,1800,0,0,0; __jhash_=999; __jua_=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F134.0.0.0%20Safari%2F537.36; __hash_=8b94736c295cb4d0678d32f0b72775bc; _ym_visorc=w; _ct_ids=5wfm9jtf%3A67186%3A176584982; _ct_session_id=176584982; SCBstart=1743151598337; SCBFormsAlreadyPulled=true; sma_postview_ready=1; SCBindexAct=2776; call_s=___5wfm9jtf.1743153404.176584982.401330:1245457|2___; _ga_CW8DX22VWK=GS1.1.1743151595.4.1.1743151605.0.0.0; tmr_detect=0%7C1743151606409; SCBindexAct=4143; sma_index_activity=2964',
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
        type = ''
        if i['finish']['isFinish'] is True:
            finish_type = 'С отделкой'
        elif i['finish']['isFinish'] is True and i['finish']['furniture'] is True:
            finish_type = 'С отделкой и доп опциями'
        elif i['finish']['whiteBox'] is True:
            finish_type = 'Предчистовая отделка'
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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Среда"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

