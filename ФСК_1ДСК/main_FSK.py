import datetime
import time
import pandas as pd
import os
import requests
from info_FSK import info
from save_to_excel import save_flats_to_excel_old_new_all

flats = []
count = 0

for key, data in info.items():
    headers = data['headers']
    params = data['params']
    cookies=data.get('cookies', {})
    response = requests.get('https://fsk.ru/api/v3/flats/all', params=params, cookies=cookies, headers=headers)



    def extract_digits_or_original(s):
        digits = ''.join([char for char in s if char.isdigit()])
        return int(digits) if digits else s


    items = response.json()

    for i in items:
        count += 1
        url = i["externalId"]
        date = datetime.date.today()
        project = i["project"]["title"]
        developer = "ФСК"
        korpus = i["corpus"]["number"]
        type = i["crmObjectType"]
        finish_type = ''
        for j in i['labels']:
           if 'отделк' in j['title'].lower():
               finish_type = j['title']

        if finish_type == 'Отделка White Box + с/у под ключ' or finish_type == 'Отделка White Box':
            finish_type = 'Предчистовая'
        elif finish_type == 'Чистовая отделка':
            finish_type = 'С отделкой'
        else:
            finish_type='Без отделки'

        if type == 'Студия':
            room_count = 'Студия'
            type = 'Квартира'
        else:
            room_count = int(i["crmRoomsQty"])

        area = i["areaTotal"]
        old_price = i["priceWoDiscount"]
        price = i["price"]
        section = i["section"]["number"]
        try:
            floor = int(i["floor"]["number"])
        except:
            floor = int(i["floor"]["number"].split('.')[0])
        flat_number = ''

        if old_price == price:
            price = None


        print(
            f"{count}, {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [
            date, project, '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', developer,
            '', '', '', '', korpus, '', '', '', '', '',
            '', type, finish_type, room_count, area, '', old_price, '', '',
            price, section, floor, ''
        ]
        flats.append(result)

    time.sleep(0.05)

save_flats_to_excel_old_new_all(flats, developer)
