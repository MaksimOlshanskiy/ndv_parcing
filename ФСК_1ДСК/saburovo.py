import datetime
import time
import random

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

import requests

cookies = {
    '_ym_uid': '1744191067563188896',
    '_ym_d': '1744191067',
    'flomni_641ae9eee9a473ff3717a7c0': '{%22userHash%22:%22f0b86d1a-2b92-4eaa-bfb3-411145959846%22}',
    'scbsid_old': '2796070936',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '_gcl_au': '1.1.1359056039.1744191068',
    'adtech_uid': '817cec93-8f65-496f-91b1-3a898d61083d%3Afsk.ru',
    'top100_id': 't1.7712007.1435734598.1744191068028',
    '_ga': 'GA1.1.873115281.1744191068',
    'smFpId_old_values': '%5B%2204b0ffbac42ccceb635ec5bff5b15618%22%5D',
    'SCBstart': '1744191068373',
    'SCBporogAct': '5000',
    'SCBFormsAlreadyPulled': 'true',
    '_fsid': 's%3AYTHH2LngDmQ0iiCDQi77veYJTCf2f71_.ifth3uYXMV4LF%2Fhdx5j8zrZxhFaI1uFJI16ULXn%2Fr84',
    '_ym_isad': '1',
    '_cmg_csstxWdO1': '1744292222',
    '_comagic_idxWdO1': '10222016746.14429217501.1744292223',
    '_ym_visorc': 'b',
    'sma_session_id': '2256955299',
    'SCBnotShow': '-1',
    '_qz_sess': '7204e4fe-e1b6-4bcb-af17-e78b3010fa3c',
    '_yasc': 'ToSC0m4k3r82nONfA8OoqGzP7MVSMFOlAGZLLN4FEiUf0CiNYI7wgzRRHaKTwCSHDqAP',
    'startSession': 'true',
    'gtm_session_start': '1744294024174',
    'sma_postview_ready': '1',
    'gtm_session_threshold': 'true',
    'floodLigth_session': 'fa514d1259b02',
    'mindboxDeviceUUID': '5bffbc54-9cb5-4220-a55d-d406d5c3b8d1',
    'directCrm-session': '%7B%22deviceGuid%22%3A%225bffbc54-9cb5-4220-a55d-d406d5c3b8d1%22%7D',
    'SCBindexAct': '2086',
    'pageviewTimerOther': '3269.2530000000006',
    'startDate': '1744295677074',
    'PageNumber': '84',
    '_ga_HMZ6W68XKJ': 'GS1.1.1744292222.2.1.1744295677.0.0.0',
    't3_sid_7712007': 's1.1572165454.1744292222446.1744295695267.2.77.13.1',
    'sma_index_activity': '57856',
    '_ga_S54RCJCKRX': 'GS1.1.1744292222.2.1.1744295697.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'apiclient': 'FSK',
    'priority': 'u=1, i',
    'referer': 'https://fsk.ru/saburovo-club/cottages?sort=price&discount=&order=1',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1744191067563188896; _ym_d=1744191067; flomni_641ae9eee9a473ff3717a7c0={%22userHash%22:%22f0b86d1a-2b92-4eaa-bfb3-411145959846%22}; scbsid_old=2796070936; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _gcl_au=1.1.1359056039.1744191068; adtech_uid=817cec93-8f65-496f-91b1-3a898d61083d%3Afsk.ru; top100_id=t1.7712007.1435734598.1744191068028; _ga=GA1.1.873115281.1744191068; smFpId_old_values=%5B%2204b0ffbac42ccceb635ec5bff5b15618%22%5D; SCBstart=1744191068373; SCBporogAct=5000; SCBFormsAlreadyPulled=true; _fsid=s%3AYTHH2LngDmQ0iiCDQi77veYJTCf2f71_.ifth3uYXMV4LF%2Fhdx5j8zrZxhFaI1uFJI16ULXn%2Fr84; _ym_isad=1; _cmg_csstxWdO1=1744292222; _comagic_idxWdO1=10222016746.14429217501.1744292223; _ym_visorc=b; sma_session_id=2256955299; SCBnotShow=-1; _qz_sess=7204e4fe-e1b6-4bcb-af17-e78b3010fa3c; _yasc=ToSC0m4k3r82nONfA8OoqGzP7MVSMFOlAGZLLN4FEiUf0CiNYI7wgzRRHaKTwCSHDqAP; startSession=true; gtm_session_start=1744294024174; sma_postview_ready=1; gtm_session_threshold=true; floodLigth_session=fa514d1259b02; mindboxDeviceUUID=5bffbc54-9cb5-4220-a55d-d406d5c3b8d1; directCrm-session=%7B%22deviceGuid%22%3A%225bffbc54-9cb5-4220-a55d-d406d5c3b8d1%22%7D; SCBindexAct=2086; pageviewTimerOther=3269.2530000000006; startDate=1744295677074; PageNumber=84; _ga_HMZ6W68XKJ=GS1.1.1744292222.2.1.1744295677.0.0.0; t3_sid_7712007=s1.1572165454.1744292222446.1744295695267.2.77.13.1; sma_index_activity=57856; SCBindexAct=2047; _ga_S54RCJCKRX=GS1.1.1744292222.2.1.1744295697.0.0.0',
}

params = {
    'complex_slug': 'saburovo-club',
    'limit': '1000',
}

response = requests.get('https://fsk.ru/api/v3/suburban/all', params=params, headers=headers)

flats = []

print(response)
def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


items = response.json()

count = 0
for i in items:
    count += 1
    try:
        url = i["externalId"]
        date = datetime.date.today()
        project = i["project"]["title"]
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
        developer = "ФСК"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i["corpus"]["number"]
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'коттедж'
        finish_type = i["labels"][2]["title"]

        if finish_type=='Чистовая отделка':
            finish_type='С отделкой'

        room_count = int(i["crmRoomsQty"])
        area = i["areaTotal"]
        price_per_metr = ''
        old_price = i["priceWoDiscount"]
        price_per_metr_new = ''
        price = i["price"]
        section = i["section"]["number"]
        floor = i["floor"]["number"]
        flat_number = ''

        if old_price == price:
            price = None

    except IndexError:
        finish_type = i["labels"][1]["title"]

    print(
        f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
              distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
              konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, '',
              price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)
sleep_time = random.uniform(10, 15)
time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)
