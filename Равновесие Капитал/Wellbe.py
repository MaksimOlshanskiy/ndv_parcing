import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'tmr_lvid': 'fdd15cc1a1dc877c59d4a449be1190ac',
    'tmr_lvidTS': '1751028012074',
    '_ga': 'GA1.1.1453494377.1751028013',
    'domain_sid': 'z9Xc9LzD4T3rx2GHzc9fj%3A1751028013304',
    '_ym_uid': '175102801477698215',
    '_ym_d': '1751028014',
    '_ym_isad': '2',
    'cted': 'modId%3Dpvofli05%3Bclient_id%3D1453494377.1751028013%3Bya_client_id%3D175102801477698215',
    '_ct_ids': 'pvofli05%3A56541%3A469495829',
    '_ct_session_id': '469495829',
    '_ct_site_id': '56541',
    '_ct': '2300000000307834692',
    '_ym_visorc': 'w',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'tmr_detect': '0%7C1751028063674',
    'XSRF-TOKEN': 'eyJpdiI6Ii9zT04xUkhEWWlVMzc1T0RMSHdoVlE9PSIsInZhbHVlIjoiT0JpMG01Uyt4WXkrN1NDb256QkJONW55d2Y1a0R2a2lmWUkzK2J1bjBsOUtXVzlZNG8wN3hVcjJIRGhXVEpnSUN6dHlFR3c3b3djazR2bVRvZUkreTZVSXJHSjhEMUJUOHVYQ3d3Y01LTWpyYldMUmFNdmdtSlRoL3JVM1NnMm4iLCJtYWMiOiJhYTQyYWQ5NWM4YmY0Y2JhOGQ5NTVhZTNhMjZkNmI2ZDMyMjZjZDM2MjI4OThiZWVmZDExOTBiNzM1YjU5NzQ3IiwidGFnIjoiIn0%3D',
    'wellbe_apartments_session': 'eyJpdiI6IlNGTWJkUm1lVWJLZGRqbjU5aUdmZnc9PSIsInZhbHVlIjoiRGVuUkFKUTNUV2RKME9oUnB2cnhEQzJidC9lMFJSSFhmYWtidmt4U1BnUFVKL2RMaWduUjFzUDJ5WG1sdlM4bFB3c2tXMjBMM1FGajBYcTFHclFiZHVDSFQvYzdMd241N2tFZ2swcEorVnA0RFZMRnNTOEFNZEQ0SHYyNFRWa08iLCJtYWMiOiI3Y2E4ZWQyMGRhYWE5MGVmZmVmYjdmNmM2ZjVkOWNiNGM4NzNiZGE2N2E1YmI5ZjA2NTg0MzU3NWE5Zjc3NjdjIiwidGFnIjoiIn0%3D',
    '_ga_F0B2CVBRCB': 'GS2.1.s1751028012$o1$g1$t1751028095$j37$l0$h0',
    'call_s': '___pvofli05.1751029896.469495829.293142:860559.293144:857743|2___',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    # 'content-length': '0',
    'origin': 'https://wellbe.apartments',
    'priority': 'u=1, i',
    'referer': 'https://wellbe.apartments/pomeshcheniya?group_type%5B0%5D=1&group_type%5B1%5D=2&group_type%5B2%5D=3&group_type%5B3%5D=4&page=3',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-xsrf-token': 'eyJpdiI6Ii9zT04xUkhEWWlVMzc1T0RMSHdoVlE9PSIsInZhbHVlIjoiT0JpMG01Uyt4WXkrN1NDb256QkJONW55d2Y1a0R2a2lmWUkzK2J1bjBsOUtXVzlZNG8wN3hVcjJIRGhXVEpnSUN6dHlFR3c3b3djazR2bVRvZUkreTZVSXJHSjhEMUJUOHVYQ3d3Y01LTWpyYldMUmFNdmdtSlRoL3JVM1NnMm4iLCJtYWMiOiJhYTQyYWQ5NWM4YmY0Y2JhOGQ5NTVhZTNhMjZkNmI2ZDMyMjZjZDM2MjI4OThiZWVmZDExOTBiNzM1YjU5NzQ3IiwidGFnIjoiIn0=',
    # 'cookie': 'tmr_lvid=fdd15cc1a1dc877c59d4a449be1190ac; tmr_lvidTS=1751028012074; _ga=GA1.1.1453494377.1751028013; domain_sid=z9Xc9LzD4T3rx2GHzc9fj%3A1751028013304; _ym_uid=175102801477698215; _ym_d=1751028014; _ym_isad=2; cted=modId%3Dpvofli05%3Bclient_id%3D1453494377.1751028013%3Bya_client_id%3D175102801477698215; _ct_ids=pvofli05%3A56541%3A469495829; _ct_session_id=469495829; _ct_site_id=56541; _ct=2300000000307834692; _ym_visorc=w; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; tmr_detect=0%7C1751028063674; XSRF-TOKEN=eyJpdiI6Ii9zT04xUkhEWWlVMzc1T0RMSHdoVlE9PSIsInZhbHVlIjoiT0JpMG01Uyt4WXkrN1NDb256QkJONW55d2Y1a0R2a2lmWUkzK2J1bjBsOUtXVzlZNG8wN3hVcjJIRGhXVEpnSUN6dHlFR3c3b3djazR2bVRvZUkreTZVSXJHSjhEMUJUOHVYQ3d3Y01LTWpyYldMUmFNdmdtSlRoL3JVM1NnMm4iLCJtYWMiOiJhYTQyYWQ5NWM4YmY0Y2JhOGQ5NTVhZTNhMjZkNmI2ZDMyMjZjZDM2MjI4OThiZWVmZDExOTBiNzM1YjU5NzQ3IiwidGFnIjoiIn0%3D; wellbe_apartments_session=eyJpdiI6IlNGTWJkUm1lVWJLZGRqbjU5aUdmZnc9PSIsInZhbHVlIjoiRGVuUkFKUTNUV2RKME9oUnB2cnhEQzJidC9lMFJSSFhmYWtidmt4U1BnUFVKL2RMaWduUjFzUDJ5WG1sdlM4bFB3c2tXMjBMM1FGajBYcTFHclFiZHVDSFQvYzdMd241N2tFZ2swcEorVnA0RFZMRnNTOEFNZEQ0SHYyNFRWa08iLCJtYWMiOiI3Y2E4ZWQyMGRhYWE5MGVmZmVmYjdmNmM2ZjVkOWNiNGM4NzNiZGE2N2E1YmI5ZjA2NTg0MzU3NWE5Zjc3NjdjIiwidGFnIjoiIn0%3D; _ga_F0B2CVBRCB=GS2.1.s1751028012$o1$g1$t1751028095$j37$l0$h0; call_s=___pvofli05.1751029896.469495829.293142:860559.293144:857743|2___',
}

params = {
    'group_type[0]': '1',
    'group_type[1]': '2',
    'group_type[2]': '3',
    'group_type[3]': '4',
    'page': '1',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://wellbe.apartments/api/v1/flats/kvartiry', params=params, cookies=cookies, headers=headers)
    items = response.json()['data']

    for i in items:

        url = i['link']
        developer = "Равновесие Капитал"
        project = i['resident_name']
        korpus = extract_digits_or_original(i['corpus_name'])
        section = ''
        type = 'Апартаменты'
        finish_type = 'С отделкой'
        room_count = i['flat_type']
        flat_number = i['number']
        try:
            area = float(i['area_total'])
        except:
            area = ''
        try:
            old_price = int(i['price'])
        except:
            old_price = ''
        try:
            price = ''
        except:
            price = ''
        try:
            floor = int(i['floor'])
        except:
            floor = ''


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
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''


        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params['page'] = str(int(params['page']) + 1)
    if not items:
        break
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

