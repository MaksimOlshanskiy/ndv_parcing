import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    'is_light_theme': 'false',
    '_gcl_au': '1.1.753230018.1742559099',
    '_ct_ids': 'q4o4iqhw%3A31564%3A948753466',
    '_ct_session_id': '948753466',
    '_ct_site_id': '31564',
    '_ct': '1100000000647480272',
    '_ga': 'GA1.2.1560555958.1742559099',
    '_gid': 'GA1.2.554538425.1742559099',
    '_ct_client_global_id': 'b7bf8ff5-0827-5c41-830e-bad9491c1c5e',
    '_ym_uid': '1742559100680377093',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    'cted': 'modId%3Dq4o4iqhw%3Bclient_id%3D1560555958.1742559099%3Bya_client_id%3D1742559100680377093',
    '_gat_UA-127051324-3': '1',
    'call_s': '___q4o4iqhw.1742561083.948753466.108350:1049746|2___',
    '_ga_DBX9NGC6SD': 'GS1.2.1742559099.1.1.1742559289.46.0.0',
    '_ym_d': '1742559318',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru',
    'priority': 'u=1, i',
    'referer': 'https://stellarcity.ru/filter',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-site': 'stellarcity.ru',
    # 'cookie': 'is_light_theme=false; _gcl_au=1.1.753230018.1742559099; _ct_ids=q4o4iqhw%3A31564%3A948753466; _ct_session_id=948753466; _ct_site_id=31564; _ct=1100000000647480272; _ga=GA1.2.1560555958.1742559099; _gid=GA1.2.554538425.1742559099; _ct_client_global_id=b7bf8ff5-0827-5c41-830e-bad9491c1c5e; _ym_uid=1742559100680377093; _ym_isad=1; _ym_visorc=w; cted=modId%3Dq4o4iqhw%3Bclient_id%3D1560555958.1742559099%3Bya_client_id%3D1742559100680377093; _gat_UA-127051324-3=1; call_s=___q4o4iqhw.1742561083.948753466.108350:1049746|2___; _ga_DBX9NGC6SD=GS1.2.1742559099.1.1.1742559289.46.0.0; _ym_d=1742559318',
}

url = 'https://stellarcity.ru/api/flat/?&limit=6&offset=0&viewMode=rows&'

flats = []
count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("results", [])

        for i in items:
            date = datetime.date.today()
            project = "Stellar City"
            developer = 'Ташир'
            korpus = i["building_number"]
            room_count = i["rooms"]

            if room_count == 0:
                room_count = 'студия'

            type = 'Квартира'
            finish_type = i["facing"]

            if finish_type == 0:
                finish_type = 'Без отделки'
            else:
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

            result = [date, project, '', '', '', '', '', '',
                      '',
                      '', '', '',
                      '', '', '', '', '', developer, '', '', '', '', korpus,
                      '', '', '', '',
                      '', '', type, finish_type, room_count, area, '', old_price, '',
                      '', price, section, floor, '']
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
