import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all
import requests

# Настройки для запросов
cookies = {
    '_ga': 'GA1.1.1741273793.1741952312',
    '_ym_uid': '1741952312566257547',
    '_ym_d': '1741952312',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    'call_s': '___vfeqtpoq.1741955041.221305338.350730:1051545|2___',
    '_ga_5CZP01QN0D': 'GS1.1.1741952312.1.1.1741953434.60.0.166441258',
    'csrftoken': 'ZmMWTlcN23nUoPhNpAZCC31TgkjfjGna',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'origin': 'https://xn--80aaijj0ai2m.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn--80aaijj0ai2m.xn--p1ai/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

params = {
    'sort': 'default',
}

base_url = 'https://xn--h1ana.xn--80aaijj0ai2m.xn--p1ai/api/v1/estate/catalog/'

url = base_url
page_number = 1  # Счетчик страниц
flats = []
count = 0

while url:
    print(f"Обрабатываю страницу {page_number}")

    params['page'] = page_number

    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    if response.status_code == 200:
        data = response.json()

        items = data.get("results", [])
        print(f"Найдено квартир на странице: {len(items)}")

        for i in items:
            count += 1
            date = datetime.date.today()
            project = i["data"]["classifier_name"]
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
            developer = "Мангазея"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = i["data"]["corp_number"]
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = 'Квартира'

            index_finish = len(i["data"]["params"])
            finish_type = i["data"]["params"][index_finish - 1]["value"]
            room_count = i["data"]["rooms"]

            if room_count == 0:
                room_count = 'студия'

            area = i["data"]["space"]
            price_per_metr = ''
            try:
                old_price = i["data"]["base_price"]
            except:
                old_price = i["data"]["price"]
            discount = ''
            price_per_metr_new = ''
            price = i["data"]["price"]
            section = ''
            floor = i["data"]["floor"]
            flat_number = ''

            if old_price == price:
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
        page_number += 1
    else:
        print(f'Ошибка: {response.status_code}')
        break

    time.sleep(0.3)

project = 'all'
save_flats_to_excel(flats, project, developer)
