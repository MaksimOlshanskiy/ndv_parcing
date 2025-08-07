import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    '_ct_ids': '717vu2vs%3A42667%3A562389345',
    '_ct_session_id': '562389345',
    '_ct_site_id': '42667',
    'call_s': '___717vu2vs.1742560558.562389345.179874:554948|2___',
    '_ct': '1700000000369969978',
    '_ct_client_global_id': 'b7bf8ff5-0827-5c41-830e-bad9491c1c5e',
    '_ga': 'GA1.2.1896431650.1742558765',
    '_gid': 'GA1.2.1523996016.1742558765',
    '_gat_UA-162478415-10': '1',
    '_ym_uid': '1742558765988001932',
    '_ym_isad': '1',
    '_ga_QVYHN51256': 'GS1.2.1742558765.1.0.1742558765.60.0.0',
    '_ym_visorc': 'w',
    'cted': 'modId%3D717vu2vs%3Bclient_id%3D1896431650.1742558765%3Bya_client_id%3D1742558765988001932',
    '_ym_d': '1742558769',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://westtower.ru/filter',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-site': 'westtower.ru',
    # 'cookie': '_ct_ids=717vu2vs%3A42667%3A562389345; _ct_session_id=562389345; _ct_site_id=42667; call_s=___717vu2vs.1742560558.562389345.179874:554948|2___; _ct=1700000000369969978; _ct_client_global_id=b7bf8ff5-0827-5c41-830e-bad9491c1c5e; _ga=GA1.2.1896431650.1742558765; _gid=GA1.2.1523996016.1742558765; _gat_UA-162478415-10=1; _ym_uid=1742558765988001932; _ym_isad=1; _ga_QVYHN51256=GS1.2.1742558765.1.0.1742558765.60.0.0; _ym_visorc=w; cted=modId%3D717vu2vs%3Bclient_id%3D1896431650.1742558765%3Bya_client_id%3D1742558765988001932; _ym_d=1742558769',
}

params = {
    'limit': '8',
}

url = 'https://westtower.ru/api/flat/'

flats = []
count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("results", [])

        for i in items:
            date = datetime.date.today()
            project = "West Tower"
            developer = 'Ташир'
            room_count = i["rooms"]

            if room_count == 0:
                room_count = 'студия'

            type = 'Апартаменты'
            finish_type = 'Предчистовая'
            area = i["area"]
            old_price = i["origin_price"]
            price = i["price"]
            section = i["section_number"]
            floor = i["floor_number"]

            if old_price == price:
                price = None

            print(
                f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '',
                      '', '', '', '', '', developer, '', '', '', '', '1', '', '', '', '',
                      '', '', type, finish_type, room_count, area, '', old_price, '', '', price,
                      section, floor, '']
            flats.append(result)
            count += 1
        # Проверяем, есть ли следующая страница
        next_url = item.get("next")
        if next_url:
            url = next_url  # Переходим на следующую страницу
            params = {}  # Очищаем параметры, так как URL следующей страницы уже содержит их
        else:
            break  # Если следующей страницы нет, выходим из цикла
    else:
        print(f'Ошибка: {response.status_code}')
        break

    time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
