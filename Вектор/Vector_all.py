import datetime
import random
import time
import requests
from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

cookies = {
    '_ym_uid': '1744104695302199556',
    '_ym_d': '1764660118',
    'session': '1355e16a18b8a072d588e74619e97339c8c0e0c9e054a3105ca7435975e04f8e',
    'scbsid_old': '2746015342',
    '_ym_visorc': 'w',
    '_ym_isad': '2',
    '_cmg_cssts_GL1': '1768918211',
    '_comagic_ids_GL1': '10290164232.14388966497.1768918211',
    'sma_session_id': '2571564515',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    'smFpId_old_values': '%5B%22adc7bfa5e8d60750384d8bfb80914db5%22%5D',
    'SCBnotShow': '-1',
    'SCBstart': '1768918212668',
    'SCBporogAct': '5000',
    'sma_postview_ready': '1',
    'SCBFormsAlreadyPulled': 'true',
    'SCBindexAct': '3521',
    'sma_index_activity': '14043',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://xn--b1agpqkk.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn--b1agpqkk.xn--p1ai/flats?order_by=price&view=cards&limit=15&complex_id=5eb5e039-f396-486f-9203-f48bac969c38&complex_id=77e4ef67-1f13-436a-99c4-385b4c89fe0a&complex_id=18f3c34e-b979-4617-bd05-541e9cf7abf0&complex_id=291888cd-5e18-40d5-851b-89ba7ff74d92&complex_id=b2c2d339-3d20-4884-90ca-9e57dab89026',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'x-host': 'xn--b1agpqkk.xn--p1ai',
    # 'cookie': '_ym_uid=1744104695302199556; _ym_d=1764660118; session=1355e16a18b8a072d588e74619e97339c8c0e0c9e054a3105ca7435975e04f8e; scbsid_old=2746015342; _ym_visorc=w; _ym_isad=2; _cmg_cssts_GL1=1768918211; _comagic_ids_GL1=10290164232.14388966497.1768918211; sma_session_id=2571564515; SCBfrom=https%3A%2F%2Fyandex.ru%2F; smFpId_old_values=%5B%22adc7bfa5e8d60750384d8bfb80914db5%22%5D; SCBnotShow=-1; SCBstart=1768918212668; SCBporogAct=5000; sma_postview_ready=1; SCBFormsAlreadyPulled=true; SCBindexAct=3521; sma_index_activity=14043',
}

json_data = {
    'project_id': '470f1d6c-84cb-43dc-9058-5d2583e3bfb0',
    'filters': [
        {
            'id': 'status',
            'type': 'system',
            'filter_type': 'select',
            'value': [
                'free',
            ],
        },
        {
            'id': 'complex_id',
            'type': 'system',
            'filter_type': 'select',
            'value': [
                '5eb5e039-f396-486f-9203-f48bac969c38',
                '77e4ef67-1f13-436a-99c4-385b4c89fe0a',
                '18f3c34e-b979-4617-bd05-541e9cf7abf0',
                '291888cd-5e18-40d5-851b-89ba7ff74d92',
                'b2c2d339-3d20-4884-90ca-9e57dab89026',
            ],
        },
    ],
    'order_by': [
        'price',
    ],
    'limit': 16,
    'offset': 0,
}

flats = []
count = 0

while True:

    try:
        response = requests.post(
            'https://xn--b1agpqkk.xn--p1ai/api/realty-filter/custom/real-estates',
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        if response.status_code == 200:
            data = response.json()

            for i in data:
                try:
                    count += 1
                    date = datetime.date.today()
                    project = i['project_name']
                    developer = "Вектор"
                    if project == 'Одинцовские кварталы':
                        korpus = i['building_number'].replace('ЖК «Одинцовские кварталы» ', '')
                    else:
                        korpus = i['building_int_number']
                    room_count = i['rooms']
                    if i['type'] == 'flat':
                        type_ = 'Квартиры'
                    area = i['total_area']
                    old_price = i['old_price']
                    price = i['price']
                    section = i['section_number']
                    floor = i['floor_number']

                    if old_price == price:
                        price = None

                    print(
                        f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                    result = [
                        date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                        '', '', '', developer, '', '', '', '', str(korpus), '', '', '', '',
                        '', '', type_, 'Без отделки', room_count, area, '', old_price, '',
                        '', price, section, str(floor), ''
                    ]
                    flats.append(result)

                except Exception as e:
                    print(f"Ошибка при обработке квартиры: {e}")
                    continue

            if not data:
                break
            json_data['offset'] = str(int(json_data['offset']) + 16)
            sleep_time = random.uniform(1, 3)
            time.sleep(sleep_time)


        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')

    except Exception as e:
        print(f"Общая ошибка: {e}")



if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
