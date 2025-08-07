import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

cookies = {
    'PHPSESSID': '48SfpibSVlcqePSJGRzMlBrj9mCnREBf',
    'BX_USER_ID': '7c7565be1314918dd51b7cd2a5978979',
    'BITRIX_CONVERSION_CONTEXT_sm': '%7B%22ID%22%3A82%2C%22EXPIRE%22%3A1741899540%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    '_ct': '3100000002821121974',
    '_ct_client_global_id': 'b7bf8ff5-0827-5c41-830e-bad9491c1c5e',
    '_ct_ids': 'dde5d0a5%3A7883%3A4795557837_36b04ec4%3A13517%3A1124557406',
    '_ym_uid': '1741862569989643464',
    '_ym_d': '1741862569',
    '_ym_isad': '1',
    '_gid': 'GA1.2.62523463.1741862569',
    'd_session_start_time': '1741862569438',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_first_add': 'fd%3D2025-03-13%2013%3A42%3A49%7C%7C%7Cep%3Dhttps%3A%2F%2Fdonstroy.moscow%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F',
    'sbjs_current': 'typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
    'sbjs_first': 'typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
    'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F134.0.0.0%20Safari%2F537.36',
    '_ym_visorc': 'w',
    'cted': 'modId%3Ddde5d0a5%3Bclient_id%3D2018500939.1741862569%3Bya_client_id%3D1741862569989643464%7CmodId%3D36b04ec4%3Bclient_id%3D2018500939.1741862569%3Bya_client_id%3D1741862569989643464',
    'sbjs_current_add': 'fd%3D2025-03-13%2013%3A46%3A01%7C%7C%7Cep%3Dhttps%3A%2F%2Fdonstroy.moscow%2Fbuy-living%2Fliving-objects%2F%3Ftype%3Dlist%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F',
    '_gat_UA-79524626-1': '1',
    '_gat': '1',
    '_ct_session_id': '1124557406',
    '_ct_site_id': '13517',
    'call_s': '___dde5d0a5.1741864627.4795557837.163277:435675|36b04ec4.1741864627.1124557406.251833:770624|2___',
    'sbjs_session': 'pgs%3D14%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fdonstroy.moscow%2Ffull-search%2F',
    '_ga_H36T4JN56M': 'GS1.1.1741862569.1.1.1741862828.51.0.0',
    '_ga': 'GA1.1.2018500939.1741862569',
    '_ga_LJV2D2Z2D2': 'GS1.1.1741862569.1.1.1741862828.0.0.0',
    '_ga_F522MVXW9K': 'GS1.2.1741862569.1.1.1741862828.9.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'content-type': 'application/json',
    'origin': 'https://donstroy.moscow',
    'priority': 'u=1, i',
    'referer': 'https://donstroy.moscow/full-search/?price%5B%5D=14.8&price%5B%5D=545.2&area%5B%5D=21&area%5B%5D=392&floor_number%5B%5D=1&floor_number%5B%5D=50&floor_first_last=false&discount=false&furnish=false&apartments=false&secondary=false&sort=price-asc&view_type=flats&page=1&view=card',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=48SfpibSVlcqePSJGRzMlBrj9mCnREBf; BX_USER_ID=7c7565be1314918dd51b7cd2a5978979; BITRIX_CONVERSION_CONTEXT_sm=%7B%22ID%22%3A82%2C%22EXPIRE%22%3A1741899540%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; _ct=3100000002821121974; _ct_client_global_id=b7bf8ff5-0827-5c41-830e-bad9491c1c5e; _ct_ids=dde5d0a5%3A7883%3A4795557837_36b04ec4%3A13517%3A1124557406; _ym_uid=1741862569989643464; _ym_d=1741862569; _ym_isad=1; _gid=GA1.2.62523463.1741862569; d_session_start_time=1741862569438; sbjs_migrations=1418474375998%3D1; sbjs_first_add=fd%3D2025-03-13%2013%3A42%3A49%7C%7C%7Cep%3Dhttps%3A%2F%2Fdonstroy.moscow%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F; sbjs_current=typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_first=typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F134.0.0.0%20Safari%2F537.36; _ym_visorc=w; cted=modId%3Ddde5d0a5%3Bclient_id%3D2018500939.1741862569%3Bya_client_id%3D1741862569989643464%7CmodId%3D36b04ec4%3Bclient_id%3D2018500939.1741862569%3Bya_client_id%3D1741862569989643464; sbjs_current_add=fd%3D2025-03-13%2013%3A46%3A01%7C%7C%7Cep%3Dhttps%3A%2F%2Fdonstroy.moscow%2Fbuy-living%2Fliving-objects%2F%3Ftype%3Dlist%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F; _gat_UA-79524626-1=1; _gat=1; _ct_session_id=1124557406; _ct_site_id=13517; call_s=___dde5d0a5.1741864627.4795557837.163277:435675|36b04ec4.1741864627.1124557406.251833:770624|2___; sbjs_session=pgs%3D14%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fdonstroy.moscow%2Ffull-search%2F; _ga_H36T4JN56M=GS1.1.1741862569.1.1.1741862828.51.0.0; _ga=GA1.1.2018500939.1741862569; _ga_LJV2D2Z2D2=GS1.1.1741862569.1.1.1741862828.0.0.0; _ga_F522MVXW9K=GS1.2.1741862569.1.1.1741862828.9.0.0',
}

json_data = {
    'price': [
        14.8,
        911.2,
    ],
    'area': [
        21,
        392,
    ],
    'floor_number': [
        1,
        50,
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


page = 1
for page in range(1, 80):
    json_data["page"] = page

    response = requests.post(
        'https://donstroy.moscow/api/v1/flatssearch/choose_params_api_flats/',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    items = response.json().get("flats", [])
    if not items:
        print(f"Данные закончились на странице {page}.")
        break
    print('-------------------------------------------------------------------')
    print(f'Сейчас страница номер {page}')
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

    page += 1

    time.sleep(0.1)

project = 'all'
save_flats_to_excel(flats, project, developer)
