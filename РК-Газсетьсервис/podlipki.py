import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_far

cookies = {
    '_ym_uid': '1744299512314186285',
    '_ym_d': '1744299512',
    '_ym_isad': '1',
    'PHPSESSID': 'umst3mqt00nnqli6i8im8gig4f',
    '_ym_visorc': 'w',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://rk-gazsetservis.ru/catalog/choose/complex_1/filter/?price[]=6214000&price[]=9196000&turnId[]=0',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1744299512314186285; _ym_d=1744299512; _ym_isad=1; PHPSESSID=umst3mqt00nnqli6i8im8gig4f; _ym_visorc=w',
}

url = 'https://rk-gazsetservis.ru/catalog/api/catalog_free/?complexId[]=1&price[]=6214000&price[]=9196000&turnId[]=0&tab[]=filter'

flats = []
count = 0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("flat", [])
        items_floor = item.get("floor", [])
        items_section = item.get("section", [])
        items_korpus = item.get("turn", [])

        for i in items:
            count += 1
            date = datetime.date.today()
            project = 'Подлипки Город'
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
            developer = "РК-Газсетьсервис"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = i['viewTitle']
            finish_type = 'Предчистовая'
            room_count = int(i["room"])
            area = float(i["area"])
            price_per_metr = ''
            old_price = int(i["price"])
            discount = ''
            price_per_metr_new = ''
            floor_id = i["floorId"]
            flat_number = ''

            for j in items_floor:
                if j['id'] == floor_id:
                    floor = int(j['num'])
                    section_id = j['sectionId']

                for k in items_section:
                    if k['id'] == section_id:
                        section = int(k['num'])
                        korpus_id = k['turnId']

                    for m in items_korpus:
                        if m['id'] == korpus_id:
                            korpus = int(m['num'].split(' ')[1])

            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area},  корпус: {korpus}, секция: {section}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, '', section, floor, flat_number]
            flats.append(result)

        # Проверяем, есть ли следующая страница
        next_url = item.get("next")
        if next_url:
            url = next_url
            params = {}
        else:
            break
    else:
        print(f'Ошибка: {response.status_code}')
        break

    time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
