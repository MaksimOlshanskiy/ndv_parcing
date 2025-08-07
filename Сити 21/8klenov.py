import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

cookies = {
    'PHPSESSID': 'MXoa0cuBz7iBQSGYWx5BEO3GZXi9hiMR',
    '_ym_uid': '1742305489952440929',
    '_ym_d': '1742305489',
    '_gcl_au': '1.1.1128556968.1742305489',
    '_utm_source': 'site-city',
    '_utm_medium': 'ref',
    '_utm_campaign': '8klenov-card',
    '_utm_term': 'undefined',
    '_utm_content': 'undefined',
    '_ym_isad': '1',
    '_ga': 'GA1.1.1600517888.1742305490',
    '_ym_visorc': 'w',
    '_ct_ids': 'no7t230j%3A35508%3A835571056',
    '_ct_session_id': '835571056',
    '_ct_site_id': '35508',
    'call_s': '___no7t230j.1742307289.835571056.131369:559446|2___',
    '_ct': '1300000000516827089',
    '_ct_client_global_id': 'b7bf8ff5-0827-5c41-830e-bad9491c1c5e',
    'cted': 'modId%3Dno7t230j%3Bclient_id%3D1600517888.1742305490%3Bya_client_id%3D1742305489952440929',
    'modal_banner': 'MjguMTIuMjAyNCAxNTowODoxNg%3D%3D',
    '_pageCount': '3',
    '_ga_8DPHDXBM98': 'GS1.1.1742305489.1.1.1742305760.60.0.0',
    'sessionTime': '280',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'priority': 'u=1, i',
    'referer': 'https://xn--8-dtbitfnh.xn--p1ai/flats/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=MXoa0cuBz7iBQSGYWx5BEO3GZXi9hiMR; _ym_uid=1742305489952440929; _ym_d=1742305489; _gcl_au=1.1.1128556968.1742305489; _utm_source=site-city; _utm_medium=ref; _utm_campaign=8klenov-card; _utm_term=undefined; _utm_content=undefined; _ym_isad=1; _ga=GA1.1.1600517888.1742305490; _ym_visorc=w; _ct_ids=no7t230j%3A35508%3A835571056; _ct_session_id=835571056; _ct_site_id=35508; call_s=___no7t230j.1742307289.835571056.131369:559446|2___; _ct=1300000000516827089; _ct_client_global_id=b7bf8ff5-0827-5c41-830e-bad9491c1c5e; cted=modId%3Dno7t230j%3Bclient_id%3D1600517888.1742305490%3Bya_client_id%3D1742305489952440929; modal_banner=MjguMTIuMjAyNCAxNTowODoxNg%3D%3D; _pageCount=3; _ga_8DPHDXBM98=GS1.1.1742305489.1.1.1742305760.60.0.0; sessionTime=280',
}

base_url = 'https://xn--8-dtbitfnh.xn--p1ai/ajax/flats/'

flats = []
page = 1
count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while True:
    # Обновляем параметр page в params
    params = {
        'filter[price][]': [
            '9.20',
            '28.00',
        ],
        'sort[price]': '1',
        'page': str(page),
        'cnt': '30',
    }

    response = requests.get(base_url, params=params, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("data", [])

        if not items:
            break

        for i in items:
            date = datetime.date.today()
            project = '8 Кленов'
            status = ''
            developer = 'Сити21'
            district = ''
            korpus = i["building"]
            room_count = i["rooms"]
            type = 'Квартира'
            finish_type = "Без отделки"
            area = float(i["sq"])

            try:
                old_price = int(i["costact"].replace(' ', ''))
            except:
                old_price = int(i["price"].replace(' ', ''))

            price = int(i["price"].replace(' ', ''))
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
    page += 1

    time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
