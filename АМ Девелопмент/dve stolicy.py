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
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6ImQ1OGU5YjFkNzc0YTVmN2JlMmJhZGVmZDcyNzE4NDhkMTU2OTI0ZGJmNzc1MjY2YjkxZmY2NGJkY2MwNjljODIwNDIzNzAwYmNhOGExMTJkIiwiaWF0IjoxNzU1Njk3MTgzLjk2MDIwNCwibmJmIjoxNzU1Njk3MTgzLjk2MDIwNywiZXhwIjoxNzU1NzAwNzgzLjk1NjM4LCJzdWIiOiJTSVRFX1dJREdFVHwyNzcxIiwic2NvcGVzIjpbIlNJVEVfV0lER0VUIl0sInR5cGUiOiJzaXRlV2lkZ2V0IiwiZW50aXRsZW1lbnRzIjoiIiwiYWNjb3VudCI6eyJpZCI6NTI5MCwidGl0bGUiOiLQkNCcINCU0LXQstC10LvQvtC_0LzQtdC90YIiLCJzdWJkb21haW4iOiJwYjUyOTAiLCJiaWxsaW5nT3duZXJJZCI6NTI5OCwiY291bnRyeUNvZGUiOiJSVSJ9LCJyb2xlcyI6WyJST0xFX1NJVEVfV0lER0VUIl0sInNpdGVXaWRnZXQiOnsiaWQiOjI3NzEsImRvbWFpbiI6Imh0dHBzOi8veG4tLS0tY3RiZmZxcnV4ajdiM2MueG4tLXAxYWkifX0.zbqGPlFgYL2PrUQLucSQGmCzlhgi6HcWfQ2Ed29W18VsTdUBWsrsw4RAFSDzWyi-QZBvRs7y-fluI2kQUFPDoQyCxgUhIqu8mPPaOg01OadgYTn9vVSGWt_6w_qKpM-X0vYNFgHm5ZuzrKmvg9yaVM4gMQhOYQEuXBoH2rLlHOfKhEeHnhltTTvUk3i42b8nBsLG9y5IkYgLiYiOKngg6qs_AQpJSMEl4bBMsFiKutwjC0IZ8o3TpC9U0qiAF4_O1BNiUGruJBXZ2CBEBNUwCKO7nqD-ymkD9TLcIaxjT8OsCpG5ukEjhmqTRfvl3P5WRIrTh1CKa1GDkRljcNywkw',
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
    'projectIds[0]': '36880',
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
