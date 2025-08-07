import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://xn--b1agmbafra0kya.xn--p1ai',
    'Pragma': 'no-cache',
    'Referer': 'https://xn--b1agmbafra0kya.xn--p1ai/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

base_url = 'https://3points.tsnnedv.ru/api/profitbase/flats?full=true&projectId=8247&status[]=AVAILABLE&houseId[]=12838&houseId[]=12863&price[min]=1&price[max]=15000000&area[min]=1&area[max]=150'

flats = []
count = 1
offset = 0
limit = 50  # Можно попробовать увеличить, если сервер позволяет


response = requests.get(base_url, headers=headers)

if response.status_code == 200:
    item = response.json()

    items = item.get("data", [])

    for i in items:
        date = datetime.date.today()
        project = i['projectName']
        developer = "Гранд"
        room_count = i['rooms_amount']
        type = "Квартира"
        area = i["area"]['area_total']
        price_per_metr_new = i['price']['pricePerMeter']
        price = i["price"]['value']
        section = i['sectionNumber']
        floor = i["floor"]

        print(
            f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}")
        result = [date, project, '', '', '', '', '', '',
                  '',
                  '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', '18',
                  '', '', '', '',
                  '', '', type, 'С отделкой', room_count, area, '', price, '',
                  '', '', section, floor, '']
        flats.append(result)

        count += 1

time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
