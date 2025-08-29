import datetime
import time
import traceback
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

'''
обновить authorization в headers по ссылке https://xn----otbabat2bef9dta.xn--p1ai/#/catalog/projects/list?filter=project:39970&filter=property.type:property&filter=property.status:AVAILABLE&genplanId=682
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjI0MDQxNjBkOGRiMTBlZjVhNGE3ZTE2OWM3MGE2OWVmZDljODcxMTRlODg0ZDRjOTNhNTZjMzdmMDM5N2M0OTY1MjIxOWUzOWVjN2EzNTRjIiwiaWF0IjoxNzU1Nzc3ODgwLjk3MTA1NCwibmJmIjoxNzU1Nzc3ODgwLjk3MTA1NywiZXhwIjoxNzU1NzgxNDgwLjk2NjMxMywic3ViIjoiU0lURV9XSURHRVR8MjQzNiIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjE0NDQwLCJ0aXRsZSI6ItCc0YvRgtC40YnQuCDQlNC10LLQtdC70L7Qv9C80LXQvdGCIiwic3ViZG9tYWluIjoicGIxNDQ0MCIsImJpbGxpbmdPd25lcklkIjoxNDQ5OCwiY291bnRyeUNvZGUiOiJSVSJ9LCJyb2xlcyI6WyJST0xFX1NJVEVfV0lER0VUIl0sInNpdGVXaWRnZXQiOnsiaWQiOjI0MzYsImRvbWFpbiI6Imh0dHA6Ly94bi0tLS1vdGJhYmF0MmJlZjlkdGEueG4tLXAxYWkifX0.La3oJ79rkZKO2WF09HpUfpgbDZLFSfx0w9Lr1XxahiUnxKw1em15cu-NpAe6KtSQ92mTzc8BddW6rThZOjgkKEqy_XZKhRC4xwY-Hz6Lb37xlF1pqr1_yUlRXrolhuGrhNLqEQ2LtXT49soBMidRwAo_V3u-ltQ36S0C_k2Ce6PRZ8jwNEspilTGvM79J6N9-Vo_orEMnzbFPj6t7bTf8b4TpennM9NmIKYi4Yypey0-VPYVY9kK1ClD6Tbjhz0IJJ8FT2p2uAGh-vabiv1Ig_mrZMVxBNG8ViW8Pk5HvIQFxxyCNJJV9iORlnVvAiX89_qh-mH1uhbOF3LQ3yBdrQ',
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
    'limit': 1000,
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []
offset = 1
page_size = 75
count = 0

while True:
    params.update({'offset': offset, 'limit': page_size})
    response = requests.get('https://pb14440.profitbase.ru/api/v4/json/property',
                            params=params,
                            headers=headers)

    if response.status_code == 200:
        data = response.json()
        properties = data.get("data", {}).get('properties', [])

        if not properties:
            print(f"Данных больше нет.")
            break

        for prop in properties:
            try:
                count += 1
                date = datetime.date.today()
                project = 'Мытищи Сити'
                developer = "Ломоносов Девелопмент"
                korpus = prop["houseName"]
                type_ = 'Квартира'
                finish_type = 'Без отделки'
                room_count = prop["rooms_amount"]
                area = prop["area"]["area_total"]
                old_price = prop['price']["value"]
                price_per_metr_new = prop['price']["pricePerMeter"]
                price = prop['price']["value"]
                section = prop["sectionName"]
                floor = prop["floor"]

                if old_price == price:
                    price = None

                print(
                    f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, finish_type, room_count, area, '', old_price, '',
                    '', price, int(section), floor, ''
                ]
                flats.append(result)

            except Exception as e:
                print(f"Ошибка при обработке квартиры: {e}")
                traceback.print_exc()
                continue

    else:
        print(f'Ошибка запроса: {response.status_code}, {response.text}')

    offset += page_size

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
