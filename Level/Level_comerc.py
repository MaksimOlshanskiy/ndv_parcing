# запрос filter...

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1741763438149410509',
    '_ym_d': '1755777460',
    'tmr_lvid': 'a5ef860db478f984f83e34d01161b4e1',
    'tmr_lvidTS': '1741763429108',
    'carrotquest_device_guid': '55c58d99-5baf-4909-8267-cb2a7314cdd5',
    'carrotquest_uid': '2044047630501150814',
    'carrotquest_auth_token': 'user.2044047630501150814.50549-b9906febe2aaab4d349cf1594e.e7b8bb70301b5e6753e43dcfa55919ea573f99afd350ef67',
    '_cmg_csstvg3wT': '1756121303',
    '_comagic_idvg3wT': '11580697199.15829139924.1756121303',
    'i18n_redirected': 'ru',
    'qrator_msid2': 'v2.0.1757581067.795.5b6ce31fVZpIhrCJ|tIqJydO4Rf0jSxrV|VHTIB4yY4I3eOndjp/WN7naFf5rEbBiwf47p9gMh0Sak7fs+d7rnM5P9wpqP3pui5DV3PgP8moI0K0NVC8P7pg==-JoMkkx/MherN4vO5U2LPQDqArqI=',
    '_ym_isad': '2',
    'adrdel': '1757581072098',
    'adrdel': '1757581072098',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1757667472104%2C%22sl%22%3A%7B%22224%22%3A1757581072104%2C%221228%22%3A1757581072104%7D%7D',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1757667472104%2C%22sl%22%3A%7B%22224%22%3A1757581072104%2C%221228%22%3A1757581072104%7D%7D',
    '_ym_visorc': 'w',
    'ya_visit_init': '1757581073046',
    'csrftoken': 'gTgEQZFMXt35AE0lmrA8N3BSaPAr0fJ9',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    '_cmg_csst4kyh5': '1757581076',
    '_comagic_id4kyh5': '11692775424.15955361399.1757581076',
    'carrotquest_session': '6cxama6q37r13st48dpciusr6xspzjzt',
    'domain_sid': 'jJ8K2WiKz1cnM9YoVV_lj%3A1757581077360',
    'carrotquest_session_started': '1',
    'carrotquest_realtime_services_transport': 'wss',
    'tmr_detect': '0%7C1757581077706',
    'carrotquest_jwt_access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NTc1ODQ2NzcsImlhdCI6MTc1NzU4MTA3NywianRpIjoiMDA5MWU3Mzc3MGFmNGRiN2ExMjJlYjUwNTc1MDU5Y2IiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDo1MDU0OS4kdXNlcl9pZDoyMDQ0MDQ3NjMwNTAxMTUwODE0Il0sImFwcF9pZCI6NTA1NDksInVzZXJfaWQiOjIwNDQwNDc2MzA1MDExNTA4MTR9.9tSaVTtsEYFd1pbUSgT4lc4wP-yjPO14dK9752l9gbE',
    'ya_visit_two_pages_finished': 'done',
    'ya_visit_total': '3',
    'ya_visit_total_session': '3',
    'ya_visit_page': '%2Ffilter%2Fkommercheskie-pomeshcheniya-v-prodazhe%2F',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'qrator-timestamp': '2025-09-11T08:58:49.286Z',
    'qrator-token': '6f7fe882a58e789dc1e194301388fc0f',
    'qrator-version': '1.0',
    'referer': 'https://business.level.ru/filter/kommercheskie-pomeshcheniya-v-prodazhe/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'x-csrftoken': 'gTgEQZFMXt35AE0lmrA8N3BSaPAr0fJ9',
    'x-forwarded-host': '',
    # 'cookie': '_ym_uid=1741763438149410509; _ym_d=1755777460; tmr_lvid=a5ef860db478f984f83e34d01161b4e1; tmr_lvidTS=1741763429108; carrotquest_device_guid=55c58d99-5baf-4909-8267-cb2a7314cdd5; carrotquest_uid=2044047630501150814; carrotquest_auth_token=user.2044047630501150814.50549-b9906febe2aaab4d349cf1594e.e7b8bb70301b5e6753e43dcfa55919ea573f99afd350ef67; _cmg_csstvg3wT=1756121303; _comagic_idvg3wT=11580697199.15829139924.1756121303; i18n_redirected=ru; qrator_msid2=v2.0.1757581067.795.5b6ce31fVZpIhrCJ|tIqJydO4Rf0jSxrV|VHTIB4yY4I3eOndjp/WN7naFf5rEbBiwf47p9gMh0Sak7fs+d7rnM5P9wpqP3pui5DV3PgP8moI0K0NVC8P7pg==-JoMkkx/MherN4vO5U2LPQDqArqI=; _ym_isad=2; adrdel=1757581072098; adrdel=1757581072098; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1757667472104%2C%22sl%22%3A%7B%22224%22%3A1757581072104%2C%221228%22%3A1757581072104%7D%7D; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1757667472104%2C%22sl%22%3A%7B%22224%22%3A1757581072104%2C%221228%22%3A1757581072104%7D%7D; _ym_visorc=w; ya_visit_init=1757581073046; csrftoken=gTgEQZFMXt35AE0lmrA8N3BSaPAr0fJ9; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; _cmg_csst4kyh5=1757581076; _comagic_id4kyh5=11692775424.15955361399.1757581076; carrotquest_session=6cxama6q37r13st48dpciusr6xspzjzt; domain_sid=jJ8K2WiKz1cnM9YoVV_lj%3A1757581077360; carrotquest_session_started=1; carrotquest_realtime_services_transport=wss; tmr_detect=0%7C1757581077706; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NTc1ODQ2NzcsImlhdCI6MTc1NzU4MTA3NywianRpIjoiMDA5MWU3Mzc3MGFmNGRiN2ExMjJlYjUwNTc1MDU5Y2IiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDo1MDU0OS4kdXNlcl9pZDoyMDQ0MDQ3NjMwNTAxMTUwODE0Il0sImFwcF9pZCI6NTA1NDksInVzZXJfaWQiOjIwNDQwNDc2MzA1MDExNTA4MTR9.9tSaVTtsEYFd1pbUSgT4lc4wP-yjPO14dK9752l9gbE; ya_visit_two_pages_finished=done; ya_visit_total=3; ya_visit_total_session=3; ya_visit_page=%2Ffilter%2Fkommercheskie-pomeshcheniya-v-prodazhe%2F',
}


params = {
    'type_of_advertisement': '0',
    'limit': '1000',
    'offset': '0',
}


flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://business.level.ru/api/filter/', params=params, cookies=cookies, headers=headers)
    items = response.json()["results"]

    for i in items:

        url = ''
        date = datetime.date.today()
        project = i["project"]
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
        developer = "Level"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = str(i["building_name"]).replace('Корпус ', '')
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        finish_type = i['renovation']
        room_count = ''
        area = float(i["area"])
        price_per_metr = ''
        old_price = int(i["old_price"])
        discount = ''
        price_per_metr_new = ''
        price = int(i["price"])
        section = ''
        floor = int(i["floor"])
        flat_number = ''

        print(
            f"{project}, {url}, дата: {date}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["offset"] = str(int(params["offset"]) + 1000)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break

save_flats_to_excel(flats, project, developer)

