import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests

'''
обновить authorization в headers по ссылке https://zamitino.ru/#/catalog/projects/list?filter=property.type:property&filter=property.status:AVAILABLE
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6ImFiMzU0OTNkOWFiYjEzYjc4NGEwYWIzN2ViYjViMDVkZjQyMDY3MWJkOGY5YjA3Nzc0MTRjOTRiZTcxY2YwY2I5ZjdkNjJlNTZlMzk2MTNlIiwiaWF0IjoxNzUzNDM1ODg5Ljk5NDQ3OCwibmJmIjoxNzUzNDM1ODg5Ljk5NDQ4MSwiZXhwIjoxNzUzNDM5NDg5Ljk4OTkzOCwic3ViIjoiU0lURV9XSURHRVR8MjI3MCIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjE0NzM1LCJ0aXRsZSI6ItCc0LXRgtGA0L7RhNC-0L3QtCIsInN1YmRvbWFpbiI6InBiMTQ3MzUiLCJiaWxsaW5nT3duZXJJZCI6MTQ3OTMsImNvdW50cnlDb2RlIjoiUlUifSwicm9sZXMiOlsiUk9MRV9TSVRFX1dJREdFVCJdLCJzaXRlV2lkZ2V0Ijp7ImlkIjoyMjcwLCJkb21haW4iOiJodHRwczovL3phbWl0aW5vLnJ1In19.OtUIvi0jU0QKs-w81IZ8aGc-meKc-cXj-VETP7gylO--sYnOJetWeaOTL7Fff8RUfJUImO5evpRdke88fH_zOw3H9N3fu3Qe5mlt4MhBkqDJVPViGVyUeNWOlLFHixSxrxY3Rml-kQPVR4SG19Zc6DyIjtsYd3-ajir8A6dfxChJe4Qo4ld0wfXiaHxVBZ_H5RydOlWIRCwT2uQHt6i0i2wzL5k3ZLhecUfPO-zhPnQIXQ9QSzzID2O1YZERvdONp0i6Nh9BsmudbuxP6_3xRMAv6gTEm1yAYRV1vOzRqH5dq2uVseZfGpJ_r4BQT7JkyXoCOIMNu5owPsnaKsDMmw',
    'origin': 'https://smart-catalog.profitbase.ru',
    'priority': 'u=1, i',
    'referer': 'https://smart-catalog.profitbase.ru/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

params = {
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'limit': '150',
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

        response = requests.get('https://pb14735.profitbase.ru/api/v4/json/property',
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
                    if '-кладовки' in prop.get("houseName", ""):
                        continue
                    count += 1
                    date = datetime.date.today()
                    project = 'Новое Замитино'
                    developer = "Замитино"
                    korpus = prop.get("houseName", "").replace('Корпус ', '').replace('Луговая ','')
                    type_ = 'Квартира'
                    finish_type = 'Без отделки'
                    room_count = prop.get("rooms_amount")
                    area = prop.get("area", {}).get("area_total")
                    price_data = prop.get("price", {})
                    old_price = price_data.get("value")
                    section = prop.get("sectionName")
                    floor = prop.get("floor")

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
            break

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
