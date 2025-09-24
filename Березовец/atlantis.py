import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests

"""
обновить authorization в headers по ссылке https://atlantis-capital.ru/#/catalog/projects/list?filter=project:36990&filter=property.status:AVAILABLE&genplanId=20
"""

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjM3ZGYwNmMyY2U1Yjk4ZTYyNDgzZWE2ZjljNzVhYWRmOTU3M2QzODQ1ZDJiYTU4YjdmMzkyOTc0MDFjMGVmYTMyNTk5OWEzYWY2MDI4MDQyIiwiaWF0IjoxNzU4NzA4MjE5LjYzNDQ5NywibmJmIjoxNzU4NzA4MjE5LjYzNDQ5OSwiZXhwIjoxNzU4NzExODE5LjYyODQ3OSwic3ViIjoiU0lURV9XSURHRVR8MjIwMSIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjE0NDQwLCJ0aXRsZSI6ItCc0YvRgtC40YnQuCDQlNC10LLQtdC70L7Qv9C80LXQvdGCIiwic3ViZG9tYWluIjoicGIxNDQ0MCIsImJpbGxpbmdPd25lcklkIjoxNDQ5OCwiY291bnRyeUNvZGUiOiJSVSJ9LCJyb2xlcyI6WyJST0xFX1NJVEVfV0lER0VUIl0sInNpdGVXaWRnZXQiOnsiaWQiOjIyMDEsImRvbWFpbiI6Imh0dHBzOi8vYXRsYW50aXMtY2FwaXRhbC5ydSJ9fQ.RK_gu4YhYyFKNopOqE3C39Dz0jjQqND5mP_IzqEKHHGDJFwatIo0kjxx7Sr4AAzugBinXxT7MlzwhUo3LFvv7Y_xSkzYJ_qEDrODWNL0OKue3R1HFZJiYe0KN5ROntOO3j408BB215AnyH1SV0HvXBPKy3Y_4VLlqepaIbD5EINpHJMNVjW6vQeL8oz8m6NhvX9r3qXWHd7NhvJjv_g407psrokawgipMCfgTEgXJp6v9melZBGJOb6SGPkPAMEl23JTsoJTpIXzhA6GOMVXrwSA-uT3gPC2bpNKrkE4UdfIA-Ahvw9SZyc2mVN8imjn1foqLwIdRyE9wClzRLS5EQ',
    'origin': 'https://smart-catalog.profitbase.ru',
    'priority': 'u=1, i',
    'referer': 'https://smart-catalog.profitbase.ru/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

params = {
    'propertyTypeAliases[0]': 'property',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'limit': '75',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []
count = 0

try:
    response = requests.get('https://pb14440.profitbase.ru/api/v4/json/property',
                            params=params,
                            headers=headers)

    if response.status_code == 200:
        data = response.json()
        properties = data.get("data", {}).get('properties', [])

        for prop in properties:
            try:
                count += 1
                date = datetime.date.today()
                project = 'Атлантис'
                developer = "Березовец"
                korpus = prop.get("houseName", "").replace('Дом ', '').replace(' - квартиры', '')
                type_ = 'Квартира'
                finish_type = 'Без отделки'
                room_count = prop.get("rooms_amount")

                if room_count == 0:
                    room_count = 'студия'

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

    else:
        print(f'Ошибка запроса: {response.status_code}, {response.text}')

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
