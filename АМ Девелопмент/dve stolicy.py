import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests

'''
обновить authorization в headers по ссылке https://xn----ctbffqruxj7b3c.xn--p1ai/flats/visual/#/catalog/projects/plans?filter=project:36880&filter=property.status:AVAILABLE&genplanId=13
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjE4OGM5N2U4ZGQzNTQzYzNmMzE4YmNiZWYxYmU0N2MxNjY1NTYwZTlmMDQ1NjE1YjAxNGFmOWE0MWJiYjNiNzk3YWUxZTY0MjU4MzQzZWQ4IiwiaWF0IjoxNzUzNDMwODU2LjYyMzc2MiwibmJmIjoxNzUzNDMwODU2LjYyMzc2NCwiZXhwIjoxNzUzNDM0NDU2LjYyMDU5Mywic3ViIjoiU0lURV9XSURHRVR8Mjc3MSIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjUyOTAsInRpdGxlIjoi0JDQnCDQlNC10LLQtdC70L7Qv9C80LXQvdGCIiwic3ViZG9tYWluIjoicGI1MjkwIiwiYmlsbGluZ093bmVySWQiOjUyOTgsImNvdW50cnlDb2RlIjoiUlUifSwicm9sZXMiOlsiUk9MRV9TSVRFX1dJREdFVCJdLCJzaXRlV2lkZ2V0Ijp7ImlkIjoyNzcxLCJkb21haW4iOiJodHRwczovL3huLS0tLWN0YmZmcXJ1eGo3YjNjLnhuLS1wMWFpIn19.CHKQD3zqQfrsFWVV4vny4l5aA0GIva71UvQ2mQrTr0keFRMkHRy0Zc4AYRNofGKxViF9zCm5Mc1eYQh-ciMI0KVMdiUA6OaFss43O0xu81rtSketXEUwf6HFxb9Oac7XRUi_arhfA7jCk0xoIZ1JmW_x26NfOqoGIMuiCDxxNcdrStdiEIfMyAJKR3uZC0T7v-mO6N0lbXwc2skKeJWUYh1kfDcJoL5GSw6NX2huVQw0MWaqGUPEKLnX_qIStmKMAPiVTo2uvnoeh7WkYLU7DNhUWPaRITBLj_GW7XxATKffwmd0EGm069DqarasHzbaZR8t_K3lhEKm9ZWxeB_-_w',
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
    'limit': '33',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []
count = 0

try:
    response = requests.get('https://pb5290.profitbase.ru/api/v4/json/property',
                            params=params,
                            headers=headers)

    if response.status_code == 200:
        data = response.json()
        properties = data.get("data", {}).get('properties', [])

        for prop in properties:
            try:
                count += 1
                date = datetime.date.today()
                project = 'Две столицы'
                developer = "АМ Девелопмент"
                korpus = prop.get("houseName", "").replace('Корпус ', '')
                type_ = 'Квартира'
                finish_type = prop['custom_fields'][18]['value']

                if finish_type in ['Нет', 'нет']:
                    finish_type = 'Без отделки'
                elif finish_type in ["Да", 'да']:
                    finish_type = "С отделкой"
                elif finish_type == "Черновая отделка":
                    finish_type = "Предчистовая"

                room_count = prop.get("rooms_amount")
                area = prop.get("area", {}).get("area_total")
                price_data = prop.get("price", {})
                old_price = price_data.get("value")
                section = prop.get("sectionNumber")
                floor = prop.get("floor")

                print(
                    f"{count} | {project}, комнаты: {room_count}, площадь: {area}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', float(str(korpus)), '', '', '', '',
                    '', '', type_, finish_type, room_count, area, '', old_price, '',
                    '', '', section, floor, ''
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
