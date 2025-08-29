import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

'''
заменить в headers authorization по ссылке https://xn--80abdl0adtby.xn--p1ai/#/catalog/projects/houses?filter=property.status:AVAILABLE
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjBiOWE0NDI3MTYxYTNhZThiZWRjNTc2YTdlODNkMmU0ZGZhMzE3ODI0OTllZWQzZDJkYjAwNjRmY2MyNGM2YzY1MzgxMWUzOGZkNTIzNDFiIiwiaWF0IjoxNzU1NzYyMDcyLjk4NzQxOCwibmJmIjoxNzU1NzYyMDcyLjk4NzQyMSwiZXhwIjoxNzU1NzY1NjcyLjk4MTk0NCwic3ViIjoiU0lURV9XSURHRVR8MTgxNCIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjQyNDIsInRpdGxlIjoi0J7QntCeINCT0YDQsNC90LQiLCJzdWJkb21haW4iOiJwYjQyNDIiLCJiaWxsaW5nT3duZXJJZCI6NDI1MCwiY291bnRyeUNvZGUiOiJSVSJ9LCJyb2xlcyI6WyJST0xFX1NJVEVfV0lER0VUIl0sInNpdGVXaWRnZXQiOnsiaWQiOjE4MTQsImRvbWFpbiI6Imh0dHBzOi8veG4tLTgwYWJkbDBhZHRieS54bi0tcDFhaSJ9fQ.RlTzIjOvbPvgb5yDc782isd7ZsVIxaKysxT-3V8fjqh49_q-JkEAFhenqGafDEJZIu0FBzmXTne-_if6sHI7DVaro9I3E0UUjU4OCMrg-criZT92iyJFPaY2Hbrk5alzf1FhaGGnHizoh0BYlukcS6My4ZlH5YbL18XSyfJLrbDqRK-k5aAmB63w4KdxBrytL1j2AqeHXMDdUAfctTuwYR5DA5BBaZewxs9FI-99sM3_rIobGxqOsRMGyhHj9L9NgVJbQmyOuUsDe_TFPowibLXSYRsPjV4imfjnN0-50rWNCSw2JIrXzF6trxbOekXqNbHQ81F1bYqRyMC2qLD09A',
    'origin': 'https://smart-catalog.profitbase.ru',
    'priority': 'u=1, i',
    'referer': 'https://smart-catalog.profitbase.ru/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}

params = {
    'propertyTypeAliases[0]': 'property',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'limit': '441',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []
count = 0
total_count = 0
offset = 0

try:
    while True:
        # Добавляем параметр offset для пагинации
        params_with_offset = params.copy()
        params_with_offset['offset'] = offset
        response = requests.get('https://pb4242.profitbase.ru/api/v4/json/property',
                                params=params_with_offset,
                                headers=headers)

        if response.status_code == 200:
            data = response.json()
            properties = data.get("data", {}).get('properties', [])
            filtered_count = data.get("data", {}).get('filteredCount', 0)

            # Если это первый запрос, получаем общее количество
            if offset == 0:
                total_count = filtered_count
                print(f"Всего доступно квартир: {total_count}")

            for prop in properties:
                try:
                    count+=1
                    date = datetime.date.today()
                    project = prop['projectName']
                    developer = "Гранд"
                    korpus = prop["houseName"].replace('Дом №', '')
                    type_ = 'Квартира'
                    finish_type = 'Без отделки'
                    room_count = prop["rooms_amount"]
                    area = prop["area"]["area_total"]
                    old_price = prop["custom_fields"][2]['value']
                    section = prop["sectionName"]
                    floor = prop["floor"]


                    print(
                        f"{count} | {project}, комнаты: {room_count}, площадь: {area}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                    result = [
                        date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                        '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                        '', '', type_, finish_type, room_count, area, '', old_price, '',
                        '', '', int(section), floor, ''
                    ]
                    flats.append(result)

                except Exception as e:
                    print(f"Ошибка при обработке квартиры: {e}")
                    continue

            # Проверяем, нужно ли делать следующий запрос
            offset += len(properties)
            if offset >= total_count or not properties:
                break

            time.sleep(1)

        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
