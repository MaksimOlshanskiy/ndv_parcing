import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

cookies = {
    'tmr_lvid': 'e94763e313a52e7170abe50b899e64c9',
    'tmr_lvidTS': '1773837913705',
    '_ym_uid': '1773837914119497773',
    '_ym_d': '1773837914',
    'cted': 'modId%3Dg5n13ae1%3Bya_client_id%3D1773837914119497773',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ct_ids': 'g5n13ae1%3A69971%3A365436878',
    '_ct_session_id': '365436878',
    '_ct_site_id': '69971',
    '_ct': '2900000000240335852',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'domain_sid': 'x_TYSbjMdlTCLl2GxdLX2%3A1773837915840',
    'ab_id': '96f16094b31fd2110ff55fc91f19e89f8503133d',
    'call_s': '___g5n13ae1.1773839749.365436878.476321:1353097|2___',
    'tmr_detect': '0%7C1773837951473',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://oktoberdom.ru/flats',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': 'tmr_lvid=e94763e313a52e7170abe50b899e64c9; tmr_lvidTS=1773837913705; _ym_uid=1773837914119497773; _ym_d=1773837914; cted=modId%3Dg5n13ae1%3Bya_client_id%3D1773837914119497773; _ym_isad=2; _ym_visorc=w; _ct_ids=g5n13ae1%3A69971%3A365436878; _ct_session_id=365436878; _ct_site_id=69971; _ct=2900000000240335852; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; domain_sid=x_TYSbjMdlTCLl2GxdLX2%3A1773837915840; ab_id=96f16094b31fd2110ff55fc91f19e89f8503133d; call_s=___g5n13ae1.1773839749.365436878.476321:1353097|2___; tmr_detect=0%7C1773837951473',
}

url = 'https://oktoberdom.ru/api/property/find'

flats = []
count = 1

response = requests.get(url, cookies=cookies, headers=headers)
print(response.status_code)
if response.status_code == 200:
    item = response.json()
    items = item.get("properties", [])

    for i in items:
        date = datetime.date.today()
        developer = 'Карандаш'
        project = 'Октябрьский'
        korpus = '1'
        room_count = i['rooms']
        finish_type = i['decorationName'].replace('WhiteBox', 'Предчистовая').replace('Классика', 'С отделкой').replace('Модерн', 'С отделкой').replace('Модерн', 'С отделкой')
        type = i['type'].replace('flat', 'квартиры')
        area = i['space']
        old_price = i['price']
        price = i['discountedPrice']
        section = i['section']
        floor = i['floor']

        if old_price == price:
            price = None

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, finish_type, room_count, area, '', old_price, '', '', price,
                  section, floor, '']
        flats.append(result)
        count += 1
else:
    print(f'Ошибка: {response.status_code}')

time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
