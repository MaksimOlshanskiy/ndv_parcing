import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests

cookies = {
    'session': 'c31a8b19aa634080295c680e3d48da7361001e4794483b42bc5d46342bc01e1a',
    '_ym_uid': '1743664134852279801',
    '_ym_d': '1743664134',
    'ab_id': '59bc78367ea271ab2b1a6fbbfc5bfbada4cbdf9c',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '_ct_ids': 'q0o82mvs%3A59204%3A350209434',
    '_ct_session_id': '350209434',
    '_ct_site_id': '59204',
    'call_s': '___q0o82mvs.1743665934.350209434.401154:1128434|2___',
    '_ct': '2400000000242114272',
    '_ct_client_global_id': '8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4',
    'cted': 'modId%3Dq0o82mvs%3Bya_client_id%3D1743664134852279801',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://elyon-dom.ru/flats',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-host': 'elyon-dom.ru',
    # 'cookie': 'session=c31a8b19aa634080295c680e3d48da7361001e4794483b42bc5d46342bc01e1a; _ym_uid=1743664134852279801; _ym_d=1743664134; ab_id=59bc78367ea271ab2b1a6fbbfc5bfbada4cbdf9c; _ym_isad=1; _ym_visorc=w; _ct_ids=q0o82mvs%3A59204%3A350209434; _ct_session_id=350209434; _ct_site_id=59204; call_s=___q0o82mvs.1743665934.350209434.401154:1128434|2___; _ct=2400000000242114272; _ct_client_global_id=8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4; cted=modId%3Dq0o82mvs%3Bya_client_id%3D1743664134852279801',
}

params = {
    'project_id': '47a73581-dcfe-4d33-9a31-dfeced4e25c9',
    'status': 'free',
    'offset': '0',
    'limit': '70',
    'order_by': 'discount_value',
}

flats = []
count=0

try:
    response = requests.get('https://elyon-dom.ru/api/realty-filter/residential/real-estates',
                            params=params,
                            headers=headers,
                            cookies=cookies)

    if response.status_code == 200:
        data = response.json()

        for i in data:
            try:
                count+=1
                date = datetime.date.today()
                project = 'ЭЛЬЙОН'
                developer = "ГК Монолит"
                korpus = "1"
                room_count = i['rooms']
                type_ = "Квартира"

                if i['finishing_type'] == 'no':
                    finish_type = 'Без отделки'
                else:
                    finish_type = "С отделкой"

                area = i['total_area']
                price_per_metr = i['old_ppm']
                old_price = i['old_price']
                price_per_metr_new = i['ppm']
                price = i['price']
                section = i['section_number']
                floor = i['floor_number']

                if old_price==price:
                    price=None

                print(
                    f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, finish_type, room_count, area, '', int(old_price), '',
                    '', price, section, floor, ''
                ]
                flats.append(result)

            except Exception as e:
                print(f"Ошибка при обработке квартиры: {e}")
                continue

    else:
        print(f'Ошибка запроса: {response.status_code}, {response.text}')

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
