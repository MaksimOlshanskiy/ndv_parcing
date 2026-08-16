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
    'i18n_redirected': 'ru',
    '_ym_uid': '1779458396475689548',
    '_ym_d': '1782981733',
    'ab-minimalist-filter-card': 'true',
    'mindboxDeviceUUID': 'd6b3597d-4b0b-4e45-8167-0b84971b36f7',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D',
    'tmr_lvid': 'e7dd4b124d1ba33e641356f49c4cc976',
    'tmr_lvidTS': '1779458402037',
    '_cmg_csstvg3wT': '1782981744',
    '_comagic_idvg3wT': '13514801524.18000186764.1782981742',
    'booking-blocking': '%22false%22',
    'qrator_msid2': 'v2.0.1784058663.181.05e47254JInCSTCm|Sq0JnSIcL1VfIdSt|+aM7oBAnajGc7zkqcizL8c7i1tdlpoZlBBRj0KE8g/yVhBiRKc+O9KXkmGqHZ+K5BgVx8qwXOUMGZCA17q8/vQ==-zECyz13DolfKMeWu1kch2elKWZE=',
    'ya_visit_init': '%221784058666342%22',
    'ya_visit_total': '%221%22',
    'ya_visit_total_session': '%221%22',
    'pageCount': '%221%22',
    'ya_visit_page': '%2F',
    'adriver_visit_one_pages_finished': 'done',
    'menu': '%7B%22isFavorite%22%3Afalse%7D',
    'carrotquest_device_guid': 'af3654e1-f4ed-4240-8436-74395aca4e83',
    'carrotquest_uid': '2281287546438681064',
    'carrotquest_auth_token': 'user.2281287546438681064.50549-b9906febe2aaab4d349cf1594e.d80a2d77680c90b6bc4880af1f95b97a25e5418ea4476fea',
    'carrotquest_jwt_access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3ODQwNjIyNjcsImlhdCI6MTc4NDA1ODY2NywianRpIjoiNTk1NWM3ZTY3ODQ3NDNiZDgxZTdiZWM3ZDk4Y2UyZTUiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDo1MDU0OS4kdXNlcl9pZDoyMjgxMjg3NTQ2NDM4NjgxMDY0Il0sImFwcF9pZCI6NTA1NDksInVzZXJfaWQiOjIyODEyODc1NDY0Mzg2ODEwNjR9.9jPbCQHY-FctTjef_EVZtTU8qEw4qwcKglmjYRZsXns',
    'carrotquest_realtime_services_transport': 'wss',
    'user_confirmed_city': 'moscow',
    'carrotquest_session': '0w60xnmig2yzdogmmdz3jwqku88adydy',
    'carrotquest_session_started': '1',
    'csrftoken': 'tOs37gTMSI5Al9tNn9iVK3BopoFqvQEc',
    'activity': '4|10',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru',
    'baggage': 'sentry-environment=production,sentry-public_key=d431fc4e116909199fba6f7f1ecd0f0a,sentry-trace_id=8762ab757904479e9bf6bb84eeef4793',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'qrator-timestamp': '2026-07-14T19:52:24.479Z',
    'qrator-token': '96cebb4f05d3248ce47510a4abe46b3a',
    'qrator-version': '1.0',
    'referer': 'https://level.ru/',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '8762ab757904479e9bf6bb84eeef4793-84326b3c5a65f64a',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    'x-csrftoken': 'tOs37gTMSI5Al9tNn9iVK3BopoFqvQEc',
    # 'cookie': 'i18n_redirected=ru; _ym_uid=1779458396475689548; _ym_d=1782981733; ab-minimalist-filter-card=true; mindboxDeviceUUID=d6b3597d-4b0b-4e45-8167-0b84971b36f7; directCrm-session=%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D; tmr_lvid=e7dd4b124d1ba33e641356f49c4cc976; tmr_lvidTS=1779458402037; _cmg_csstvg3wT=1782981744; _comagic_idvg3wT=13514801524.18000186764.1782981742; booking-blocking=%22false%22; qrator_msid2=v2.0.1784058663.181.05e47254JInCSTCm|Sq0JnSIcL1VfIdSt|+aM7oBAnajGc7zkqcizL8c7i1tdlpoZlBBRj0KE8g/yVhBiRKc+O9KXkmGqHZ+K5BgVx8qwXOUMGZCA17q8/vQ==-zECyz13DolfKMeWu1kch2elKWZE=; ya_visit_init=%221784058666342%22; ya_visit_total=%221%22; ya_visit_total_session=%221%22; pageCount=%221%22; ya_visit_page=%2F; adriver_visit_one_pages_finished=done; menu=%7B%22isFavorite%22%3Afalse%7D; carrotquest_device_guid=af3654e1-f4ed-4240-8436-74395aca4e83; carrotquest_uid=2281287546438681064; carrotquest_auth_token=user.2281287546438681064.50549-b9906febe2aaab4d349cf1594e.d80a2d77680c90b6bc4880af1f95b97a25e5418ea4476fea; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3ODQwNjIyNjcsImlhdCI6MTc4NDA1ODY2NywianRpIjoiNTk1NWM3ZTY3ODQ3NDNiZDgxZTdiZWM3ZDk4Y2UyZTUiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDo1MDU0OS4kdXNlcl9pZDoyMjgxMjg3NTQ2NDM4NjgxMDY0Il0sImFwcF9pZCI6NTA1NDksInVzZXJfaWQiOjIyODEyODc1NDY0Mzg2ODEwNjR9.9jPbCQHY-FctTjef_EVZtTU8qEw4qwcKglmjYRZsXns; carrotquest_realtime_services_transport=wss; user_confirmed_city=moscow; carrotquest_session=0w60xnmig2yzdogmmdz3jwqku88adydy; carrotquest_session_started=1; csrftoken=tOs37gTMSI5Al9tNn9iVK3BopoFqvQEc; activity=4|10',
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
        if 'work' in project:
            continue
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
        srok_sdachi_old = f'{i['completion_quarter']} кв {i['completion_year']}'
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

