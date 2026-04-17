import datetime
import time
import requests
from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

'''
Квартирография верная с сайта, заменять не нужно!
kvartirografia=False
'''

cookies = {
    '_ym_uid': '1755692570356429176',
    '_ym_d': '1773824471',
    'tmr_lvid': 'e931ff9ecacb5734704397b771b4123f',
    'tmr_lvidTS': '1755692569566',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'scbsid_old': '2746015342',
    '_ymab_param': 'u8PrAeVsdhMKcya579QaHVUxaj451n6ucR9NZPr--TT_DYXeLi2O_Skrx4rAVhW-seGllFqWX_fs2pEIzY6MguKWqH0',
    '_ct_ids': 'aymg2z1m%3A52820%3A2266252552',
    '_ct_session_id': '2266252552',
    '_ct_site_id': '52820',
    'call_s': '___aymg2z1m.1773826270.2266252552.258214:781699|2___',
    '_ct': '800000001046937817',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'cted': 'modId%3Daymg2z1m%3Bya_client_id%3D1755692570356429176',
    'domain_sid': 'MKmoSamoQT5t6IuhLwErE%3A1773824472731',
    'tmr_detect': '0%7C1773824473232',
    'sma_session_id': '2640898315',
    'SCBfrom': '',
    'smFpId_old_values': '%5B%22cd14d52d59b08c237e2004225d23c665%22%5D',
    'accept-cookie': 'true',
    'city': '2',
    'sma_index_activity': '10602',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://msk.group-akvilon.ru/project/lot-ot-akvilon/flats/?order=price&type=flats',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1755692570356429176; _ym_d=1773824471; tmr_lvid=e931ff9ecacb5734704397b771b4123f; tmr_lvidTS=1755692569566; _ym_isad=2; _ym_visorc=w; scbsid_old=2746015342; _ymab_param=u8PrAeVsdhMKcya579QaHVUxaj451n6ucR9NZPr--TT_DYXeLi2O_Skrx4rAVhW-seGllFqWX_fs2pEIzY6MguKWqH0; _ct_ids=aymg2z1m%3A52820%3A2266252552; _ct_session_id=2266252552; _ct_site_id=52820; call_s=___aymg2z1m.1773826270.2266252552.258214:781699|2___; _ct=800000001046937817; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; cted=modId%3Daymg2z1m%3Bya_client_id%3D1755692570356429176; domain_sid=MKmoSamoQT5t6IuhLwErE%3A1773824472731; tmr_detect=0%7C1773824473232; sma_session_id=2640898315; SCBfrom=; smFpId_old_values=%5B%22cd14d52d59b08c237e2004225d23c665%22%5D; accept-cookie=true; city=2; sma_index_activity=10602',
}

params = {
    'order': 'price',
    'page': '1',
}


base_url = 'https://msk.group-akvilon.ru/api/flats/'

flats = []
count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])

    return int(digits) if digits else s

url = base_url
while url:
    response = requests.get(url, params=params, cookies=cookies, headers=headers)
    if response.status_code == 200:
        item = response.json()
        items = item.get("results", [])
        for i in items:
            date = datetime.date.today()
            project = i["project_title"].replace('Аквилон ', '').replace(' by Akvilon', '')
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
            developer = "Аквилон"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = i["building_number"].replace(' (for life)', '').replace(' (for business)', '')
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''

            srok_sdachi_old = f"{i['completion_quarter']} кв {i['completion_year']}"
            stadia = ''
            dogovor = ''

            if i['is_apartments']:
                type = 'Апартаменты'
            else:
                type = 'Квартиры'
            area = float(i["area"])
            if i['has_furnish']:
                finish_type = "С отделкой"
            else:
                finish_type = "Без отделки"
            room_count = str(i["rooms"])
            if room_count == 'None' and area > 30:
                room_count = '2'
            if room_count == 'None' and area < 30:
                room_count = 'студия'
            if room_count == '0':
                room_count = 'студия'
            if i['euro'] and room_count != 'студия':
                room_count += 'е'

            price_per_metr = ''
            old_price = i["price"]
            discount = ''
            price_per_metr_new = ''
            price = i["price_promo"]
            section = ''
            floor = i["floor"]
            flat_number = ''

            if price == old_price:
                price = None

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

        # Проверяем, есть ли следующая страница
        next_url = item.get("next")
        if next_url:
            url = next_url  # Переходим на следующую страницу
            params = {}  # Очищаем параметры, так как URL следующей страницы уже содержит их
        else:
            break  # Если следующей страницы нет, выходим из цикла
    else:
        print(f'Ошибка: {response.status_code}')
        break

    time.sleep(0.3)
project = 'all'
save_flats_to_excel(flats, project, developer, kvartirografia=False)
