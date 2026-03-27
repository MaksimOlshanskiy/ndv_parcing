import datetime
import time
from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

'''
Если на сайте появятся скидки, то нужно изменить код!!!!
'''

cookies = {
    '_ym_uid': '1773754191319419251',
    '_ym_d': '1773754191',
    'cted': 'modId%3D666dpp3f%3Bya_client_id%3D1773754191319419251',
    '_ym_visorc': 'w',
    '_ym_isad': '2',
    '_ct_ids': '666dpp3f%3A76887%3A146757741',
    '_ct_session_id': '146757741',
    '_ct_site_id': '76887',
    'call_s': '___666dpp3f.1773755990.146757741.519660:1480077|2___',
    '_ct': '3300000000093608991',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'c2d_widget_id': '{%225c44cbd0f5e16025091c61e6341e3fcf%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%209d011977470988548616%5C%22%2C%5C%22client_token%5C%22:%5C%2267d606bb28401523a434fd644d2da804%5C%22}%22}',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://enigmiya.ru/search',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1773754191319419251; _ym_d=1773754191; cted=modId%3D666dpp3f%3Bya_client_id%3D1773754191319419251; _ym_visorc=w; _ym_isad=2; _ct_ids=666dpp3f%3A76887%3A146757741; _ct_session_id=146757741; _ct_site_id=76887; call_s=___666dpp3f.1773755990.146757741.519660:1480077|2___; _ct=3300000000093608991; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; c2d_widget_id={%225c44cbd0f5e16025091c61e6341e3fcf%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%209d011977470988548616%5C%22%2C%5C%22client_token%5C%22:%5C%2267d606bb28401523a434fd644d2da804%5C%22}%22}',
}

url = 'https://enigmiya.ru/api/hydra/data'

flats = []
count = 1

response = requests.get(url, cookies=cookies, headers=headers)
korpus_dict = {'Б' : 'Атлас', 'Г' : 'Монте Бьянко', 'В' : 'Олимп', 'А' : 'Эльбрус'}

if response.status_code == 200:
    data = response.json()
    items = data.get('apartments', {})


    for i, j in items.items():

        if j.get('st', '') == 0:
            continue

        date = datetime.date.today()
        project = 'Энигмия'
        developer = 'Upside Development'
        korpus = j.get('s', '')
        korpus = korpus_dict.get(korpus, korpus)
        room_count = j.get('s', '')

        if room_count==0:
            room_count='студия'

        finish_type = j.get("spec_fl", '')
        if finish_type=='White-box':
            finish_type='Предчистовая'
        elif finish_type=='Чистовая':
            finish_type='С отделкой'
        else:
            finish_type = 'Без отделки'
        type = 'Квартира'


        area = j.get("sq", '')
        price = ''
        old_price = j.get("tc", '')
        floor = j.get('f', '')
        if price == 0:
            continue

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, finish_type, room_count, area, '',old_price, '', '', price,
                  '', floor, '']
        flats.append(result)
        count += 1
else:
    print(f'Ошибка: {response.status_code}')


time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
