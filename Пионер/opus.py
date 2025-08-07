import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    '_ym_uid': '1745412129890419896',
    '_ym_d': '1753358210',
    '_ym_isad': '1',
    'cted': 'modId%3D71fwuvpy%3Bya_client_id%3D1745412129890419896',
    '_ym_visorc': 'w',
    'favorites': '[]',
    '_ct_ids': '71fwuvpy%3A53903%3A608172452',
    '_ct_session_id': '608172452',
    '_ct_site_id': '53903',
    '_ct': '2200000000392384147',
    '_ct_client_global_id': '8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4',
    'scbsid_old': '2796070936',
    'PHPSESSID': 'QUwa6b0i7jmUzVuCowxjRda4D9XF2HBK',
    'sma_session_id': '2368924052',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%22a932251185d3bf41fcd7e2656de279f5%22%5D',
    'SCBstart': '1753358213734',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'call_s': '___71fwuvpy.1753360064.608172452.269303:870535|2___',
    'sma_index_activity': '7326',
    'SCBindexAct': '1324',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://opus-home.ru/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1745412129890419896; _ym_d=1753358210; _ym_isad=1; cted=modId%3D71fwuvpy%3Bya_client_id%3D1745412129890419896; _ym_visorc=w; favorites=[]; _ct_ids=71fwuvpy%3A53903%3A608172452; _ct_session_id=608172452; _ct_site_id=53903; _ct=2200000000392384147; _ct_client_global_id=8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4; scbsid_old=2796070936; PHPSESSID=QUwa6b0i7jmUzVuCowxjRda4D9XF2HBK; sma_session_id=2368924052; SCBfrom=; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%22a932251185d3bf41fcd7e2656de279f5%22%5D; SCBstart=1753358213734; SCBFormsAlreadyPulled=true; sma_postview_ready=1; call_s=___71fwuvpy.1753360064.608172452.269303:870535|2___; sma_index_activity=7326; SCBindexAct=1324',
}

params = {
    'page': 'flats',
}

url = 'https://opus-home.ru/ajax/'

flats = []
count = 1

response = requests.get(url, params=params, cookies=cookies, headers=headers)

if response.status_code == 200:
    data = response.json()

    for j in data:
        date = datetime.date.today()
        project = 'Opus'
        developer = 'Pioneer'
        room_count = j.get('rooms', '')
        korpus = '1'
        type = 'Квартира'
        area = j.get("square", '')
        old_price = j.get("price", '')
        price = j.get("price_sale", '')
        floor = j.get('floor', '')
        section = j.get('section', '')

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

project = 'Opus'
developer = 'Pioneer'

save_flats_to_excel(flats, project, developer)
