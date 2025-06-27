import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random


cookies = {
    'spid': '1741784632987_62d30c366d1e5b195ad803dff541d343_rmtsfh281m20htua',
    '_ym_uid': '1741784635438762062',
    '_ym_d': '1741784635',
    'tmr_lvid': '1c335b6614b3f392afef8213cbdc301d',
    'tmr_lvidTS': '1741784635189',
    '_ga': 'GA1.1.835945232.1741784643',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    'scbsid_old': '2746015342',
    'uxs_uid': '7adaf8b0-ff42-11ef-978b-e730cc09ad57',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    'spsc': '1743780531973_d733658e8127bc75140808365935136f_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'PHPSESSID': '1uvfor5eihm334gbu6htjqol4q',
    '_cmg_csstvfLiQ': '1743780533',
    '_comagic_idvfLiQ': '10090583013.14300024543.1743780532',
    'domain_sid': 'OIbdJw_MXh1IehKOV3pwu%3A1743780533476',
    'tmr_detect': '0%7C1743780534810',
    'USE_COOKIE_CONSENT_STATE': '{%22session%22:true%2C%22persistent%22:true%2C%22necessary%22:true%2C%22preferences%22:true%2C%22statistics%22:true%2C%22marketing%22:true%2C%22firstParty%22:true%2C%22thirdParty%22:true}',
    'sessionId': '17437805349851471298',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1743866936575%2C%22sl%22%3A%7B%22224%22%3A1743780536575%2C%221228%22%3A1743780536575%7D%7D',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1743866936575%2C%22sl%22%3A%7B%22224%22%3A1743780536575%2C%221228%22%3A1743780536575%7D%7D',
    'sma_session_id': '2249634741',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%2C%22b0d44eece823d71c253568fc397e79de%22%5D',
    'adrdel': '1743780536988',
    'adrdel': '1743780536988',
    'SCBstart': '1743780537057',
    'SCBporogAct': '5000',
    'sma_postview_ready': '1',
    'sma_index_activity': '1132',
    'SCBindexAct': '882',
    '_ga_H5S7YBLWM3': 'GS1.1.17437805349851471298.5.1.1743780544.0.0.0',
    '_ga_70ZZHDSCR6': 'GS1.1.1743780535.5.1.1743780544.51.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': '',
    'baggage': 'sentry-environment=production,sentry-public_key=64d42d1ec99f4044ff0df570a905dbca,sentry-trace_id=0b9cf8a3f4fe496d91cb258de170e831,sentry-sample_rate=0.1,sentry-transaction=%2Fflats%2F*,sentry-sampled=false',
    'priority': 'u=1, i',
    'referer': 'https://www.mr-group.ru/flats/page-2/?grid=card',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '0b9cf8a3f4fe496d91cb258de170e831-92f48918f4511a31-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'spid=1741784632987_62d30c366d1e5b195ad803dff541d343_rmtsfh281m20htua; _ym_uid=1741784635438762062; _ym_d=1741784635; tmr_lvid=1c335b6614b3f392afef8213cbdc301d; tmr_lvidTS=1741784635189; _ga=GA1.1.835945232.1741784643; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; scbsid_old=2746015342; uxs_uid=7adaf8b0-ff42-11ef-978b-e730cc09ad57; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; spsc=1743780531973_d733658e8127bc75140808365935136f_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5; _ym_isad=2; _ym_visorc=w; PHPSESSID=1uvfor5eihm334gbu6htjqol4q; _cmg_csstvfLiQ=1743780533; _comagic_idvfLiQ=10090583013.14300024543.1743780532; domain_sid=OIbdJw_MXh1IehKOV3pwu%3A1743780533476; tmr_detect=0%7C1743780534810; USE_COOKIE_CONSENT_STATE={%22session%22:true%2C%22persistent%22:true%2C%22necessary%22:true%2C%22preferences%22:true%2C%22statistics%22:true%2C%22marketing%22:true%2C%22firstParty%22:true%2C%22thirdParty%22:true}; sessionId=17437805349851471298; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1743866936575%2C%22sl%22%3A%7B%22224%22%3A1743780536575%2C%221228%22%3A1743780536575%7D%7D; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1743866936575%2C%22sl%22%3A%7B%22224%22%3A1743780536575%2C%221228%22%3A1743780536575%7D%7D; sma_session_id=2249634741; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%2C%22b0d44eece823d71c253568fc397e79de%22%5D; adrdel=1743780536988; adrdel=1743780536988; SCBstart=1743780537057; SCBporogAct=5000; sma_postview_ready=1; sma_index_activity=1132; SCBindexAct=882; _ga_H5S7YBLWM3=GS1.1.17437805349851471298.5.1.1743780544.0.0.0; _ga_70ZZHDSCR6=GS1.1.1743780535.5.1.1743780544.51.0.0',
}


params = {
    'category': 'flats',
    'page': '1',
    'limit': '1000',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://www.mr-group.ru/api/sale/products', params=params, cookies=cookies, headers=headers)

    items = response.json()["items"]

    for i in items:

        url = ""

        date = datetime.date.today()
        project = i["project"]["name"]
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
        developer = "MR"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i["building"]["name"].replace('Корпус ', '')
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if i['subtype']['name'] == 'Апартаменты':
            type = 'Апартаменты'
        else:
            type = 'Квартиры'
        if i["decoration"]["name"] == "MR Base":
            finish_type = "Предчистовая"
        elif i["decoration"]["name"] == "MR Ready":
            finish_type = "С отделкой"
        else:
            finish_type = i["decoration"]["name"]

        room_count = int(i["rooms_number"])
        area = i["area"]
        price_per_metr = ''
        old_price = ""
        discount = ''
        price_per_metr_new = ''
        if not i['discount']:
            price = i["price"]
            old_price = i["price"]
        else:
            price = i['discount']['price']
            old_price = i["price"]
        section = ''
        floor = i["floor"]
        flat_number = ''

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["page"] = str(int(params["page"]) + 1)
    sleep_time = random.uniform(10, 15)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break

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

filename = f"{developer}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

