import datetime
import time
import requests
from save_to_excel import save_flats_to_excel_near

'''
обновить authorization в headers по ссылке https://ametist-hotel.ru/#/catalog/house/111759/list?facadeId=49584&filter=property.type:hotel-room&filter=property.status:AVAILABLE
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjNhMjljYTZmMDUwMmI0MWE1NTc1MmY5MTM3Nzc0ODQzY2YyNGNlMTM2NzI0ZTIzM2M2YzI5NTI0ODE0NGYzMjU4NGM4ZmFkYWIzNTQyMjc0IiwiaWF0IjoxNzUzNDM2NzE3LjI5NTMxMywibmJmIjoxNzUzNDM2NzE3LjI5NTMxNiwiZXhwIjoxNzUzNDQwMzE3LjI4OTk0OSwic3ViIjoiU0lURV9XSURHRVR8MzAzOSIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjE3NDk0LCJ0aXRsZSI6ItCh0Jcg0JDQvNC10YLQuNGB0YIiLCJzdWJkb21haW4iOiJwYjE3NDk0IiwiYmlsbGluZ093bmVySWQiOjE3NTg0LCJjb3VudHJ5Q29kZSI6IlJVIn0sInJvbGVzIjpbIlJPTEVfU0lURV9XSURHRVQiXSwic2l0ZVdpZGdldCI6eyJpZCI6MzAzOSwiZG9tYWluIjoiaHR0cHM6Ly9hbWV0aXN0LWhvdGVsLnJ1In19.qW0BfBItWs0vBbT2UWwN3T4tFws2F_6ozIkcd0C_IP2h45txsqVHwCZRjsdaeUb5QyiWnXirrzx18WhP3PzEpzdh2CGQIqSBEdLuW__uGtioJfKNjYcrkrW6myJf2JumfwxnkoBcPndqrdg64_tZgpEOhu4kchPcbFIV5WLIXcVehvNxnd0t7ItaW-KEhMv1snlcmjYbKrnAIdx7uSrPmYZ3bmrF4Iw7bv_etmWWIOKsOc7jlySfkWJs5py8PR6gAFlYsYp0wvahoqtMpzfNrbCdeHJ5QGRB3LL0Xj942WmMFM7dIZuwDlm6AY_3X9nb-zFsbp-u7PzKlbfpkBWyzw',
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
    'propertyTypeAliases[0]': 'hotel_room',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'houseId': '111759',
    'limit': '100',
    'offset': '0',
    'full': 'true',
    'returnFilteredCount': 'true',
}

base_url = 'https://pb17494.profitbase.ru/api/v4/json/property'

flats = []
count = 0
project = 'Гостиничный комплекс Аметист'
developer = "Легион"
korpus = '1'
type_ = 'Апартаменты'
finish_type = 'Без отделки'

while True:
    try:
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')
            break

        data = response.json()
        properties = data.get("data", {}).get('properties', [])
        total = data.get("data", {}).get("filteredCount", 0)

        if not properties:
            break

        for prop in properties:
            try:
                count += 1
                date = datetime.date.today()
                room_count = prop.get("rooms_amount")
                if room_count == 0:
                    room_count = 'студия'

                area = prop.get("area", {}).get("area_total")
                price_data = prop.get("price", {})
                old_price = price_data.get("prevValue")
                price = price_data.get("value")
                section = ''
                floor = prop.get("floor")

                if old_price is None:
                    old_price = price
                    price = None

                print(f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, finish_type, room_count, area, '', old_price, '',
                    '', price, section, floor, ''
                ]
                flats.append(result)

            except Exception as e:
                print(f"Ошибка при обработке квартиры: {e}")
                continue

        # обновляем offset
        params['offset'] = str(int(params['offset']) + int(params['limit']))

        if len(flats) >= total:
            break

        time.sleep(0.5)  # задержка между запросами, если нужно

    except Exception as e:
        print(f"Общая ошибка: {e}")
        break

if flats:
    save_flats_to_excel_near(flats, project, developer)
else:
    print("Нет данных для сохранения")
