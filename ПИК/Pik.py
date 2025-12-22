import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain',
    'Origin': 'https://www.pik.ru',
    'Referer': 'https://www.pik.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# "type" 4 это коммерческая недвижимость
params = {
    "type": "1,2",
    "location": "2,3",
    "flatPage": 1,
    "flatLimit": 8,
    "onlyFlats": 1,
    "currentBenefit": "polnaya-oplata",      #   проверить эту строчку, была проблема в прошлый раз

}

zk_list = [1876, 1709,1555,481,378,294,1372,2214,1129,47,411,21,1240,164,1519,156,1421,2319,530,518,296,1196,1460,161,1688,1411,1108,1874,1165,1556,149,2106,1401,1580,1124,477,118,1200,464,1167,1934,65,1272,1220,320]
flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

for zk in zk_list:


    params["flatPage"] = 1

    print("Парсим ЖК id:", zk)

    while True:


        url = f'https://flat.pik-service.ru/api/v1/filter/flat-by-block/{str(zk)}'

        response = requests.get(
            url=url,
            headers=headers,
            params=params
        )

        print('--------------------------------------------------------------')
        items = response.json()["data"]["items"]

        for i in items:

            date = datetime.date.today()
            project = i["blockName"]
            english = ''
            promzona = ''
            mestopolozhenie = ''
            subway = ''
            distance_to_subway = ''
            time_to_subway = ''
            mck = ''
            distance_to_mck = ''
            time_to_mck = ''
            bkl = ''
            distance_to_bkl = ''
            time_to_bkl = ''
            status = ''
            start = ''
            comment = ''
            developer = "ПИК"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = str(i["bulkName"]).replace('Корпус ', '')
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            if i['typeId'] == 2:
                type = 'Апартаменты'
            else:
                type = 'Квартиры'
            if i["finishType"] == 0:
                finish_type = "Без отделки"
            elif i["finishType"] == 1:
                finish_type = "С отделкой"
            elif i["finishType"] == 2:
                finish_type = "Предчистовая"
            elif i["finishType"] == 3:
                finish_type = "С отделкой и доп опциями"
            if int(i["rooms"]) == 0 or int(i["rooms"]) == -1:
                room_count = 0
            else:
                room_count = int(i["rooms"])
            area = float(i["area"])
            price_per_metr = ''
            if i["oldPrice"] is None:
                old_price = i["price"]
                price = ''
            else:
                old_price = i["oldPrice"]
                price = i["price"]
            discount = ''
            price_per_metr_new = ''

            section = i["sectionNumber"]
            floor = i["floor"]
            flat_number = ''

            print(
                f"{project}, дата: {date}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type} ")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck, distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)

        if not items:
            print("Всё скачано. Переходим к загрузке в файл")
            break

        params["flatPage"] += 1
        sleep_time = random.uniform(1, 4)
        time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)



