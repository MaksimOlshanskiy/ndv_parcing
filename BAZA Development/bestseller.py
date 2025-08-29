import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

'''
Надо обновить в headers поле authorization по ссылке
https://baza.bz/projects/bestseller#/catalog/projects/list?filter=project:50007&filter=property.type:property&filter=property.status:AVAILABLE&genplanId=2176
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjY3YmViYzkwODAzZjk0MzQ4ZGZhMzY4YmI2YjE2N2FiYTM1MTUxYzkzNmM1ZDZlMjBhZjljOTY4ZWU3ODE5YWYxODg2NjYyYzg1MmMzYTFiIiwiaWF0IjoxNzU2MTA2NzQ0Ljc3NDEyNiwibmJmIjoxNzU2MTA2NzQ0Ljc3NDEyOCwiZXhwIjoxNzU2MTEwMzQ0Ljc2OTgxNSwic3ViIjoiU0lURV9XSURHRVR8MjM0MSIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjE1MzUzLCJ0aXRsZSI6IkJBWkEgRGV2ZWxvcG1lbnQiLCJzdWJkb21haW4iOiJwYjE1MzUzIiwiYmlsbGluZ093bmVySWQiOjE1NDExLCJjb3VudHJ5Q29kZSI6IlJVIn0sInJvbGVzIjpbIlJPTEVfU0lURV9XSURHRVQiXSwic2l0ZVdpZGdldCI6eyJpZCI6MjM0MSwiZG9tYWluIjoiaHR0cHM6Ly9iYXphLmJ6In19.rS0pO_vMJy3_XxuB8hPb-Lf9szT2C9kHQfCoOOuGSfXcFk0L8lXHfb_OGMA3dpsgPgD7Bl4KZAUr7VW28masa3-NWplUlMahSxg6cwFS05qgK8J66Z-tcUV7f3ZGN499LYY2BCLbQNF6u1uRaS16-o-870KNDAcXCu_X2t5dC6X8RseDvpD4nB0C1Mq8X7X1kKPKr2OfxBOLthV24iAMgpmegt6VVEYBJ9pRJwHc1zqPp3fZ6q_xho7d4HDThuGXfhjWBuUld7lff5py13qk8LElRTTNoAzcZgyTD615GLAfbCi9hJnvOLto2l7gpyEiQMunCfF0LXabYJILeHsmTw',
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
    'houseId': '125459',
    'limit': '100',
    'offset': '0',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []

try:
    response = requests.get('https://pb15353.profitbase.ru/api/v4/json/property',
                            params=params,
                            headers=headers)

    if response.status_code == 200:
        data = response.json()
        properties = data.get("data", {}).get('properties', [])

        for prop in properties:
            try:
                date = datetime.date.today()
                project = 'Бестселлер'
                developer = "BAZA Development"
                korpus = prop.get("houseName", "").replace('Корпус №', '')
                type_ = 'Квартира'
                room_count = prop.get("rooms_amount")
                area = prop.get("area", {}).get("area_total")
                price_data = prop.get("price", {})
                old_price = price_data.get("value")
                price_per_metr = round(float(price_data.get("pricePerMeter")))
                price = price_data.get("value")
                section = prop.get("section").replace(',', '.')
                floor = prop.get("floor")

                print(
                    f"{project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, 'Без отделки', room_count, area, price_per_metr, old_price, '',
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
    save_flats_to_excel(flats, 'Бестселлер', 'BAZA Development')
else:
    print("Нет данных для сохранения")
