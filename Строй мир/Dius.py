import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

cookies = {
    '_ym_uid': '1745504348684550748',
    '_ym_d': '1745504348',
    'session': '256a9bd765b8d54176437921c8086e4b12ba78c5b27a6ca6ff44642156078e0b',
    '_ct': '3200000000031246565',
    '_ct_client_global_id': '8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4',
    'cted': 'modId%3Dqep3qap0%3Bya_client_id%3D1745504348684550748',
    '_ym_isad': '1',
    '_ct_ids': 'qep3qap0%3A74586%3A65831429',
    '_ct_session_id': '65831429',
    '_ct_site_id': '74586',
    'call_s': '___qep3qap0.1753367883.65831429.477004:1355648|2___',
    '_ym_visorc': 'w',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://dius-mfk.ru/flats',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-host': 'dius-mfk.ru',
    # 'cookie': '_ym_uid=1745504348684550748; _ym_d=1745504348; session=256a9bd765b8d54176437921c8086e4b12ba78c5b27a6ca6ff44642156078e0b; _ct=3200000000031246565; _ct_client_global_id=8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4; cted=modId%3Dqep3qap0%3Bya_client_id%3D1745504348684550748; _ym_isad=1; _ct_ids=qep3qap0%3A74586%3A65831429; _ct_session_id=65831429; _ct_site_id=74586; call_s=___qep3qap0.1753367883.65831429.477004:1355648|2___; _ym_visorc=w',
}

limit = 100  # максимальный лимит, который принимает сервер
offset = 0
flats = []
count = 0

while True:
    params = {
        'project_id': '4092660e-34ee-4a05-8672-dbbe2d80b133',
        'status': 'free',
        'offset': str(offset),
        'limit': str(limit),
    }
    try:
        response = requests.get('https://dius-mfk.ru/api/realty-filter/residential/real-estates',
                                params=params,
                                headers=headers,
                                cookies=cookies)

        if response.status_code == 200:
            data = response.json()

            if not data:  # если пустой ответ, значит данные кончились
                print("Данных больше нет, выходим из цикла")
                break

            for i in data:
                try:
                    count += 1
                    date = datetime.date.today()
                    project = 'DIUS'
                    developer = "Строй мир"
                    korpus = '1'
                    room_count = i['rooms']

                    if room_count == 0:
                        room_count = 'студия'

                    type_ = "Апартамент"
                    area = i['total_area']
                    old_price = i.get('old_price', 0)
                    price = int(round(i.get('price', 0),0))
                    section = i.get('section_number', 0)
                    floor = i.get('floor_number', 0)

                    if old_price == price:
                        price = None

                    print(
                        f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                    result = [
                        date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                        '', '', '', developer, '', '', '', '', korpus if korpus else '',
                        '', '', '', '', '', '', type_, 'Без отделки', room_count, area,
                        '', old_price, '', '', price,
                        int(section) if section else 0, int(floor) if floor else 0, ''
                    ]
                    flats.append(result)

                except Exception as e:
                    print(f"Ошибка при обработке квартиры: {e}")
                    continue

            offset += limit  # сдвигаем смещение для следующей страницы

        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')
            break  # прерываем цикл при ошибке

    except Exception as e:
        print(f"Общая ошибка: {e}")
        break

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
