import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests

cookies = {
    '_ga_B4ZS2CG2Y3': 'GS1.1.1743515983.1.0.1743515983.0.0.0',
    '_ga': 'GA1.1.1441621149.1743515983',
    '_ym_uid': '1743515984211597661',
    '_ym_d': '1743515984',
    '_ym_visorc': 'w',
    'marquiz__url_params': '{}',
    'cted': 'modId%3Dmd2kejyn%3Bclient_id%3D1441621149.1743515983%3Bya_client_id%3D1743515984211597661',
    '_ym_isad': '1',
    '_ct_site_id': '66211',
    '_ct_ids': 'md2kejyn%3A66211%3A212669419',
    '_ct_session_id': '212669419',
    'call_s': '___md2kejyn.1743517784.212669419.392361:1102438|2___',
    '_ct': '2700000000148250023',
    '_ct_client_global_id': '3db326d5-8cce-5878-a408-3c38a7df2fb2',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'if-none-match': 'W/"f336-9EJ7i+VSkNAfZp/nESoYR0V631Y"',
    'priority': 'u=1, i',
    'referer': 'https://malahovkahouse.ru/flats?space=21,64',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_ga_B4ZS2CG2Y3=GS1.1.1743515983.1.0.1743515983.0.0.0; _ga=GA1.1.1441621149.1743515983; _ym_uid=1743515984211597661; _ym_d=1743515984; _ym_visorc=w; marquiz__url_params={}; cted=modId%3Dmd2kejyn%3Bclient_id%3D1441621149.1743515983%3Bya_client_id%3D1743515984211597661; _ym_isad=1; _ct_site_id=66211; _ct_ids=md2kejyn%3A66211%3A212669419; _ct_session_id=212669419; call_s=___md2kejyn.1743517784.212669419.392361:1102438|2___; _ct=2700000000148250023; _ct_client_global_id=3db326d5-8cce-5878-a408-3c38a7df2fb2',
}

params = ''

url = 'https://malahovkahouse.ru/api/property/find'

flats = []
count = 1

response = requests.get(url, cookies=cookies, headers=headers)
if response.status_code == 200:
    item = response.json()
    items = item.get("properties", [])

    for i in items:
        date = datetime.date.today()
        project = 'Дом в Малаховке'
        developer = 'АМ Девелопмент'
        korpus = i['house']
        room_count = i['rooms']

        if room_count == 0:
            room_count = 'студия'

        finish_type = i['decorationName']
        if finish_type=='WhiteBox':
            finish_type='Предчистовая'
        elif finish_type in ['Классика','Модерн']:
            finish_type='С отделкой'
        type = 'Квартира'
        area = i['space']
        old_price = i['price']
        ppm = ''
        price = i['discountedPrice']
        section = i['section']
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

save_flats_to_excel(flats, project, developer)
