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
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjhmZTRkY2U0YzM3MzNjYjI1ZjlhOWMxNjQxYzM2ZDM2YTY1MmU0YmJjZTVjYTUyYWVmMjQ2MDI5MDg0OTVmNzFkMzJjZTU4YWZiNWRhOWFkIiwiaWF0IjoxNzY0NTc4NTgxLjkwMjkzNiwibmJmIjoxNzY0NTc4NTgxLjkwMjkzOCwiZXhwIjoxNzY0NTgyMTgxLjg5MzE4OSwic3ViIjoiU0lURV9XSURHRVR8Mjc3MSIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjUyOTAsInRpdGxlIjoi0JDQnCDQlNC10LLQtdC70L7Qv9C80LXQvdGCIiwic3ViZG9tYWluIjoicGI1MjkwIiwiYmlsbGluZ093bmVySWQiOjUyOTgsImNvdW50cnlDb2RlIjoiUlUifSwicm9sZXMiOlsiUk9MRV9TSVRFX1dJREdFVCJdLCJzaXRlV2lkZ2V0Ijp7ImlkIjoyNzcxLCJkb21haW4iOiJodHRwczovL3huLS0tLWN0YmZmcXJ1eGo3YjNjLnhuLS1wMWFpIn19.adr-ObM8Z5witwJtEALsrj-7vg3hLNa7WV8U7qHhqi5kXTGTyz_4NH3EWMeMK_kYW3OCmW_gtrV7y9LlhdhF8dFngSjT8Ll9bEWB6YVA28W9fxIJyoNkZnYhRLXjxGXYh3dCGIqu6BdGhuWW3zaenjeoAtLIf0foLEUZUTU5ZJUbm32hsL7bNO2aOOBLxU1CuhyVCsrlOAq4Ifw4uhNuozuNd-GBdLcEynjy8RskABpa58v6IZl4Mgff6zhzR9ko_4yoAS7oS9U2bWuPd2StuXk7CTCCxbHCTSj4C-U06nUvyhh4Cg4P4nGa5lIXTC7kO7ky5jpfPeiaqC7dUKp1hw',
    'origin': 'https://smart-catalog.profitbase.ru',
    'priority': 'u=1, i',
    'referer': 'https://smart-catalog.profitbase.ru/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

params = {
    'projectIds[0]': '36880',
    'propertyTypeAliases[0]': 'property',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'limit': '10',
    'offset': '0',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []

while True:
    try:
        response = requests.get('https://pb5290.profitbase.ru/api/v4/json/property',
                                params=params,
                                headers=headers)

        if response.status_code == 200:
            data = response.json()
            properties = data.get("data", {}).get('properties', [])

            for prop in properties:
                try:

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
                        f"{project}, комнаты: {room_count}, площадь: {area}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

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
            if not properties:
                break
            params['offset'] = str(int(params['offset']) + 10)
        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')

    except Exception as e:
        print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
