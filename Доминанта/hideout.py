import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

base_url = "https://d-a.ru/ajax/flats/?filter[price][0]=0&filter[price][1]=0&filter[profile]=Жилая&filter[project_code]=hideout&filter[type]=Машиноместо&filter[hide_reserved][0]=Y&sort[price]=2&page={page}&cnt=30"

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
        project = "Hide out"
        developer = "Доминанта"
        korpus = i["building"]
        finish_type = i.get("finishing", "")
        room_count = i.get("rooms", "")
        area = float(i.get("sq", ""))
        price = int(i.get("price", "").replace(' ', ''))
        old_price = int(i.get("priceold", ""))
        section = i.get("section", "")
        floor = i.get("floor", "")

        if old_price == 0:
            old_price = price
            price = None

        print(
            f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        flats.append([date, project, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", developer, "",
                      "", "", "", korpus, "", "", "", "", "", "", "квартира", finish_type, room_count, area, "", old_price,
                      "", '', price, section, floor, ""])

    page += 1
    time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
