import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    '__ddg9_': '89.188.120.54',
    '__ddg1_': 'bwEhbi7zhadZ78CFkiAB',
    'scbsid_old': '2750244825',
    '_ym_uid': '1742468874962745286',
    '_ym_d': '1742468874',
    '_ym_isad': '1',
    '_ga': 'GA1.1.368739333.1742468875',
    '_ct_ids': 'xh6o3uby%3A56302%3A422644728',
    '_ct_session_id': '422644728',
    '_ct_site_id': '56302',
    'call_s': '___xh6o3uby.1742470670.422644728.299425:886510|2___',
    '_ct': '2300000000274725784',
    'counter_upside': '2',
    '_ym_visorc': 'w',
    '_ct_client_global_id': 'b7bf8ff5-0827-5c41-830e-bad9491c1c5e',
    'cted': 'modId%3Dxh6o3uby%3Bclient_id%3D368739333.1742468875%3Bya_client_id%3D1742468874962745286',
    '_ga_VLBX0FNVL2': 'GS1.1.1742468874.1.1.1742468885.49.0.0',
    '__ddg10_': '1742468882',
    '__ddg8_': 'Cxw8ID1vuvLXWoPm',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://upside-towers.ru/search?sq=min~22.77000,max~113.89000&tc=min~15658400.00000,max~59518360.00000',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

url = 'https://upside-towers.ru/hydra/json/data.json'

flats = []
count = 1

response = requests.get(url, cookies=cookies, headers=headers)
korpus_dict = {'Б' : 'Атлас', 'Г' : 'Монте Бьянко', 'В' : 'Олимп', 'А' : 'Эльбрус'}

if response.status_code == 200:
    data = response.json()
    items = data.get('apartments', {})

    for i, j in items.items():
        date = datetime.date.today()
        project = 'Апсайд Тауэрс'
        developer = 'Upside Development'
        korpus = j.get('tr_n', '')[0]
        korpus = korpus_dict.get(korpus, korpus)
        room_count = j.get('rc', '')

        if room_count==0:
            room_count='студия'

        finish_type = j.get("spec_fl", '')
        if finish_type=='White-box':
            finish_type='Предчистовая'
        elif finish_type=='Чистовая':
            finish_type='С отделкой'
        type = 'Квартира'


        area = j.get("sq", '')
        price = j.get("tc", '')
        floor = j.get('f', '')
        if price == 0:
            continue

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, finish_type, room_count, area, '', price, '', '', '',
                  '', floor, '']
        flats.append(result)
        count += 1
else:
    print(f'Ошибка: {response.status_code}')


time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
