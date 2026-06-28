import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    '_gcl_au': '1.1.1163854971.1781872824',
    '_ym_uid': '1781872824838601610',
    '_ym_d': '1781872824',
    'scbsid_old': '4097698043',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'tmr_lvid': '59ebeb22d0a1467bbd5509443cca0df0',
    'tmr_lvidTS': '1781872824295',
    '_ct_ids': 'n5ovc6d9%3A42226%3A939899976',
    '_ct_session_id': '939899976',
    '_ct_site_id': '42226',
    '_ct': '1600000000618158053',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'cted': 'modId%3Dn5ovc6d9%3Bya_client_id%3D1781872824838601610',
    'domain_sid': 'JDm1J6PG-cYhSEw0h9161%3A1781872826515',
    'sma_session_id': '2742494654',
    'SCBfrom': 'https%3A%2F%2Fpioneer.ru%2F',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'SCBstart': '1781872826990',
    'smFpId_old_values': '%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'PHPSESSID': 'tog4cmit2wFskzEHSVXnQGvf884eJsvS',
    'tmr_detect': '0%7C1781872877057',
    'call_s': '___n5ovc6d9.1781874749.939899976.181953:561235|2___',
    'SCBindexAct': '3677',
    'sma_index_activity': '9432',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://highlife.ru/commercial',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': '_gcl_au=1.1.1163854971.1781872824; _ym_uid=1781872824838601610; _ym_d=1781872824; scbsid_old=4097698043; _ym_isad=2; _ym_visorc=w; tmr_lvid=59ebeb22d0a1467bbd5509443cca0df0; tmr_lvidTS=1781872824295; _ct_ids=n5ovc6d9%3A42226%3A939899976; _ct_session_id=939899976; _ct_site_id=42226; _ct=1600000000618158053; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; cted=modId%3Dn5ovc6d9%3Bya_client_id%3D1781872824838601610; domain_sid=JDm1J6PG-cYhSEw0h9161%3A1781872826515; sma_session_id=2742494654; SCBfrom=https%3A%2F%2Fpioneer.ru%2F; SCBnotShow=-1; SCBporogAct=5000; SCBstart=1781872826990; smFpId_old_values=%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D; SCBFormsAlreadyPulled=true; sma_postview_ready=1; PHPSESSID=tog4cmit2wFskzEHSVXnQGvf884eJsvS; tmr_detect=0%7C1781872877057; call_s=___n5ovc6d9.1781874749.939899976.181953:561235|2___; SCBindexAct=3677; sma_index_activity=9432',
}

params = {
    'page': 'commercial',
}

flats = []
count = 1

response = requests.get('https://highlife.ru//ajax/', params=params, cookies=cookies, headers=headers)
print(response.status_code)
if response.status_code == 200:
    data = response.json()['list']


    for j in data:

        if j.get("status", '') != 'Свободно':
            continue
        date = datetime.date.today()
        project = 'High Life'
        developer = 'Pioneer'
        room_count = ''
        korpus = j.get('corpus', '').replace('К', '').strip()
        type = ''
        area = j.get("square", '')
        old_price = j.get("price", '')
        price = j.get("price_discount", '')
        floor = j.get('floor', '')
        section = ''

        if old_price == price:
            price = None

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, 'с отделкой', room_count, area, '', old_price, '', '', price,
                  section, floor, '']
        flats.append(result)
        count += 1

else:
    print(f'Ошибка: {response.status_code}')

time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
