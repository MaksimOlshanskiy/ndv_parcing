import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    'scbsid_old': '2746015342',
    'tmr_lvid': 'aad5d37970c59d2bd85f70997504626e',
    'tmr_lvidTS': '1741789069029',
    '_ym_uid': '1741789069854858672',
    '_ym_d': '1741789069',
    'adrdel': '1741789069175',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    '_ym_isad': '2',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1741875469182%2C%22sl%22%3A%7B%22224%22%3A1741789069182%2C%221228%22%3A1741789069182%7D%7D',
    'sma_session_id': '2220871853',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    '_cmg_csst6s8R1': '1741789069',
    '_comagic_id6s8R1': '10025825086.14198458151.1741789069',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    '_ym_visorc': 'w',
    'SCBstart': '1741789069454',
    'domain_sid': 'tNei4h3ukTz-QDWV8eIND%3A1741789070066',
    'SCBporogAct': '5000',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'tmr_detect': '0%7C1741789092053',
    'SCBindexAct': '1487',
    'sma_index_activity': '1987',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://gk-osnova.ru/kupit-kvartiru?etazh=1,33&price=4000000,265000000&minDiscount=0&sortBy=cost&orderBy=asc',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=2746015342; tmr_lvid=aad5d37970c59d2bd85f70997504626e; tmr_lvidTS=1741789069029; _ym_uid=1741789069854858672; _ym_d=1741789069; adrdel=1741789069175; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; _ym_isad=2; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1741875469182%2C%22sl%22%3A%7B%22224%22%3A1741789069182%2C%221228%22%3A1741789069182%7D%7D; sma_session_id=2220871853; SCBfrom=https%3A%2F%2Fwww.google.com%2F; _cmg_csst6s8R1=1741789069; _comagic_id6s8R1=10025825086.14198458151.1741789069; SCBnotShow=-1; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; _ym_visorc=w; SCBstart=1741789069454; domain_sid=tNei4h3ukTz-QDWV8eIND%3A1741789070066; SCBporogAct=5000; SCBFormsAlreadyPulled=true; sma_postview_ready=1; tmr_detect=0%7C1741789092053; SCBindexAct=1487; sma_index_activity=1987',
}

params = {
    'page':1,

}

zk_dict = {4: 'Mainstreet', 2: 'RED7', 3: "UNO, Старокоптевский", 1: "Very на ботанической", 7: "UNO, Головинские пруды",
       8: "Физтехсити", 9: "Nametkin tower", 11: "Гоголь парк", 12: "Мираполис", 14: "Emotion", 15: "Малиново",
       16: "Evopark Сокольники", 17: "Evopark Измайлово", 18: "UNO, Соколиная гора", 19: 'UNO.Горбунова'
       }

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get(
        'https://gk-osnova.ru/api/building-objects/filter?min_cost=4000000&max_cost=265000000&min_floor=1&max_floor=33&layout_types[0]=flat&layout_types[1]=apartment&sort[cost]=asc&&min_discount=0&projects[0]=4&projects[1]=2&projects[2]=3&projects[3]=1&projects[4]=7&projects[5]=6&projects[6]=8&projects[7]=9&projects[8]=10&projects[9]=11&projects[10]=12&projects[11]=13&projects[12]=14&projects[13]=15&projects[14]=16&projects[15]=17&projects[16]=18&projects[17]=19',
        cookies=cookies,
        headers=headers,
        params=params
    )

    items = response.json()["data"]["flats"]

    for i in items:

        url = ""

        date = datetime.date.today()
        project = zk_dict.get(i["project_id"], i["project_id"])
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
        developer = "Основа"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        try:
            korpus = int(i["building"])
        except:
            korpus = i["building"]
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'

        try:
            if i["properties"].get("with_decoration_whitebox") is not None and i["properties"].get("with_decoration_whitebox") == True:
                finish_type = "Предчистовая"
            elif i["properties"].get("with_decoration_finishing") is not None and i["properties"].get("with_decoration_finishing") == True:
                finish_type = "С отделкой"
            elif i["properties"].get("with_decoration_furnished") is not None and i["properties"].get("with_decoration_furnished") == True:
                finish_type = "С отделкой и доп опциями"
            else:
                finish_type = 'Без отделки'
        except:
            finish_type = 'Без отделки'

        room_count = i["layout"]["room_count"]
        area = i["layout"]["area"]
        price_per_metr = ''
        old_price = i["cost"]
        discount = ''
        price_per_metr_new = ''
        price = i["discount_cost"]
        try:
            section = int(i["section"])
        except:
            section = i["section"]
        floor = i["floor"]["number"]
        flat_number = i["number"]

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["page"] = str(int(params["page"]) + 1)
    sleep_time = random.uniform(2, 5)
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
