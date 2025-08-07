import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
import requests

cookies = {
    'optimizelyEndUserId': 'oeu1744213120792r0.028752513041990002',
    'optimizelySegments': '%7B%222340150041%22%3A%22false%22%2C%222347740017%22%3A%22gc%22%2C%222347760012%22%3A%22direct%22%7D',
    'optimizelyBuckets': '%7B%7D',
    'optimizelyPendingLogEvents': '%5B%5D',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=0, i',
    'referer': 'https://sholohovo.ru/search',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'optimizelyEndUserId=oeu1744213120792r0.028752513041990002; optimizelySegments=%7B%222340150041%22%3A%22false%22%2C%222347740017%22%3A%22gc%22%2C%222347760012%22%3A%22direct%22%7D; optimizelyBuckets=%7B%7D; optimizelyPendingLogEvents=%5B%5D',
}

url = 'https://sholohovo.ru/assets/js/data.json?v1745484089678&_=1745484089679'

flats = []
count = 1

response = requests.get(url, cookies=cookies, headers=headers, verify=False)

if response.status_code == 200:
    data = response.json()
    items = data.get('apartments', {})
    for i, j in items.items():
        if j['st'] != 1:
            continue

        count += 1
        date = datetime.date.today()
        project = 'Шолохово'
        developer = 'РосЕвроСити'
        korpus = j.get('b', '')
        room_count = j.get('rc', '')

        if room_count == 0:
            room_count = 'студия'

        finish_type = j.get("decor", '')

        if finish_type == 'Есть':
            finish_type = 'С отделкой'
        else:
            finish_type = 'Без отделки'

        type = 'Квартира'
        area = j.get("sq", '')
        old_price = j.get('tc', '')
        discount = j.get('percent', '')
        price = j.get("tc", '')
        floor = j.get('f', '')
        section = j.get('s', '')

        if old_price == price:
            price = None

        print(
            f"{count}| {i} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, finish_type, room_count, area, '', old_price, discount, '', price,
                  section, floor, '']
        flats.append(result)
else:
    print(f'Ошибка: {response.status_code}')

time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
