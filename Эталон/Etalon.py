import datetime
import time
import pandas as pd
import os
import requests


cookies = {
    'PHPSESSID': 'kLhpYpDU4pBf5qEWlalRohUJEv3FHoQh',
    'scbsid_old': '2750244825',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

url = 'https://etalongroup.ru/bitrix/services/main/ajax.php?action=etalongroup:filter.FlatFilter.getFlatList'

flats = []
count = 1

# Параметры пагинации
offset = 0
limit = 8  # Количество объявлений на одной странице (можно менять)
have_item = True  # Флаг наличия данных

while have_item:
    print(f"Загружаю объявления с offset={offset}...")

    params = {
        'filter[onlyInSale]': 'true',
        'getAuctionSlider': 'true',
        'limit': limit,  # Количество объявлений на страницу
        'offset': offset,  # Смещение
    }

    response = requests.post(url, headers=headers, cookies=cookies, params=params)

    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        break

    try:
        data = response.json()
        items = data.get("data", [{}])[0].get("itemList", [])
        pagination = data.get("data", [{}])[0].get("pagination", {})

        if not items:
            print("Данные закончились, выхожу из цикла.")
            break

        for i in items:
            date = datetime.date.today()
            project = ''
            status = ''
            developer = 'Эталон'
            okrug = ''
            district = ''
            korpus = ''
            room_count = ''
            type = i["title"].split()
            if type[0] == 'Студия':
                room_count = 0
                type = 'Студия'
            else:
                if type[0] == 'Однокомнатная':
                    room_count = 1
                elif type[0] == 'Двухкомнатная':
                    room_count = 2
                elif type[0] == 'Трехкомнатная':
                    room_count = 3
                elif type[0] == 'Четырехкомнатная':
                    room_count = 4
                elif type[0] == 'Пятикомнатная':
                    room_count = 5
                type = 'Квартира'

            finish_type = ''
            area = i["area"]
            old_price = i["price"]
            discount = ''
            price = i["priceTotal"]
            section = ''
            floor = i["floor"]
            flat_number = ''

            print(
                f"{count}, {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', status, '', '', developer, okrug,
                      district, '', '', korpus, '', '', '', '', '', '', type, finish_type, room_count, area, '',
                      old_price, discount, '', price, section, floor, flat_number]
            flats.append(result)

            count += 1

        # Проверяем, есть ли еще данные
        have_item = pagination.get("haveItem", False)
        offset = pagination.get("offset", offset + limit)  # Обновляем offset

        time.sleep(0.1)  # Задержка между запросами
    except Exception as e:
        print(f"Ошибка обработки JSON: {e}")
        break


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
base_path = r"C:\Users\m.lugovskiy\PycharmProjects\Parcer\Date_files"
folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{current_date}_all.xlsx"
file_path = os.path.join(folder_path, filename)
df.to_excel(file_path, index=False)

print(f"Данные сохранены в {file_path}")
