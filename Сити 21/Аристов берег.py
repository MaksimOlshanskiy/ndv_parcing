import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

'''
Не делаем отдельную квартирографию, берём как есть
kvartirografia=False
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'origin': 'https://aristov-bereg.ru',
    'priority': 'u=1, i',
    'referer': 'https://aristov-bereg.ru/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

params = {
    'offset': '0',
}

base_url = 'https://api.aristov-bereg.ru/api/v1/choose/objects/'

flats = []
page = 1
count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while True:
    # Обновляем параметр page в params


    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("objects", [])

        for i in items:
            if i['id'] == 0:
                continue
            try:
                if i['is_promo']:
                    continue
            except:
                pass

            date = datetime.date.today()
            project = 'Аристов Берег'
            status = ''
            developer = 'Сити 21 век'
            district = ''
            try:
                korpus = i["building"]
            except:
                korpus = ''
            room_count = str(i["room"]).replace('0', 'студия')
            if i['euro'] is True:
                room_count += 'е'
            type = 'Квартира'
            finish_type = "Без отделки"
            area = float(i["area"])
            old_price = int(i["old_price"])
            price = int(i["price"])
            if old_price == 0:
                old_price = price

            section = i["section"]
            floor = i["floor"]

            if old_price == price:
                price = None

            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

            count += 1

            result = [date, project, '', '', '', '', '', '', '', '', '', '',
                      '', '', status, '', '', developer, '', district, '', '', korpus, '', '', '', '',
                      '', '', type, finish_type, room_count, area, '', old_price, '', '', price,
                      section, floor, '']
            flats.append(result)
    else:
        print(f'Ошибка: {response.status_code}')
        break

    # Увеличиваем номер страницы
    params['offset'] = str(int(params['offset']) + 12)

    if not response.json().get('show_more'):
        break

    time.sleep(0.3)

save_flats_to_excel(flats, project, developer, kvartirografia=False)
