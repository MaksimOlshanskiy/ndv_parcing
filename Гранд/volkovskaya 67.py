import datetime

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests

cookies = {
    '_ym_uid': '1743666843229524173',
    '_ym_d': '1743666843',
    'cted': 'modId%3Dgav3hfl5%3Bya_client_id%3D1743666843229524173',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://dev.volkovskaya67.ru/flats',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1743666843229524173; _ym_d=1743666843; cted=modId%3Dgav3hfl5%3Bya_client_id%3D1743666843229524173',
}

flats = []
count = 0

try:
    response = requests.get('https://dev.volkovskaya67.ru/api/property',
                            headers=headers,
                            cookies=cookies)

    if response.status_code == 200:
        data = response.json()

        for i in data:
            try:
                if i['type'] in ['КЛ', 'ММ']:
                    continue

                count += 1
                date = datetime.date.today()
                project = 'Волковская 67'
                developer = "Гранд"
                korpus = i['house']
                room_count = i['rooms']

                if room_count == 0:
                    room_count = 'студия'

                type_ = "Апартаменты"

                if i['decorationName'] in ['Модерн', 'Классика']:
                    finish_type = 'С отделкой'
                else:
                    finish_type = i['decorationName']
                    if finish_type == 'WhiteBox':
                        finish_type = 'Предчистовая'

                area = i['space']
                price_per_metr = ''
                old_price = int(round(i['price'], 0))
                price_per_metr_new = ''
                price = int(round(i['discountedPrice'], 0))
                section = i['section']
                floor = i['floor']

                if old_price == price:
                    price = None

                print(
                    f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, finish_type, room_count, area, price_per_metr, old_price, '',
                    price_per_metr_new, price, int(section), int(str(floor)), ''
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
