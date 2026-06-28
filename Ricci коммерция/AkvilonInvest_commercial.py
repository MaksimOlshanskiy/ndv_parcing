import datetime
import time
import requests
from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

'''
Нужно удалять дубликаты! Их много
'''

import requests

cookies = {
    '_ym_uid': '1766409591278118085',
    '_ym_d': '1781785514',
    '_ymab_param': 'XihTyDNt60EsbX6JlF4afRo97NSexBGMQ-wgyB1mrk82LztsCcOdWtL0RwcOslQAqeOMRISgXDX2ER_s5poFAbuDhC0',
    '_ym_isad': '2',
    'cted': 'modId%3Daymg2z1m%3Bya_client_id%3D1766409591278118085',
    '_ym_visorc': 'w',
    'tmr_lvid': 'c6f40b3020c64e497af90dd4994ce2ff',
    'tmr_lvidTS': '1766409591431',
    'scbsid_old': '4097698043',
    '_ct_ids': 'aymg2z1m%3A52820%3A2296168908',
    '_ct_session_id': '2296168908',
    '_ct_site_id': '52820',
    'call_s': '___aymg2z1m.1781787311.2296168908.258214:781696|2___',
    '_ct': '800000001067238201',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'accept-cookie': 'true',
    'city': '2',
    'domain_sid': 'Kz0hF6pAifViYUOMnXzSL%3A1781785515485',
    'tmr_detect': '0%7C1781785516729',
    'sma_session_id': '2741267635',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    'SCBstart': '1781785551804',
    'smFpId_old_values': '%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D',
    'SCBporogAct': '5000',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'sma_index_activity': '4647',
    'SCBindexAct': '3897',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://msk.group-akvilon.ru/novostroyki/kommercheskaya-nedvizhimost/',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1766409591278118085; _ym_d=1781785514; _ymab_param=XihTyDNt60EsbX6JlF4afRo97NSexBGMQ-wgyB1mrk82LztsCcOdWtL0RwcOslQAqeOMRISgXDX2ER_s5poFAbuDhC0; _ym_isad=2; cted=modId%3Daymg2z1m%3Bya_client_id%3D1766409591278118085; _ym_visorc=w; tmr_lvid=c6f40b3020c64e497af90dd4994ce2ff; tmr_lvidTS=1766409591431; scbsid_old=4097698043; _ct_ids=aymg2z1m%3A52820%3A2296168908; _ct_session_id=2296168908; _ct_site_id=52820; call_s=___aymg2z1m.1781787311.2296168908.258214:781696|2___; _ct=800000001067238201; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; accept-cookie=true; city=2; domain_sid=Kz0hF6pAifViYUOMnXzSL%3A1781785515485; tmr_detect=0%7C1781785516729; sma_session_id=2741267635; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; SCBstart=1781785551804; smFpId_old_values=%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D; SCBporogAct=5000; SCBFormsAlreadyPulled=true; sma_postview_ready=1; sma_index_activity=4647; SCBindexAct=3897',
}

params = {

}

flats = []
count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])

    return int(digits) if digits else s

response = requests.get('https://msk.group-akvilon.ru/api/commercial/', params=params, cookies=cookies, headers=headers)
if response.status_code == 200:
    item = response.json()
    lots_count = item['count']
    print(lots_count)

while len(flats) < lots_count:
    response = requests.get('https://msk.group-akvilon.ru/api/commercial/', params=params, cookies=cookies, headers=headers)
    if response.status_code == 200:
        item = response.json()
        items = item.get("results", [])
        for i in items:
            date = datetime.date.today()
            project = i["project_title"].replace('Аквилон ', '').replace(' by Akvilon', '')
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
            developer = "Аквилон"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = i["building_number"].replace(' (for life)', '').replace(' (for business)', '')
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''

            srok_sdachi_old = f"{i['completion_quarter']} кв {i['completion_year']}"
            stadia = ''
            dogovor = ''
            type = 'Квартиры'
            area = float(i["area"])
            finish_type = ''
            room_count = ''
            price_per_metr = ''
            old_price = i["price"]
            discount = ''
            price_per_metr_new = ''
            price = i["price_promo"]
            section = ''
            floor = i["floor"]
            flat_number = ''

            if price == old_price:
                price = None

            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)

            count += 1

        # Проверяем, есть ли следующая страница
        if not items:
            break
        next_url = item.get("next")
        if next_url:
            url = next_url  # Переходим на следующую страницу
            params = {}  # Очищаем параметры, так как URL следующей страницы уже содержит их
        else:
            break  # Если следующей страницы нет, выходим из цикла
    else:
        print(f'Ошибка: {response.status_code}')
        break

    time.sleep(0.3)
project = 'all'
save_flats_to_excel(flats, project, developer, kvartirografia=False)
