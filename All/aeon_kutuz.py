import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import time

cookies = {
    'PHPSESSID': 'zmEjsXT2CPXUAlDH1QlAvm2sbjz3eoXF',
    '_ym_uid': '1742298891216037287',
    '_ym_d': '1742298891',
    '_ym_isad': '1',
    '_cmg_csstf0FGE': '1742298891',
    '_comagic_idf0FGE': '10432403754.14548838459.1742298890',
    'comagicphone': '+7 (495) 431-02-27',
    '_ym_visorc': 'w',
    'pageCount': '6',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'priority': 'u=1, i',
    'referer': 'https://riverpark-kutuzovskiy.ru/flats/~PwZT/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

base_url = 'https://riverpark-kutuzovskiy.ru/ajax/flats/index.php?filter=%7B%22price%22:[24,289],%22sq%22:[21,152],%22type%22:[%22%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0%22],%22project%22:[],%22stage%22:[],%22rooms%22:[],%22floor%22:[%222.00%22,%2245.00%22],%22ids%22:[],%22views%22:[],%22building%22:[],%22section%22:[],%22advantages%22:[],%22penthouse%22:[],%22plantype%22:[],%22flat%22:%22%22%7D&sort=%7B%22rooms%22:2%7D&page={page}&cnt=30'

flats = []
count = 1
page = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while True:
    # Формируем URL для текущей страницы
    url = base_url.format(page=page)

    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("data", [])

        if not items:
            break

        for i in items:
            date = datetime.date.today()
            project = i["project"]
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
            developer = "Аеон"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = i["building"]
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = i["rooms_text"]
            finish_type = i['finishing']

            if finish_type == 'White Box':
                finish_type = 'Предчистовая'

            try:
                room_count = int(i["rooms_text"].split('-')[0])
            except:
                room_count = 0
                if room_count == 0:
                    room_count = 'студия'

            if '-комнатная' in type:
                type = 'Квартира'

            type = 'Квартира'
            area = float(i["sq"])
            price_per_metr = ''
            old_price = int(i["price"].replace(' ', ''))
            discount = ''
            price_per_metr_new = ''
            price = ''
            section = i["section"]
            floor = int(i["floor"])
            flat_number = ''

            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)

            count += 1
    else:
        print(f'Ошибка: {response.status_code}')
        break

    # Увеличиваем номер страницы
    page += 1

    time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
