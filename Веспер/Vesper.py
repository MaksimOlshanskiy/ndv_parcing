import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

cookies = {
    '_ym_uid': '1742205644667005339',
    '_ym_d': '1742205644',
    '_ym_isad': '1',
    '_gid': 'GA1.2.1615702455.1742205645',
    '_ga_CH4N4HXTEW': 'GS1.1.1742205644.1.0.1742205644.0.0.0',
    '_ym_visorc': 'w',
    '_cmg_csstdN3ds': '1742205645',
    '_comagic_iddN3ds': '9188604422.13120320567.1742205638',
    '_ga': 'GA1.2.1502303398.1742205645',
    '_gat_UA-103783566-41': '1',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'referer': 'https://realty.vespermoscow.com/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

base_url = 'https://realty.vespermoscow.com/be/wp-json/wp/v2/getObjects?projects=46862,7143,7927,43751&order_by=facing&order=ASC'

flats = []
count=1

current_page = 1

while True:
    try:
        # Добавляем параметр пагинации в URL
        url = f"{base_url}&page={current_page}"

        response = requests.get(url, headers=headers, cookies=cookies)

        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            break

        data = response.json()
        items = data.get("data", [])
        pagination = data.get("pagination", {})

        if not items:
            print("Данные закончились, выхожу из цикла.")
            break

        for i in items:
            date = datetime.date.today()
            project = i["project"]["name"]
            status = ''
            developer = 'Веспер'
            district = ''
            korpus = i["build"]

            if korpus==' ':
                korpus='1'

            room_count = int(i["rooms"])
            type = i["adds"]

            if type=='Особняк':
                type='Таунхаус'
            elif type=='Пентхаус, Квартира' or type=='Квартира, Терраса':
                type='Квартира'
            elif type=='Апартамент' or type=='Апартамент, Студия':
                type='Апартаменты'

            finish_type = i["facing"]

            if finish_type in ['Дизайнерский ремонт', 'Чистовая с мебелью', 'Да']:
                finish_type='С отделкой'
            else:
                finish_type='Без отделки'
            area = float(i["area"])
            old_price = int(i["price"])
            discount = ''
            section = ''
            floor = i["floor"]

            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, корпус: {korpus}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', status, '', '', developer, '',
                      district, '', '', korpus, '', '', '', '', '', '', type, finish_type, room_count, area, '',
                      old_price, discount, '', '', section, floor, '']
            flats.append(result)

            count+=1

        if pagination.get("currentPage", 0) >= pagination.get("total", 0):
            print("Все страницы обработаны, выхожу из цикла.")
            break

        current_page += 1
        time.sleep(0.1)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        break
    except Exception as e:
        print(f"Ошибка обработки данных: {e}")
        break

project = 'all'
save_flats_to_excel(flats,project, developer)