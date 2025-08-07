import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

cookies = {
    '_ym_uid': '1744033734414468505',
    '_ym_d': '1744033734',
    '_ga': 'GA1.1.283748272.1744033734',
    '_ym_visorc': 'w',
    'cted': 'modId%3Dd9btzfb9%3Bclient_id%3D283748272.1744033734%3Bya_client_id%3D1744033734414468505',
    '_ym_isad': '1',
    '_ct_ids': 'd9btzfb9%3A51796%3A787982751',
    '_ct_session_id': '787982751',
    '_ct_site_id': '51796',
    'call_s': '___d9btzfb9.1744035543.787982751.251584:769934.251592:769949.253937:769953.282082:833891|2___',
    '_ct': '2100000000443421529',
    '_ct_client_global_id': '8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4',
    'marquiz__url_params': '{}',
    'marquiz__count-opened_67b73f0880994700195d7188': '1',
    '_ga_MCG2VSJR9E': 'GS1.1.1744033733.1.1.1744033759.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://river-house.ru/by-params/flat/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1744033734414468505; _ym_d=1744033734; _ga=GA1.1.283748272.1744033734; _ym_visorc=w; cted=modId%3Dd9btzfb9%3Bclient_id%3D283748272.1744033734%3Bya_client_id%3D1744033734414468505; _ym_isad=1; _ct_ids=d9btzfb9%3A51796%3A787982751; _ct_session_id=787982751; _ct_site_id=51796; call_s=___d9btzfb9.1744035543.787982751.251584:769934.251592:769949.253937:769953.282082:833891|2___; _ct=2100000000443421529; _ct_client_global_id=8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4; marquiz__url_params={}; marquiz__count-opened_67b73f0880994700195d7188=1; _ga_MCG2VSJR9E=GS1.1.1744033733.1.1.1744033759.0.0.0',
}

url = 'https://river-house.ru/api/property/find?type=flat&price=10764600,52197600'

flats = []
count = 1

response = requests.get(url, cookies=cookies, headers=headers)
if response.status_code == 200:
    item = response.json()
    items = item.get("properties", [])

    for i in items:
        date = datetime.date.today()
        developer = 'Риверхаус'
        project = 'RIVER HOUSE'
        korpus = '1'
        room_count = i['rooms_amount']
        finish_type = i['facing'].capitalize()
        if finish_type == 'Чистовая':
            finish_type = "С отделкой"

        type = 'Квартира'
        area = i['areaTotal']
        old_price = i['priceTotal']
        price = i['priceWithDiscount']
        section = i['sectionNumber']
        floor = i['floor']

        if old_price == price:
            price = None

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, finish_type, room_count, area, '', old_price, '', '', price,
                  section, floor, '']
        flats.append(result)
        count += 1
else:
    print(f'Ошибка: {response.status_code}')

time.sleep(0.05)

developer = 'Риверхаус'
project = 'RIVER HOUSE'
save_flats_to_excel(flats, project, developer)
