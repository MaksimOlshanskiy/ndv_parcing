import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new


"""
Продан
"""

cookies = {
    'session': '2517abed61931d548160b12c5f0b03d393537dbc4a0d60d590e76e683ff7b29b',
    'roistat_visit': '584852',
    'roistat_first_visit': '584852',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_is_need_listen_requests': '0',
    'roistat_is_save_data_in_cookie': '1',
    '_ym_uid': '1743518439707935451',
    '_ym_d': '1743518439',
    '_ym_isad': '1',
    'roistat_marker': 'seo_google_',
    'roistat_marker_old': 'seo_google_',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old',
    '_ym_visorc': 'w',
    '___dc': '7c858f33-5c2e-4044-973f-b1eb7a94c23f',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://xn----8sbelmhdeh3apndr7lvc.xn--p1ai/flats?area_max=48',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-host': 'xn----8sbelmhdeh3apndr7lvc.xn--p1ai',
    # 'cookie': 'session=2517abed61931d548160b12c5f0b03d393537dbc4a0d60d590e76e683ff7b29b; roistat_visit=584852; roistat_first_visit=584852; roistat_visit_cookie_expire=1209600; roistat_is_need_listen_requests=0; roistat_is_save_data_in_cookie=1; _ym_uid=1743518439707935451; _ym_d=1743518439; _ym_isad=1; roistat_marker=seo_google_; roistat_marker_old=seo_google_; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old; _ym_visorc=w; ___dc=7c858f33-5c2e-4044-973f-b1eb7a94c23f',
}

params = {
    'project_id': 'd6eea882-b5e8-410d-a4d6-d9383292747d',
    'status': 'free',
    'offset': '0',
    'limit': '24',
    'order_by': 'price',
}

flats = []

try:
    response = requests.get('https://xn----8sbelmhdeh3apndr7lvc.xn--p1ai/api/realty-filter/residential/real-estates',
                            params=params,
                            headers=headers,
                            cookies=cookies)

    if response.status_code == 200:
        data = response.json()

        for i in data:
            try:
                date = datetime.date.today()
                project = 'Первый Рязанский'
                developer = "СИСдевелопмент"
                korpus = i['building_int_number']
                room_count = i['rooms']
                type_ = "Квартира"
                area = i['total_area']
                price_per_metr = i['old_ppm']
                old_price = i['old_price']
                price_per_metr_new = i['ppm']
                price = i['price']
                section = i['section_number']
                floor = i['floor_number']

                print(
                    f"{project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    'Продан', '', '', developer, '', '', '', '', float(str(korpus)), '', '', '', '',
                    '', '', type_, 'Без отделки', room_count, area, int(price_per_metr), int(old_price), '',
                    '', int(price), int(section), int(str(floor)), ''
                ]
                flats.append(result)

            except Exception as e:
                print(f"Ошибка при обработке квартиры: {e}")
                continue

    else:
        print(f'Ошибка запроса: {response.status_code}, {response.text}')

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, 'Первый Рязанский', 'СИСдевелопмент')
else:
    print("Нет данных для сохранения")
