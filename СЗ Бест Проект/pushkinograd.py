import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
import requests

cookies = {
    '_ym_uid': '1744030755283890896',
    '_ym_d': '1744030755',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '_ct_ids': 'qs0dqgxt%3A70020%3A133309676',
    '_ct_session_id': '133309676',
    '_ct_site_id': '70020',
    'call_s': '___qs0dqgxt.1744032555.133309676.432809:1232068.456296:1289983.459004:1299645|2___',
    '_ct': '2900000000089086729',
    '_ct_client_global_id': '8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4',
    'cted': 'modId%3Dqs0dqgxt%3Bya_client_id%3D1744030755283890896',
    'PHPSESSID': 'tmrm5ar374fdibf6a542hbo930',
    '__hid': '01961055-78b4-7912-9693-f7550ff0c08b',
    '__buttonly_id': '62195312',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://pushkinograd.ru/plans?mode=search',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1744030755283890896; _ym_d=1744030755; _ym_isad=1; _ym_visorc=w; _ct_ids=qs0dqgxt%3A70020%3A133309676; _ct_session_id=133309676; _ct_site_id=70020; call_s=___qs0dqgxt.1744032555.133309676.432809:1232068.456296:1289983.459004:1299645|2___; _ct=2900000000089086729; _ct_client_global_id=8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4; cted=modId%3Dqs0dqgxt%3Bya_client_id%3D1744030755283890896; PHPSESSID=tmrm5ar374fdibf6a542hbo930; __hid=01961055-78b4-7912-9693-f7550ff0c08b; __buttonly_id=62195312',
}

url = 'https://pushkinograd.ru/hydra/json/data.json'

flats = []
count = 1

response = requests.get(url, cookies=cookies, headers=headers)


if response.status_code == 200:
    data = response.json()
    items = data.get('apartments', {})
    for i, j in items.items():
        if j.get('st', '') != 1:
            continue
        date = datetime.date.today()
        project = 'Пушкино Град'
        developer = 'СЗ Бест Проект'
        korpus = j.get('b', '')
        room_count = j.get('rc', '')

        if room_count == 0:
            room_count = 'студия'

        finish_type = j.get("fin", '')
        if finish_type=='Да':
            finish_type='с отделкой'
        type = 'Квартира'
        area = j.get("sq", '')
        old_price = j.get('tc', '')
        price = j.get("tcd", '')
        floor = j.get('f', '')


        print(
            f"{count} | {i} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, finish_type, room_count, area, '', old_price, '', '', price,
                  '', floor, '']
        flats.append(result)
        count += 1
else:
    print(f'Ошибка: {response.status_code}')

time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
