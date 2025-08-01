import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_far

cookies = {
    'session': '1aad8d5d51b5b961e02a276addf723989d7c5b2375201adea4bed865f1bd15e9',
    '_ym_uid': '1744363846146011718',
    '_ym_d': '1744363846',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '_cmg_csste9LcR': '1744363846',
    '_comagic_ide9LcR': '10127062073.14342295148.1744363846',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://zogorod.ru/flats',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-host': 'zogorod.ru',
    # 'cookie': 'session=1aad8d5d51b5b961e02a276addf723989d7c5b2375201adea4bed865f1bd15e9; _ym_uid=1744363846146011718; _ym_d=1744363846; _ym_isad=1; _ym_visorc=w; _cmg_csste9LcR=1744363846; _comagic_ide9LcR=10127062073.14342295148.1744363846',
}

flats = []
limit = 100
offset = 0
total_flats = 0
processed_flats = 0
count = 0

try:

    initial_params = {
        'project_id': 'ae0c1d6b-e7e8-48be-b83f-fc11f24335a6',
        'status': 'free',
        'offset': 0,
        'limit': 1,  # Минимальный запрос для получения метаданных
        'order_by': 'price',
    }

    initial_response = requests.get('https://zogorod.ru/api/realty-filter/residential/real-estates',
                                    params=initial_params,
                                    headers=headers,
                                    cookies=cookies)

    if initial_response.status_code == 200:
        initial_data = initial_response.json()
        total_flats = len(initial_data)
        total_flats = 206

        print(f"Всего квартир: {total_flats}")

        # Запрашиваем данные пачками по limit записей
        while offset < total_flats:
            params = {
                'project_id': 'ae0c1d6b-e7e8-48be-b83f-fc11f24335a6',
                'status': 'free',
                'offset': offset,
                'limit': limit,
                'order_by': 'price',
            }

            response = requests.get('https://zogorod.ru/api/realty-filter/residential/real-estates',
                                    params=params,
                                    headers=headers,
                                    cookies=cookies)

            if response.status_code == 200:
                data = response.json()
                current_batch = len(data)
                processed_flats += current_batch

                for i in data:
                    try:
                        count += 1
                        date = datetime.date.today()
                        project = 'Зеленый город'
                        developer = "ИММО ДЕВЕЛОПМЕНТ"
                        korpus = i['building_number'].replace('Дом ', '')
                        room_count = i['rooms']

                        if room_count == 0:
                            room_count = 'студия'

                        type_ = "Квартира"

                        if i['finishing_type'] == 'no':
                            finish_type = 'Без отделки'
                        else:
                            finish_type = "С отделкой"

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
                            '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                            '', '', type_, finish_type, room_count, area, '', old_price, '',
                            '', price, section, int(str(floor)), ''
                        ]
                        flats.append(result)

                    except Exception as e:
                        print(f"Ошибка при обработке квартиры: {e}")
                        continue

                offset += limit
                print(f"Обработано {processed_flats} из {total_flats} квартир")

                time.sleep(1)
            else:
                print(f'Ошибка запроса: {response.status_code}, {response.text}')
                break
    else:
        print(f'Ошибка начального запроса: {initial_response.status_code}, {initial_response.text}')

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
