import datetime
import time
import requests

from functions import save_flats_to_excel
from info import info
from save_to_excel import save_flats_to_excel_old_new

flats = []
count = 1
project = "Ново-Никольское"
developer = "Агрострой"

for key, data in info.items():
    headers = data['headers']
    base_url = data['base_url']
    cookies = data.get('cookies', {})

    try:
        response = requests.get(base_url, cookies=cookies, headers=headers)
        response.raise_for_status()
        items = response.json()
    except Exception as e:
        print(f"[{key}] Ошибка при получении данных: {e}")
        continue

    for item in items:
        if base_url == 'https://n-nk.ru/import/filter-data-highrise.json':
            date = datetime.date.today()
            room_count = item.get("FlatRoomsCount", "")
            area = item.get("TotalArea", "")

            # Обработка цен
            try:
                old_price_raw = item.get("OldPriceFormat", "").replace(' ', '')
            except:
                old_price_raw = item.get("OldPriceFormat", "")

            price_raw = item.get("PriceFormat", "").replace(' ', '')
            price = int(price_raw) if price_raw.isdigit() else ''
            old_price = int(old_price_raw) if old_price_raw.isdigit() else int(price_raw)

            floor = item.get("FloorNumber", "")
            section = item.get("SectionNumber", "")
            number = item.get("FlatNum", "")
            house_number = item.get("HouseCount", "")

            if (number == 94 and house_number == 12) or (number == 91 and house_number == 12) or (
                    number == 90 and house_number == 12):
                finish_type = "С отделкой"
            else:
                finish_type = "Без отделки"
        else:
            date = datetime.date.today()
            room_count = item.get("FlatRoomsCount", "")
            area = item.get("TotalArea", "")
            old_price = old_price
            price = int(item.get("PriceFormat", "").replace(' ', ''))
            floor = item.get("FloorNumber", "")
            section = item.get("SectionNumber", "")
            finish_type = "Без отделки"

        if price == old_price:
            price = None

        print(f"{count}, {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}")

        row = [
            date, project, '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', developer, '', '', '', '', house_number, '', '', '', '',
            '', '', 'Квартира', finish_type, room_count, area, '', old_price, '', '', price,
            section, floor, ''
        ]

        flats.append(row)
        count += 1

    time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
print(f"Успешно сохранено {len(flats)} записей")
