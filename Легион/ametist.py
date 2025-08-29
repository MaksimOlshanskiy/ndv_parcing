import datetime
import time
import requests
from save_to_excel import save_flats_to_excel_near

'''
обновить authorization в headers по ссылке https://ametist-hotel.ru/#/catalog/house/111759/list?facadeId=49584&filter=property.type:hotel-room&filter=property.status:AVAILABLE
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6ImYwZGIzNzUwOGIyNDc0Mjk4NDdlNjg2NDU2ODlhNjRkZWVlYTQ3MTQzYjY5MzA1ODE3OWQ5MzZlNWIwYTgxNjEwZjk5NjA3NzU1YWE0ZTBlIiwiaWF0IjoxNzU1Nzc3NzAzLjMzMzM0LCJuYmYiOjE3NTU3Nzc3MDMuMzMzMzQyLCJleHAiOjE3NTU3ODEzMDMuMzMwMDg5LCJzdWIiOiJTSVRFX1dJREdFVHwzMDM5Iiwic2NvcGVzIjpbIlNJVEVfV0lER0VUIl0sInR5cGUiOiJzaXRlV2lkZ2V0IiwiZW50aXRsZW1lbnRzIjoiIiwiYWNjb3VudCI6eyJpZCI6MTc0OTQsInRpdGxlIjoi0KHQlyDQkNC80LXRgtC40YHRgiIsInN1YmRvbWFpbiI6InBiMTc0OTQiLCJiaWxsaW5nT3duZXJJZCI6MTc1ODQsImNvdW50cnlDb2RlIjoiUlUifSwicm9sZXMiOlsiUk9MRV9TSVRFX1dJREdFVCJdLCJzaXRlV2lkZ2V0Ijp7ImlkIjozMDM5LCJkb21haW4iOiJodHRwczovL2FtZXRpc3QtaG90ZWwucnUifX0.Spht5jUgzLRtHfGrtqYSSDDnvyhkxN5SspzeQZjN4jpC42pT73euucCsGFPnKyVmdcWEgXIphCtOnk7WtgKx1JDrxZdr2Dgv5zJG940ZY-gxWpoIvn3Fo0GPihnFQ9Ut-Yh3jKvooz7VONuA1mKpjKu8QEH7Au9Ssoom7n1-_NLa01uZtX9Y4NDfqWoSYnofJmEKJIFV5UayAa3R0eYzGjAakxow6QTxQB9gQeDkTl3rjC9VDTaaV0ZkIJWf6pmpwo5BpGJsQW6GAXxGaY6pEkKWXNLaTVsnb9Il1tzVc0jre_3-ohIoHC36I4KjpZImSCBZrHH_RDHt5SQs4nhvCA',
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
