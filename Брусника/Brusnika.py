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
    '_ym_d': '1785140258',
    '_ym_isad': '2',
    'mindboxDeviceUUID': 'd6b3597d-4b0b-4e45-8167-0b84971b36f7',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D',
    'carrotquest_device_guid': 'aba29952-d58b-4a41-86da-250fca3f71e3',
    'carrotquest_uid': '2290360578499150600',
    'carrotquest_auth_token': 'user.2290360578499150600.51753-776395ac10b7ee9e1ccd2b8213.e39e17bb48f791f34f6344da33adfd1e3459eafecf2b8023',
    '__eventn_id': '41e40cdd-3656-47c1-be5c-eb1c5942390e',
    'carrotquest_jwt_access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3ODUxNDM4NTcsImlhdCI6MTc4NTE0MDI1NywianRpIjoiMGQ3NWQ4OWMxNWVlNGJkNjliNjBlMTYwOGQ0NmE3MGMiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDo1MTc1My4kdXNlcl9pZDoyMjkwMzYwNTc4NDk5MTUwNjAwIl0sImFwcF9pZCI6NTE3NTMsInVzZXJfaWQiOjIyOTAzNjA1Nzg0OTkxNTA2MDB9.zWbQHv-YHF5rU2HdMUvj9IlAqV4tJyKyXbSYf-jv9vA',
    'carrotquest_realtime_services_transport': 'wss',
    '_gcl_au': '1.1.2040997119.1785140258',
    'first_page': 'https://moskva.brusnika.ru/',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '_cmg_csstPowxG': '1785140258',
    '_comagic_idPowxG': '13643815759.18144340269.1785140257',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'acs_3': '%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1785226658064%2C%22sl%22%3A%7B%22224%22%3A1785140258064%2C%221228%22%3A1785140258064%7D%7D',
    'acs_3': '%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1785226658064%2C%22sl%22%3A%7B%22224%22%3A1785140258064%2C%221228%22%3A1785140258064%7D%7D',
    'tmr_lvid': '5a177ccfb44c98e090dccda7d3650dd8',
    'tmr_lvidTS': '1780062503153',
    'adrdel': '1785140258137',
    'adrdel': '1785140258137',
    'scbsid_old': '16031261345',
    '_ym_visorc': 'b',
    'domain_sid': 'bcpIyyNCjvwJccKhz9O9z%3A1785140258405',
    'sma_session_id': '2786791349',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'smFpId_old_values': '%5B%221760a41b46d1a0c018f5c6bd064f5ef3%22%5D',
    'SCBnotShow': '-1',
    'SCBstart': '1785140258769',
    'SCBporogAct': '5000',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'undefined': '2.239',
    'SCBindexAct': '618',
    'csrftoken': 'LDdKIc8hvCl248baFd56Db578a781iCc',
    'pageviewCount': '2',
    'sessionid': 'hn827gkk3gzw0xa2bynitp4jrmaqimk0',
    'carrotquest_session': '8ey1v2h3qjuzdnvzi26kgzgsybzg78c1',
    'carrotquest_session_started': '1',
    'tmr_detect': '0%7C1785140265507',
    'sma_index_activity': '1781',
    'SCBindexAct': '1280',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://moskva.brusnika.ru/flat/',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1780062499353899720; _ym_d=1785140258; _ym_isad=2; mindboxDeviceUUID=d6b3597d-4b0b-4e45-8167-0b84971b36f7; directCrm-session=%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D; carrotquest_device_guid=aba29952-d58b-4a41-86da-250fca3f71e3; carrotquest_uid=2290360578499150600; carrotquest_auth_token=user.2290360578499150600.51753-776395ac10b7ee9e1ccd2b8213.e39e17bb48f791f34f6344da33adfd1e3459eafecf2b8023; __eventn_id=41e40cdd-3656-47c1-be5c-eb1c5942390e; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3ODUxNDM4NTcsImlhdCI6MTc4NTE0MDI1NywianRpIjoiMGQ3NWQ4OWMxNWVlNGJkNjliNjBlMTYwOGQ0NmE3MGMiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDo1MTc1My4kdXNlcl9pZDoyMjkwMzYwNTc4NDk5MTUwNjAwIl0sImFwcF9pZCI6NTE3NTMsInVzZXJfaWQiOjIyOTAzNjA1Nzg0OTkxNTA2MDB9.zWbQHv-YHF5rU2HdMUvj9IlAqV4tJyKyXbSYf-jv9vA; carrotquest_realtime_services_transport=wss; _gcl_au=1.1.2040997119.1785140258; first_page=https://moskva.brusnika.ru/; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _cmg_csstPowxG=1785140258; _comagic_idPowxG=13643815759.18144340269.1785140257; adrcid=A0r9KB4fc8duMUv2jPsp-tg; adrcid=A0r9KB4fc8duMUv2jPsp-tg; acs_3=%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1785226658064%2C%22sl%22%3A%7B%22224%22%3A1785140258064%2C%221228%22%3A1785140258064%7D%7D; acs_3=%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1785226658064%2C%22sl%22%3A%7B%22224%22%3A1785140258064%2C%221228%22%3A1785140258064%7D%7D; tmr_lvid=5a177ccfb44c98e090dccda7d3650dd8; tmr_lvidTS=1780062503153; adrdel=1785140258137; adrdel=1785140258137; scbsid_old=16031261345; _ym_visorc=b; domain_sid=bcpIyyNCjvwJccKhz9O9z%3A1785140258405; sma_session_id=2786791349; SCBfrom=https%3A%2F%2Fwww.google.com%2F; smFpId_old_values=%5B%221760a41b46d1a0c018f5c6bd064f5ef3%22%5D; SCBnotShow=-1; SCBstart=1785140258769; SCBporogAct=5000; SCBFormsAlreadyPulled=true; sma_postview_ready=1; undefined=2.239; SCBindexAct=618; csrftoken=LDdKIc8hvCl248baFd56Db578a781iCc; pageviewCount=2; sessionid=hn827gkk3gzw0xa2bynitp4jrmaqimk0; carrotquest_session=8ey1v2h3qjuzdnvzi26kgzgsybzg78c1; carrotquest_session_started=1; tmr_detect=0%7C1785140265507; sma_index_activity=1781; SCBindexAct=1280',
}

params = {
    'offset': '0',
    'ordering': 'price_order',
    'limit': '3200',
    'active_banner': 'true',
    'active_big_card': 'true',
    'is_group': '0',
    'is_booked': 'false',
}

response = requests.get('https://moskva.brusnika.ru/api/filter/flats/', params=params, cookies=cookies, headers=headers)

items = response.json()["results"]
flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

for i in items:
    if 'id' in i:  # Убираем рекламную строку, т.к. в квартирах нет ключа id
        continue

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
    type = 'Квартиры'
    for tag in i["tags"]:
        if "отделк" in tag:
            finish_type = tag.replace(' отделка', '')
    room_count = int(i["rooms"])
    area = float(i["square"])
    price_per_metr = ''
    old_price = int(str(i["price_old"]).replace('.00', ''))
    if old_price == 0:
        old_price = int(str(i["price_package_without_promo"]).replace('.00', '').replace('.0', ''))
    discount = ''
    price_per_metr_new = ''
    price = int(str(i["price_marketing"]).replace('.00', ''))
    if i["section_number"] == "Тихий дом":
        section = "Тихий дом"
    else:
        section = extract_digits_or_original(i["section_number"])
    floor = i["floor"]
    flat_number = ''


    print(
        f"{project}, {url}, дата: {date}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}, срок сдачи: {srok_sdachi_old}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]





    flats.append(result)

save_flats_to_excel(flats, project, developer)

