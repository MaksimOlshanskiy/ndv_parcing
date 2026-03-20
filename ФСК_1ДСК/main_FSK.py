import datetime
import time
import pandas as pd
import os
import requests
from functions import save_flats_to_excel
from info_FSK import info
from save_to_excel import save_flats_to_excel_old_new_all

cookies = {
    '_ym_uid': '1741781835642692654',
    '_ym_d': '1771224225',
    '_fsid': 's%3AEHKx_6TePG56nbbpaYWSXV3x0dmKrhYq.CRIoMIyCDya95LOFiF7leSBGvJS63xWGx5hoU%2Bx1U98',
    '_yasc': 'hLz8egujrYqNIqN1VoEc+BqCVi8Z8JB6tajx2LRyQoEE/dVsanlRTBFVk8g83ta1',
    '_ymab_param': 'SUP7c35MZAs1-Pcnn5erhZFipV8NkDaJ0RB-XqtbAX3Q5YbrYOC5l3hX3PBH2tCjAK7FhnPzyjFRBUchSLVlYa1xXZw',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'PageNumber': 'NaN',
    'flomni_641ae9eee9a473ff3717a7c0': '{%22userHash%22:%220121d7b1-12e1-4fb6-ae93-f18c3a2d1cb1%22}',
    'scbsid_old': '2746015342',
    'adtech_uid': '466a3f2e-2ea3-4a9d-8389-d8d285df8b95%3Afsk.ru',
    'top100_id': 't1.7712007.1828860295.1773830293747',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'tmr_lvid': '4637ab7ced736fe4a09be7a27da22233',
    'tmr_lvidTS': '1741781835461',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1773916693861%2C%22sl%22%3A%7B%22224%22%3A1773830293861%2C%221228%22%3A1773830293861%7D%7D',
    '__upin': 'uiym2TZM/0r3xWqRBX6KrA',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '_cmg_csstxWdO1': '1773830294',
    '_comagic_idxWdO1': '12407298571.16953783611.1773830293',
    'adrdel': '1773830294065',
    'tmr_detect': '0%7C1773830296549',
    'sma_session_id': '2641004276',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22ab19ac2380782ae239d725bfec8e9f49%22%5D',
    'SCBstart': '1773830296986',
    'SCBporogAct': '5000',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    't3_sid_7712007': 's1.277257722.1773830293748.1773830758407.1.20.7.1..',
    'sma_index_activity': '5749',
    'SCBindexAct': '2865',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'apiclient': 'FSK',
    'priority': 'u=1, i',
    'referer': 'https://fsk.ru/flats/list',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1741781835642692654; _ym_d=1771224225; _fsid=s%3AEHKx_6TePG56nbbpaYWSXV3x0dmKrhYq.CRIoMIyCDya95LOFiF7leSBGvJS63xWGx5hoU%2Bx1U98; _yasc=hLz8egujrYqNIqN1VoEc+BqCVi8Z8JB6tajx2LRyQoEE/dVsanlRTBFVk8g83ta1; _ymab_param=SUP7c35MZAs1-Pcnn5erhZFipV8NkDaJ0RB-XqtbAX3Q5YbrYOC5l3hX3PBH2tCjAK7FhnPzyjFRBUchSLVlYa1xXZw; _ym_isad=2; _ym_visorc=w; PageNumber=NaN; flomni_641ae9eee9a473ff3717a7c0={%22userHash%22:%220121d7b1-12e1-4fb6-ae93-f18c3a2d1cb1%22}; scbsid_old=2746015342; adtech_uid=466a3f2e-2ea3-4a9d-8389-d8d285df8b95%3Afsk.ru; top100_id=t1.7712007.1828860295.1773830293747; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; tmr_lvid=4637ab7ced736fe4a09be7a27da22233; tmr_lvidTS=1741781835461; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1773916693861%2C%22sl%22%3A%7B%22224%22%3A1773830293861%2C%221228%22%3A1773830293861%7D%7D; __upin=uiym2TZM/0r3xWqRBX6KrA; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _cmg_csstxWdO1=1773830294; _comagic_idxWdO1=12407298571.16953783611.1773830293; adrdel=1773830294065; tmr_detect=0%7C1773830296549; sma_session_id=2641004276; SCBfrom=https%3A%2F%2Fyandex.ru%2F; SCBnotShow=-1; smFpId_old_values=%5B%22ab19ac2380782ae239d725bfec8e9f49%22%5D; SCBstart=1773830296986; SCBporogAct=5000; SCBFormsAlreadyPulled=true; sma_postview_ready=1; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; t3_sid_7712007=s1.277257722.1773830293748.1773830758407.1.20.7.1..; sma_index_activity=5749; SCBindexAct=2865',
}

params = {
    'offset': '22',
    'limit': '24',
    'sort': 'price',
    'order': '1',
    'city': '1',
}



flats = []
count = 0

while True:

    response = requests.get('https://fsk.ru/api/v3/flats', params=params, cookies=cookies, headers=headers)
    print(response.status_code)

    def extract_digits_or_original(s):
        digits = ''.join([char for char in s if char.isdigit()])
        return int(digits) if digits else s

    items = response.json()['items']

    for i in items:
        count += 1
        url = ''
        date = datetime.date.today()
        project = i["project"]["title"]
        developer = "ФСК"
        korpus = i["corpus"]["number"]
        type = i["crmObjectType"]
        finish_type = ''
        for j in i['labels']:
           if 'отделк' in j['title'].lower():
               finish_type = j['title']

        if finish_type == 'Отделка White Box + с/у под ключ' or finish_type == 'Отделка White Box':
            finish_type = 'Предчистовая'
        elif finish_type == 'Чистовая отделка':
            finish_type = 'С отделкой'
        else:
            finish_type='Без отделки'

        if type == 'Студия':
            room_count = 'Студия'
            type = 'Квартира'
        else:
            room_count = int(i["crmRoomsQty"])

        area = i["areaTotal"]
        old_price = i["priceWoDiscount"]
        price = i["price"]
        section = i["section"]["number"]
        try:
            floor = int(i["floor"]["number"])
        except:
            floor = int(i["floor"]["number"].split('.')[0])
        flat_number = ''

        if old_price == price:
            price = None


        print(
            f"{count}, {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [
            date, project, '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', developer,
            '', '', '', '', korpus, '', '', '', '', '',
            '', type, finish_type, room_count, area, '', old_price, '', '',
            price, section, floor, ''
        ]
        flats.append(result)

    time.sleep(0.05)
    params['offset'] = str(int(params['offset']) + 24)
    if not items:
        break

save_flats_to_excel(flats, 'all', developer)
