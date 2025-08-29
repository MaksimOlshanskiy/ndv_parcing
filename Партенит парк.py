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
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6Ijk1MTYxNTVkNWIyODRiMGQ2NWJkZDk1OTMzY2RiZTE5MGEzYTc2MGFjNzNmNGVhNTcyNjc2NTQzNWZlNGJlMTRjNTJjOWU0MGM5ZmUxMTFhIiwiaWF0IjoxNzU1NjcyMDMzLjMxOTE5OCwibmJmIjoxNzU1NjcyMDMzLjMxOTIsImV4cCI6MTc1NTY3NTYzMy4zMDkxNDQsInN1YiI6IlNJVEVfV0lER0VUfDIzNDkiLCJzY29wZXMiOlsiU0lURV9XSURHRVQiXSwidHlwZSI6InNpdGVXaWRnZXQiLCJlbnRpdGxlbWVudHMiOiIiLCJhY2NvdW50Ijp7ImlkIjoxNTI2NSwidGl0bGUiOiLQodC10LLQsNGB0YLQvtC_0L7Qu9GMINCh0YLRgNC-0LkiLCJzdWJkb21haW4iOiJwYjE1MjY1IiwiYmlsbGluZ093bmVySWQiOjE1MzIzLCJjb3VudHJ5Q29kZSI6IlJVIn0sInJvbGVzIjpbIlJPTEVfU0lURV9XSURHRVQiXSwic2l0ZVdpZGdldCI6eyJpZCI6MjM0OSwiZG9tYWluIjoiaHR0cHM6Ly94bi0tODBhZGlzanJhYmdtZGRlamYybi54bi0tcDFhaSJ9fQ.hk5klc8m3nuG3Bk5I5BayBrKYpP0jWxIwN_7cBOjGWj8zupCQ9bBw1NBOp0AQXTha2lIyW6NytnOjPnrLwWUa99hKs2BTDFAut80w68fqp2kL4nfb6K1KohysuhX4jICB5yiHz1YqtGxWt7r8XaDbQU4aLb8E0Pse1taLw1DumvoB3A2XVQcubddmWEqYDiPQwqma5oVOK4A8elLz715Lmsassp8YV9lxdhnvFSwJPJYzC8LMFfF5ql16cqdPN6B-76VuzYFzX99z2eKOcBwuhbgmXya1SYm-4bMSKbwi_GB0Zmr2FOkftR9UWeAW7ZEAcgLenB7C-8wea7Q5fa8ng',
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
    'houseId': '103944',
    'limit': '10',
    'offset': '0',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []
count = 0
buildings_ids = ['103944', '103945', '119493', '119494']


for buildings_id in buildings_ids:

    params['houseId'] = buildings_id
    params['offset'] = '0'

    while True:

        try:
            response = requests.get('https://pb15265.profitbase.ru/api/v4/json/property', params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                properties = data.get("data", {}).get('properties', [])

                for prop in properties:
                    try:
                        count += 1
                        date = datetime.date.today()
                        project = 'Партенит Парк'
                        developer = "Севастопольстрой"
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
