import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

cookies = {
    '_ct': '3100000002889012760',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_uid': '1745588248351634478',
    '_ym_d': '1763648083',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_first_add': 'fd%3D2025-11-20%2017%3A14%3A42%7C%7C%7Cep%3Dhttps%3A%2F%2Fdonstroy.moscow%2Ffull-search%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fdonstroy.moscow%2F',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
    'tmr_lvid': 'e0dcbecb89a2a37efdd9c3e08f83390c',
    'tmr_lvidTS': '1745588249051',
    'sbjs_current_add': 'fd%3D2025-11-21%2009%3A42%3A45%7C%7C%7Cep%3Dhttps%3A%2F%2Fdonstroy.moscow%2Fobjects%2Fnachalo%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fyandex.ru%2F',
    'sbjs_current': 'typ%3Dreferral%7C%7C%7Csrc%3Dyandex.ru%7C%7C%7Cmdm%3Dreferral%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%2F%7C%7C%7Ctrm%3D%28none%29',
    'agree-cookie': '1',
    'PHPSESSID': 'jtHtwN94NWiwp0m3CpcXjgN9yHpBFVfU',
    'BITRIX_CONVERSION_CONTEXT_sm': '%7B%22ID%22%3A68%2C%22EXPIRE%22%3A1764622740%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    'cted': 'modId%3Ddde5d0a5%3Bya_client_id%3D1745588248351634478%7CmodId%3D36b04ec4%3Bya_client_id%3D1745588248351634478',
    '_ct_ids': '36b04ec4%3A13517%3A1225902331_dde5d0a5%3A7883%3A4904082096',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'sbjs_udata': 'vst%3D4%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F142.0.0.0%20Safari%2F537.36',
    'd_session_start_time': '1764596856192',
    'domain_sid': 'Ko8nhcVLMJEX5YUs1eWe4%3A1764596858992',
    '_ct_session_id': '4904082096',
    '_ct_site_id': '7883',
    'call_s': '___36b04ec4.1764598670.1225902331.251833:770624|dde5d0a5.1764598670.4904082096.163277:157967|2___',
    'sbjs_session': 'pgs%3D3%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fdonstroy.moscow%2Ffull-search%2F',
    'tmr_detect': '0%7C1764596873095',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://donstroy.moscow',
    'priority': 'u=1, i',
    'referer': 'https://donstroy.moscow/full-search/?price%5B%5D=17.8&price%5B%5D=915.2&area%5B%5D=27&area%5B%5D=392&floor_number%5B%5D=2&floor_number%5B%5D=37&floor_first_last=false&discount=false&furnish=false&apartments=false&secondary=false&sort=price-asc&view_type=flats&page=2&view=card',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '_ct=3100000002889012760; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_uid=1745588248351634478; _ym_d=1763648083; sbjs_migrations=1418474375998%3D1; sbjs_first_add=fd%3D2025-11-20%2017%3A14%3A42%7C%7C%7Cep%3Dhttps%3A%2F%2Fdonstroy.moscow%2Ffull-search%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fdonstroy.moscow%2F; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; tmr_lvid=e0dcbecb89a2a37efdd9c3e08f83390c; tmr_lvidTS=1745588249051; sbjs_current_add=fd%3D2025-11-21%2009%3A42%3A45%7C%7C%7Cep%3Dhttps%3A%2F%2Fdonstroy.moscow%2Fobjects%2Fnachalo%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fyandex.ru%2F; sbjs_current=typ%3Dreferral%7C%7C%7Csrc%3Dyandex.ru%7C%7C%7Cmdm%3Dreferral%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%2F%7C%7C%7Ctrm%3D%28none%29; agree-cookie=1; PHPSESSID=jtHtwN94NWiwp0m3CpcXjgN9yHpBFVfU; BITRIX_CONVERSION_CONTEXT_sm=%7B%22ID%22%3A68%2C%22EXPIRE%22%3A1764622740%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; cted=modId%3Ddde5d0a5%3Bya_client_id%3D1745588248351634478%7CmodId%3D36b04ec4%3Bya_client_id%3D1745588248351634478; _ct_ids=36b04ec4%3A13517%3A1225902331_dde5d0a5%3A7883%3A4904082096; _ym_isad=2; _ym_visorc=w; sbjs_udata=vst%3D4%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F142.0.0.0%20Safari%2F537.36; d_session_start_time=1764596856192; domain_sid=Ko8nhcVLMJEX5YUs1eWe4%3A1764596858992; _ct_session_id=4904082096; _ct_site_id=7883; call_s=___36b04ec4.1764598670.1225902331.251833:770624|dde5d0a5.1764598670.4904082096.163277:157967|2___; sbjs_session=pgs%3D3%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fdonstroy.moscow%2Ffull-search%2F; tmr_detect=0%7C1764596873095',
}

json_data = {
    'price': [
        17.8,
        915.2,
    ],
    'area': [
        27,
        392,
    ],
    'floor_number': [
        2,
        37,
    ],
    'rooms': [],
    'projects': [],
    'quarters': [],
    'buildings': [],
    'advantages': [],
    'floor_first_last': False,
    'discount': False,
    'furnish': False,
    'apartments': False,
    'secondary': False,
    'category': None,
    'sort': 'price-asc',
    'view_type': 'flats',
    'page': 1,
}

flats = []
count=0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while True:

    response = requests.post(
        'https://donstroy.moscow/api/v1/flatssearch/choose_params_api_flats/',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    result = []
    items = response.json().get("flats", [])

    print(f'Сейчас страница номер {json_data['page']}')
    for i in items:
        if not i["isUtp"]:
            count+=1
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
            developer = "Донстрой"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            if i["quarter"]:
                korpus = f"{i["quarter"]} корп. {i["building"]}"
            else:
                korpus = i["building"]
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = 'Квартира'

            try:
                if i['labels'][0]['title'] == 'Отделка':
                    finish_type = "С отделкой"
                else:
                    finish_type = 'Без отделки'
            except:
                finish_type = 'Без отделки'

            room_count = i["rooms"]

            if room_count==0:
                room_count='студия'

            area = float(i["area"])
            price_per_metr = ''
            old_price = i["price_old"]
            discount = ''
            price_per_metr_new = ''
            price = i["price"]
            section = i["section"]
            floor = i["floor"]
            flat_number = ''

            if old_price == None:
                old_price = price
                price=None
        else:
            continue

        print(
            f"{count} | {project}, дата: {date}, отделка: {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

    json_data['page'] = str(int(json_data['page']) + 1)
    try:
        if not result:
            print(f"Данные закончились на странице {json_data['page']}.")
            break
    except:
        ''
    print('-------------------------------------------------------------------')

    time.sleep(0.1)

project = 'all'
save_flats_to_excel(flats, project, developer)
