import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'priority': 'u=1, i',
    'referer': 'https://varshavskaya.life/plans/search',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

url = 'https://varshavskaya.life/hydra/json/data.json'

flats = []
count = 1

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    items = data.get('apartments', {})

    for i, j in items.items():
        st = j.get('st', '')
        if st == 1:
            date = datetime.date.today()
            project = 'Life Варшавская'
            developer = 'Pioneer'
            korpus = j.get('b', '')
            room_count = j.get('rc', '')

            if room_count == 0:
                room_count = 'студия'

            finish_type = j.get("renovation", '')
            if finish_type == 0:
                finish_type = 'Без отделки'
            else:
                finish_type = 'С отделкой'

            type = 'Квартира'
            area = j.get("sq", '')
            old_price = j.get("tc", '')
            price = j.get("tcd", '')
            floor = j.get('f', '')

            if old_price == price:
                price = None

            print(
                f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '',
                      '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                      '', '', type, finish_type, room_count, area, '', old_price, '', '', price,
                      '', floor, '']
            flats.append(result)
            count += 1
        else:
            continue
else:
    print(f'Ошибка: {response.status_code}')

time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
