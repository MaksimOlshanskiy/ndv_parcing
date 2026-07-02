import datetime
import random
import time
import requests
from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

cookies = {
    'session': '0ae066b64f15cde32e751ab1bcabdf577841476ed458e8be44e04e924f92f77c',
    '_ym_uid': '1782895832964309629',
    '_ym_d': '1782895832',
    'gtm-session-start': '1782895831702',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ct_ids': 'q62wbewg%3A72043%3A312260742',
    '_ct_session_id': '312260742',
    '_ct_site_id': '72043',
    'call_s': '___q62wbewg.1782897632.312260742.449292:1268327|2___',
    '_ct': '3000000000215130256',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'tmr_lvid': 'ccdc1e5cf41c6d4788304d7d07b2ab0d',
    'tmr_lvidTS': '1782895834051',
    'cted': 'modId%3Dq62wbewg%3Bya_client_id%3D1782895832964309629',
    'domain_sid': 'rk35ijB-gYrG1aPO3kzEh%3A1782895834967',
    '_ymab_param': 'pEB4lvF_xFhef84UTABO8q_Z9x5EEp2dfr8G49yFqhFXsIgNXSqYbc8NNRX5LbGZF8f3vVpPBRNGWFYlsk3zOvRY4j4',
    'tmr_detect': '0%7C1782895836681',
    'pv_count': '2',
    'session_count_3': '2',
    'session_count_5': '2',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://vnukovocountry.club',
    'Pragma': 'no-cache',
    'Referer': 'https://vnukovocountry.club/flats',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'X-Host': 'vnukovocountry.club',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'session=0ae066b64f15cde32e751ab1bcabdf577841476ed458e8be44e04e924f92f77c; _ym_uid=1782895832964309629; _ym_d=1782895832; gtm-session-start=1782895831702; _ym_isad=2; _ym_visorc=w; _ct_ids=q62wbewg%3A72043%3A312260742; _ct_session_id=312260742; _ct_site_id=72043; call_s=___q62wbewg.1782897632.312260742.449292:1268327|2___; _ct=3000000000215130256; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; tmr_lvid=ccdc1e5cf41c6d4788304d7d07b2ab0d; tmr_lvidTS=1782895834051; cted=modId%3Dq62wbewg%3Bya_client_id%3D1782895832964309629; domain_sid=rk35ijB-gYrG1aPO3kzEh%3A1782895834967; _ymab_param=pEB4lvF_xFhef84UTABO8q_Z9x5EEp2dfr8G49yFqhFXsIgNXSqYbc8NNRX5LbGZF8f3vVpPBRNGWFYlsk3zOvRY4j4; tmr_detect=0%7C1782895836681; pv_count=2; session_count_3=2; session_count_5=2',
}

json_data = {
    'project_id': '455b97b1-8c10-433d-9588-f95702bffb47',
    'filters': [
        {
            'id': 'status',
            'type': 'system',
            'filter_type': 'select',
            'value': [
                'free',
            ],
        },
    ],
    'order_by': [
        'price',
    ],
    'limit': 16,
    'offset': 0,
}



flats = []
count = 0

while True:

    try:
        response = requests.post(
            'https://vnukovocountry.club/api/realty-filter/custom/real-estates',
            cookies=cookies,
            headers=headers,
            json=json_data,
        )

        if response.status_code == 200:
            data = response.json()

            for i in data:
                try:
                    count += 1
                    date = datetime.date.today()
                    project = i['project_name']
                    developer = "Primacom"
                    korpus = i['building_int_number']
                    room_count = i['rooms']
                    if i['type'] == 'flat':
                        type_ = 'Квартиры'
                    area = i['total_area']
                    old_price = i['old_price']
                    price = i['price']
                    section = i['section_number']
                    floor = i['floor_number']

                    if old_price == price:
                        price = None

                    print(
                        f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                    result = [
                        date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                        '', '', '', developer, '', '', '', '', str(korpus), '', '', '', '',
                        '', '', type_, 'Без отделки', room_count, area, '', old_price, '',
                        '', price, section, str(floor), ''
                    ]
                    flats.append(result)

                except Exception as e:
                    print(f"Ошибка при обработке квартиры: {e}")
                    continue

            if not data:
                break
            json_data['offset'] = str(int(json_data['offset']) + 16)
            sleep_time = random.uniform(1, 3)
            time.sleep(sleep_time)


        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')

    except Exception as e:
        print(f"Общая ошибка: {e}")



if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
