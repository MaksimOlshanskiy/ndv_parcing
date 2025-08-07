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
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6Ijk1NmFkOTQ3ODQ5YmRjYjRjZjA2MGViZWM3YzI1MmZkMDg0NmY3MjIxOTFmMmRjZDQ0OGYwNzI2MmJlNzMxNmM4N2MwMDM5MDMyZWJhOTdmIiwiaWF0IjoxNzUzNjg3MTYyLjMxNjYxNCwibmJmIjoxNzUzNjg3MTYyLjMxNjYxNywiZXhwIjoxNzUzNjkwNzYyLjMxMTgwOCwic3ViIjoiU0lURV9XSURHRVR8MTgxNCIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjQyNDIsInRpdGxlIjoi0J7QntCeINCT0YDQsNC90LQiLCJzdWJkb21haW4iOiJwYjQyNDIiLCJiaWxsaW5nT3duZXJJZCI6NDI1MCwiY291bnRyeUNvZGUiOiJSVSJ9LCJyb2xlcyI6WyJST0xFX1NJVEVfV0lER0VUIl0sInNpdGVXaWRnZXQiOnsiaWQiOjE4MTQsImRvbWFpbiI6Imh0dHBzOi8veG4tLTgwYWJkbDBhZHRieS54bi0tcDFhaSJ9fQ.zTboEhWT2LcKGTfPZmSERdPL_1I8MBx85HGfPiO9K9r9hTwurv24cycj_Jq4Tr1ffW1TjLsO8bE53OctRaa5ztQCnNGP6wghaRmrPPnEh2Ttaq9ObAB1qwki7Pk5WdfGGN_Glmsdfs7KHuEZup5dP3uqYNBkf-8fbC37d805CZggoMB1_oI5_iu-h4KTu8In7Tf6okPO78QSPMNgkbj4E6wJ4Dc1A0VTG2O-ron2Wvx7BT4ohRvBdEsEPc7Dwv0l_C3UKhkFxhzsSwLmg67l4bXgECKGdHDvF3ixXpoq-smVM6WFKY2X51iWLZDjBMblmw3mhLPfHeMDAoZ9yT7ZOQ',
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
                    project = 'Соболевка'
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
