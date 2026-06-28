# 'limit': '2000'  можно изменить, лучше посмотреть сколько квартир доступно на сайте

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os

from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1780062499353899720',
    '_ym_d': '1780062499',
    'mindboxDeviceUUID': 'd6b3597d-4b0b-4e45-8167-0b84971b36f7',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D',
    '__eventn_id': '284986cf-6631-400a-8835-823f390cf17c',
    '_gcl_au': '1.1.1333750330.1780062500',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    'carrotquest_device_guid': '6774b2a8-bede-478b-998c-269df5909a6d',
    'carrotquest_uid': '2247765268963001076',
    'carrotquest_auth_token': 'user.2247765268963001076.51753-776395ac10b7ee9e1ccd2b8213.86af9792c58b56cc5ecf487f6e3f25309e155c147a135f7a',
    'csrftoken': 'YjkHuy7WIus76rRBoaMaNxV4cWNtRqTx',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'tmr_lvid': '5a177ccfb44c98e090dccda7d3650dd8',
    'tmr_lvidTS': '1780062503153',
    '_ym_isad': '2',
    'carrotquest_realtime_services_transport': 'wss',
    'carrotquest_jwt_access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3ODE3OTA5NjAsImlhdCI6MTc4MTc4NzM2MCwianRpIjoiN2Y5YTBiNDRhOTAyNGIxMGI1NmJjOWNkNjM3ZTUxNmMiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDo1MTc1My4kdXNlcl9pZDoyMjQ3NzY1MjY4OTYzMDAxMDc2Il0sImFwcF9pZCI6NTE3NTMsInVzZXJfaWQiOjIyNDc3NjUyNjg5NjMwMDEwNzZ9.OHYX-hdbvfZhtKeTD9-lTZFhe6XAc38a8Dpea4N0tnQ',
    'first_page': 'https://moskva.brusnika.ru/',
    'scbsid_old': '4097698043',
    'adrdel': '1781787363873',
    'adrdel': '1781787363873',
    'acs_3': '%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1781873763884%2C%22sl%22%3A%7B%22224%22%3A1781787363884%2C%221228%22%3A1781787363884%7D%7D',
    'acs_3': '%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1781873763884%2C%22sl%22%3A%7B%22224%22%3A1781787363884%2C%221228%22%3A1781787363884%7D%7D',
    '_cmg_csstPowxG': '1781787364',
    '_comagic_idPowxG': '13442635939.17918895329.1781787361',
    '_ym_visorc': 'w',
    'domain_sid': 'bcpIyyNCjvwJccKhz9O9z%3A1781787365316',
    'sma_session_id': '2741306055',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D',
    'SCBstart': '1781787366246',
    'SCBFormsAlreadyPulled': 'true',
    'undefined': '6.179',
    'carrotquest_session': 'eh0o2hjy155s235zjdqqxgj8swqirv4a',
    'carrotquest_session_started': '1',
    'pageviewCount': '2',
    'tmr_detect': '0%7C1781787375173',
    'sma_index_activity': '1594',
    'SCBindexAct': '1194',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://moskva.brusnika.ru/commercial/',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'x-csrftoken': 'YjkHuy7WIus76rRBoaMaNxV4cWNtRqTx',
    # 'cookie': '_ym_uid=1780062499353899720; _ym_d=1780062499; mindboxDeviceUUID=d6b3597d-4b0b-4e45-8167-0b84971b36f7; directCrm-session=%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D; __eventn_id=284986cf-6631-400a-8835-823f390cf17c; _gcl_au=1.1.1333750330.1780062500; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; carrotquest_device_guid=6774b2a8-bede-478b-998c-269df5909a6d; carrotquest_uid=2247765268963001076; carrotquest_auth_token=user.2247765268963001076.51753-776395ac10b7ee9e1ccd2b8213.86af9792c58b56cc5ecf487f6e3f25309e155c147a135f7a; csrftoken=YjkHuy7WIus76rRBoaMaNxV4cWNtRqTx; adrcid=A0r9KB4fc8duMUv2jPsp-tg; adrcid=A0r9KB4fc8duMUv2jPsp-tg; tmr_lvid=5a177ccfb44c98e090dccda7d3650dd8; tmr_lvidTS=1780062503153; _ym_isad=2; carrotquest_realtime_services_transport=wss; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3ODE3OTA5NjAsImlhdCI6MTc4MTc4NzM2MCwianRpIjoiN2Y5YTBiNDRhOTAyNGIxMGI1NmJjOWNkNjM3ZTUxNmMiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDo1MTc1My4kdXNlcl9pZDoyMjQ3NzY1MjY4OTYzMDAxMDc2Il0sImFwcF9pZCI6NTE3NTMsInVzZXJfaWQiOjIyNDc3NjUyNjg5NjMwMDEwNzZ9.OHYX-hdbvfZhtKeTD9-lTZFhe6XAc38a8Dpea4N0tnQ; first_page=https://moskva.brusnika.ru/; scbsid_old=4097698043; adrdel=1781787363873; adrdel=1781787363873; acs_3=%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1781873763884%2C%22sl%22%3A%7B%22224%22%3A1781787363884%2C%221228%22%3A1781787363884%7D%7D; acs_3=%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1781873763884%2C%22sl%22%3A%7B%22224%22%3A1781787363884%2C%221228%22%3A1781787363884%7D%7D; _cmg_csstPowxG=1781787364; _comagic_idPowxG=13442635939.17918895329.1781787361; _ym_visorc=w; domain_sid=bcpIyyNCjvwJccKhz9O9z%3A1781787365316; sma_session_id=2741306055; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D; SCBstart=1781787366246; SCBFormsAlreadyPulled=true; undefined=6.179; carrotquest_session=eh0o2hjy155s235zjdqqxgj8swqirv4a; carrotquest_session_started=1; pageviewCount=2; tmr_detect=0%7C1781787375173; sma_index_activity=1594; SCBindexAct=1194',
}

params = {
    'offset': '0',
    'limit': '1000',
    'view': 'buy',
    'rent_active': 'false',
}

response = requests.get('https://moskva.brusnika.ru/api/office_filter/offices/', params=params, cookies=cookies, headers=headers)
print(response.status_code)
items = response.json()["results"]
print(items)
flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

for i in items:


    url = i["page_url"]

    date = datetime.date.today()
    project = i["complex_name"]
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
    developer = "Брусника"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    if i["building_name"] == "Тихий дом":
        korpus = "Тихий дом"
    else:
        korpus = extract_digits_or_original(i["building_name"])
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = i['delivery_title'].replace('Срок сдачи: ', '').replace('квартал', 'кв')
    stadia = ''
    dogovor = ''
    try:
        type = i['commerce_purpose'][0]['name']
    except:
        type = ''
    finish_type = ''
    room_count = ''
    area = float(i["square"].replace(',', '.'))
    price_per_metr = ''
    old_price = int(str(i["price"]).replace('.00', ''))
    discount = ''
    price_per_metr_new = ''
    price = old_price
    section = ''
    floor = i["floor_number"]
    flat_number = ''


    print(
        f"{project}, {url}, дата: {date}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}, срок сдачи: {srok_sdachi_old}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]





    flats.append(result)

save_flats_to_excel(flats, project, developer)

