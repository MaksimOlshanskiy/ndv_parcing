import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'scbsid_old': '2746015342',
    '_ym_uid': '1741789069854858672',
    '_ym_d': '1745827865',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'tmr_lvid': 'aad5d37970c59d2bd85f70997504626e',
    'tmr_lvidTS': '1741789069029',
    'tmr_lvid': 'aad5d37970c59d2bd85f70997504626e',
    'tmr_lvidTS': '1741789069029',
    'SCBnotShow': '-1',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csst6s8R1': '1750929838',
    '_comagic_id6s8R1': '10695554871.14976856276.1750929837',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1751016237765%2C%22sl%22%3A%7B%22224%22%3A1750929837765%2C%221228%22%3A1750929837765%7D%7D',
    'adrdel': '1750929837863',
    'domain_sid': 'tNei4h3ukTz-QDWV8eIND%3A1750929839066',
    'sma_session_id': '2339886367',
    'SCBfrom': '',
    'smFpId_old_values': '%5B%22b0d44eece823d71c253568fc397e79de%22%2C%22f0a18207107a745e280d9357abcbd51d%22%2C%22d3b2a7a62667c988953915d7d3b4139e%22%2C%22ca505640ddf99ec8d4755fa1299dcd1a%22%5D',
    'SCBstart': '1750929840186',
    'sma_postview_ready': '1',
    'SCBporogAct': '5000',
    'view_room_osnova': '1',
    'tmr_detect': '0%7C1750930136198',
    'SCBindexAct': '1340',
    'sma_index_activity': '2040',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://gk-osnova.ru/kupit-kvartiru?etazh=1,33&price=4000000,265000000&minDiscount=0&sortBy=cost&orderBy=asc',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=2746015342; _ym_uid=1741789069854858672; _ym_d=1745827865; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; tmr_lvid=aad5d37970c59d2bd85f70997504626e; tmr_lvidTS=1741789069029; tmr_lvid=aad5d37970c59d2bd85f70997504626e; tmr_lvidTS=1741789069029; SCBnotShow=-1; _ym_isad=2; _ym_visorc=w; _cmg_csst6s8R1=1750929838; _comagic_id6s8R1=10695554871.14976856276.1750929837; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1751016237765%2C%22sl%22%3A%7B%22224%22%3A1750929837765%2C%221228%22%3A1750929837765%7D%7D; adrdel=1750929837863; domain_sid=tNei4h3ukTz-QDWV8eIND%3A1750929839066; sma_session_id=2339886367; SCBfrom=; smFpId_old_values=%5B%22b0d44eece823d71c253568fc397e79de%22%2C%22f0a18207107a745e280d9357abcbd51d%22%2C%22d3b2a7a62667c988953915d7d3b4139e%22%2C%22ca505640ddf99ec8d4755fa1299dcd1a%22%5D; SCBstart=1750929840186; sma_postview_ready=1; SCBporogAct=5000; view_room_osnova=1; tmr_detect=0%7C1750930136198; SCBindexAct=1340; sma_index_activity=2040',
}

params = {
    'page':1,

}

zk_dict = {4: 'Mainstreet', 2: 'RED7', 3: "UNO, Старокоптевский", 1: "Very на ботанической", 7: "UNO, Головинские пруды",
       8: "Физтехсити", 9: "Nametkin tower", 11: "Гоголь парк", 12: "Мираполис", 14: "Emotion", 15: "Малиново",
       16: "Evopark Сокольники", 17: "Evopark Измайлово", 18: "UNO, Соколиная гора", 19: 'UNO.Горбунова'
       }

flats = []

session = requests.Session()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    try:
        response = session.get(
            'https://gk-osnova.ru/api/building-objects/filter?min_cost=4000000&max_cost=265000000&min_floor=1&max_floor=33&layout_types[0]=flat&layout_types[1]=apartment&sort[cost]=asc&&min_discount=0&projects[0]=4&projects[1]=2&projects[2]=3&projects[3]=1&projects[4]=7&projects[5]=6&projects[6]=8&projects[7]=9&projects[8]=10&projects[9]=11&projects[10]=12&projects[11]=13&projects[12]=14&projects[13]=15&projects[14]=16&projects[15]=17&projects[16]=18&projects[17]=19',
            cookies=cookies,
            headers=headers,
            params=params
        )
        print(response.status_code)

        items = response.json()["data"]["flats"]
    except:
        print('Ошибка. Пробую перезапустить сессию')
        time.sleep(10)
        session = requests.Session()
        response = session.get(
            'https://gk-osnova.ru/api/building-objects/filter?min_cost=4000000&max_cost=265000000&min_floor=1&max_floor=33&layout_types[0]=flat&layout_types[1]=apartment&sort[cost]=asc&&min_discount=0&projects[0]=4&projects[1]=2&projects[2]=3&projects[3]=1&projects[4]=7&projects[5]=6&projects[6]=8&projects[7]=9&projects[8]=10&projects[9]=11&projects[10]=12&projects[11]=13&projects[12]=14&projects[13]=15&projects[14]=16&projects[15]=17&projects[16]=18&projects[17]=19',
            cookies=cookies,
            headers=headers,
            params=params
        )
        print(response.status_code)

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
    sleep_time = random.uniform(4, 8)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break

save_flats_to_excel(flats, project, developer)
