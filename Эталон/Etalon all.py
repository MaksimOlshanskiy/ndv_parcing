import datetime
import time
import requests
from bs4 import BeautifulSoup
import re

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

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
limit = 9  # Количество объявлений на одной странице (можно менять)
have_item = True  # Флаг наличия данных


def get_meta_description(flat_url):
    try:
        if not flat_url.startswith('http'):
            flat_url = f'https://etalongroup.ru{flat_url}'

        response = requests.get(flat_url, headers=headers, cookies=cookies, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tag = soup.find('meta', attrs={'name': 'description'})

            if meta_tag:
                return meta_tag.get('content', '')
            else:
                print("Мета-тег description не найден")  # Отладочное сообщение
                return ''
        else:
            print(f"Ошибка HTTP при запросе страницы: {response.status_code}")  # Отладочное сообщение
            return ''
    except Exception as e:
        print(f"Ошибка при получении мета-описания: {str(e)}")  # Отладочное сообщение
        return ''


def extract_building_and_complex(meta_description):
    """Извлекает номер корпуса и название ЖК из мета-описания."""
    korpus = ''
    project = ''

    if meta_description:
        korpus_match = re.search(r'корпус\s+(\d+)', meta_description, re.IGNORECASE)
        if korpus_match:
            korpus = korpus_match.group(1)

        jk_match = re.search(r'ЖК\s+([^–\-.\n]+)', meta_description, re.IGNORECASE)
        if jk_match:
            project = jk_match.group(1)

    return korpus, project


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
            project = i['objectTitle']
            date = datetime.date.today()
            status = ''
            developer = 'Эталон'
            okrug = ''
            district = ''
            room_count = ''
            type = i["title"].split()

            if type[0] == 'Студия':
                room_count = 'Студия'
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
            finish_type = 'Без отделки'
            area = i["area"]
            old_price = i["price"]
            discount = ''
            price = i["priceTotal"]
            section = ''
            floor = i["floor"]
            flat_number = ''

            flat_url = i.get("link", "")
            meta_description = get_meta_description(flat_url) if flat_url else ""

            korpus = extract_building_and_complex(meta_description)[0]

            if old_price == price:
                price = None

            print(
                f"{count}, {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', status, '', '', developer, okrug,
                      district, '', '', korpus, '', '', '', '', '', '', type, finish_type, room_count, area, '',
                      old_price, discount, '', price, section, floor, flat_number]
            flats.append(result)

            count += 1
            time.sleep(0.05)

        # Проверяем, есть ли еще данные
        have_item = pagination.get("haveItem", False)
        offset = pagination.get("offset", offset + limit)  # Обновляем offset

        time.sleep(0.05)  # Задержка между запросами
    except Exception as e:
        print(f"Ошибка обработки JSON: {e}")
        break

save_flats_to_excel(flats, 'all', developer)
