import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_far
import requests

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://xn----ktbmbf3af6fk4a.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn----ktbmbf3af6fk4a.xn--p1ai/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}

params = {
    'storepartuid': '726063840041',
    'recid': '576086979',
    'c': '1748418774490',
    'slice': '1',
    'getparts': 'true',
    'size': '36',
}

url = 'https://store.tildaapi.com/api/getproductslist/'

flats = []
count = 1
max_slice = 2  # Максимальное число страниц

while int(params['slice']) <= max_slice:
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        break

    item = response.json()
    items = item.get("products", [])

    if not items:
        print("Нет данных, выходим из цикла.")
        break

    for i in items:
        date = datetime.date.today()
        project = 'Скрылья'
        developer = "Флагман"
        korpus = ''
        type = 'Квартира'
        finish_type = 'Без отделки'

        characteristics = i.get('characteristics', [])

        room_count = characteristics[1]['value'] if len(characteristics) > 1 else ''
        area = characteristics[2]['value'] if len(characteristics) > 2 else ''
        area=area.replace(',', '.')
        floor = characteristics[3]['value'].split('/')[0] if len(characteristics) > 3 else ''

        price = i.get('price', '0').split('.')[0]
        old_price = i.get('priceold', '0').split('.')[0]

        if old_price=='':
            old_price=price

        print(f"{count}, {project}, {finish_type}, тип: {type}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        flats.append([
            date, project, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", developer, '', "", "", "",
            korpus, "", "", "", "", "", "", type, finish_type, int(room_count), float(area), "", old_price, "", "", '', "",
            int(floor), ""
        ])
        count += 1

    params['slice'] = str(int(params['slice']) + 1)
    time.sleep(0.05)

project = 'Скрылья'
developer = "Флагман"
save_flats_to_excel(flats, f'{project} 1 комнатные', developer)

print(f"Данные сохранены")
