import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

base_url = "https://d-a.ru/ajax/flats/?filter[price][0]=329160000.00&filter[price][1]=329160000.00&filter[sq][0]=0&filter[sq][1]=0&filter[profile]=%D0%96%D0%B8%D0%BB%D0%B0%D1%8F&filter[project_code]=hide&filter[type]=%D0%9C%D0%B0%D1%88%D0%B8%D0%BD%D0%BE%D0%BC%D0%B5%D1%81%D1%82%D0%BE&filter[price_mlnusd][0]=0&filter[price_mlnusd][1]=0&filter[price_mlneur][0]=0&filter[price_mlneur][1]=0&filter[price_sqm][0]=0&filter[price_sqm][1]=0&filter[price_sqmusd][0]=0&filter[price_sqmusd][1]=0&filter[price_sqmeur][0]=0&filter[price_sqmeur][1]=0&filter[hide_reserved][0]=Y&filter[flat]=&sort[sq]=1&page={page}&cnt=30"

page = 1
flats = []
count = 0

while True:
    url = base_url.format(page=page)
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Ошибка: {response.status_code}')
        break

    item = response.json()
    items = item.get("data", [])

    if not items:
        print("Данные закончились, выходим из цикла.")
        break

    for i in items:
        count += 1
        date = datetime.date.today()
        project = "Hide"
        developer = "Доминанта"
        korpus = i["building"]
        finish_type = 'Предчистовая'
        room_count = int(i.get("bedroomscount", ""))
        area = float(i.get("sq", ""))
        price = int(i.get("price", "").replace(' ', ''))
        old_price = int(i.get("priceold", ""))
        section = i.get("section", "")
        floor = int(i.get("floor", ""))

        if old_price == 0:
            old_price = price
            price = None

        print(
            f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}"
        )

        flats.append([date, project, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", developer, "",
                      "", "", "", korpus, "", "", "", "", "", "", "квартиры", finish_type, room_count, area, "",
                      old_price,
                      "", '', price, section, floor, ""])

    page += 1
    if page > 10:
        print("Достигнут лимит страниц, выходим из цикла.")
        break

    time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
print(f"Файл сохранен")
