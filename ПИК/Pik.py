import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

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


params = {
    "type": "1,2",
    "location": "2,3",
    "flatPage": 1,
    "flatLimit": 8,
    "onlyFlats": 1,
    "currentBenefit": "polnaya-oplata-1",      #   проверить эту строчку, была проблема в прошлый раз

}

zk_list = [
  21,
  47,
  55,
  65,
  90,
  118,
  130,
  149,
  156,
  159,
  161,
  162,
  164,
  172,
  219,
  253,
  294,
  296,
  320,
  378,
  404,
  411,
  464,
  477,
  481,
  518,
  519,
  530,
  544,
  1108,
  1124,
  1129,
  1134,
  1167,
  1196,
  1200,
  1220,
  1240,
  1272,
  1369,
  1372,
  1401,
  1411,
  1421,
  1424,
  1460,
  1519,
  1541,
  1555,
  1556,
  1580,
  1688,
  1692,
  1709,
  1874,
  1934,
  1377
]

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

for zk in zk_list:

    flats = []
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
            korpus = i["bulkName"]
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = ''

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

            area = i["area"]
            price_per_metr = ''
            if i["oldPrice"] is None:
                old_price = 0
            else:
                old_price = i["oldPrice"]
            discount = ''
            price_per_metr_new = ''
            price = i["price"]
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

    if len(flats) >= 10:      #  сохраняем ЖК, где 10 и более квартир в наличии

        df = pd.DataFrame(flats, columns=['Дата обновления',
                                          'Название проекта',
                                          'на англ',
                                          'промзона',
                                          'Местоположение',
                                          'Метро',
                                          'Расстояние до метро, км',
                                          'Время до метро, мин',
                                          'МЦК/МЦД/БКЛ',
                                          'Расстояние до МЦК/МЦД, км',
                                          'Время до МЦК/МЦД, мин',
                                          'БКЛ',
                                          'Расстояние до БКЛ, км',
                                          'Время до БКЛ, мин',
                                          'статус',
                                          'старт',
                                          'Комментарий',
                                          'Девелопер',
                                          'Округ',
                                          'Район',
                                          'Адрес',
                                          'Эскроу',
                                          'Корпус',
                                          'Конструктив',
                                          'Класс',
                                          'Срок сдачи',
                                          'Старый срок сдачи',
                                          'Стадия строительной готовности',
                                          'Договор',
                                          'Тип помещения',
                                          'Отделка',
                                          'Кол-во комнат',
                                          'Площадь, кв.м',
                                          'Цена кв.м, руб.',
                                          'Цена лота, руб.',
                                          'Скидка,%',
                                          'Цена кв.м со ск, руб.',
                                          'Цена лота со ск, руб.',
                                          'секция',
                                          'этаж',
                                          'номер'])

        current_date = datetime.date.today()

        # Базовый путь для сохранения
        base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ПИК"

        folder_path = os.path.join(base_path, str(current_date))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = f"{developer}_{project}_{current_date}.xlsx"

        # Полный путь к файлу
        file_path = os.path.join(folder_path, filename)

        # Сохранение файла в папку
        df.to_excel(file_path, index=False)

    else:
        print(f"В ЖК всего {len(flats)} квартир, поэтому не сохраняем в файл")


