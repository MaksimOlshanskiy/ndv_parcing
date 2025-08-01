import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'm108_session_id': 'm1ga085983630507831830000',
    'm108_client_id': '5857028461852284000',
    'scbsid_old': '2746015342',
    '_ym_uid': '1743152808957171634',
    '_ym_d': '1743152808',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_gcl_au': '1.1.2057046286.1743152809',
    '_cmg_csstQOizX': '1743152809',
    '_comagic_idQOizX': '9229931912.13169841982.1743152808',
    'tmr_lvid': '75d657731a575311f0ee7e592ea6eb30',
    'tmr_lvidTS': '1743152809450',
    '_gid': 'GA1.2.1592557004.1743152810',
    'domain_sid': 'oyjzwFJFxQw2pMxQCpO1V%3A1743152811322',
    'sma_session_id': '2240708400',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    'cookie-accepted': 'yes',
    'activity': '2|-1',
    'SCBporogAct': '5000',
    'XSRF-TOKEN': 'eyJpdiI6ImlWa20wWGd3N0ZXdHY0VmJvUXhUY2c9PSIsInZhbHVlIjoiYXlMWHlWU3NpTDEwRnZyNExlL09SUVk1Uy81UWVpU042QTREb2c3UVBLRGsybEh1b1pvUmFGdVY5VytPTXhCU29LNmN1cUNkTFNmOGswTlI3WmRxdVhmc2JIV3lhSEhWZFIzZU5rQjJud0dyQm5rR0hvMmZoVGZpSEtQQ2IzRjciLCJtYWMiOiI3MTRhMjI4Yjg2NGIyYTM0Yjc4MWIyZGFiMzU3ZjAyOGM1YTIyYTU4OGM4NjQ0ZjBhOWE4ZDE0YjNlZDBlY2M1IiwidGFnIjoiIn0%3D',
    'primavera_session': 'eyJpdiI6ImNoRUI2T3hXVFdpOEg5aVMvTWVYU3c9PSIsInZhbHVlIjoiWjMyTGpNbC9OcnBRMWRBRVFvK3FYRWduZEtxQ0RTZHZOVy8ydlFySXlvVmtadDRrVlE0SFV4WDU2UGF2Ny9sa1B5VHVFWHJKNFp1bTVHZUpkMzdtY3RCbU5LR3BsdTNMOGV1SjR5U3greXprUmdWOUtsQU51VTRSaUNOR1duZVIiLCJtYWMiOiJlYTc3MTE0YjFjODk4NDQwYzc5ZmYwYWU3M2I5YWJlMmRlOTNkOTY0ZGQwMzg0NzYwYWI1ZjBjNmEwY2QxYzZjIiwidGFnIjoiIn0%3D',
    '_gat_primavera': '1',
    '_ga': 'GA1.1.115922388.1743152809',
    '_ga_77QPZKQE57': 'GS1.1.1743152809.1.1.1743154754.60.0.0',
    'SCBstart': '1743154755189',
    'SCBFormsAlreadyPulled': 'true',
    'tmr_detect': '0%7C1743154756409',
    'SCBindexAct': '2752',
    'sma_index_activity': '10677',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://primavera.moscow',
    'priority': 'u=1, i',
    'referer': 'https://primavera.moscow/search',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'eyJpdiI6ImlWa20wWGd3N0ZXdHY0VmJvUXhUY2c9PSIsInZhbHVlIjoiYXlMWHlWU3NpTDEwRnZyNExlL09SUVk1Uy81UWVpU042QTREb2c3UVBLRGsybEh1b1pvUmFGdVY5VytPTXhCU29LNmN1cUNkTFNmOGswTlI3WmRxdVhmc2JIV3lhSEhWZFIzZU5rQjJud0dyQm5rR0hvMmZoVGZpSEtQQ2IzRjciLCJtYWMiOiI3MTRhMjI4Yjg2NGIyYTM0Yjc4MWIyZGFiMzU3ZjAyOGM1YTIyYTU4OGM4NjQ0ZjBhOWE4ZDE0YjNlZDBlY2M1IiwidGFnIjoiIn0=',
    # 'cookie': 'm108_session_id=m1ga085983630507831830000; m108_client_id=5857028461852284000; scbsid_old=2746015342; _ym_uid=1743152808957171634; _ym_d=1743152808; _ym_isad=2; _ym_visorc=w; _gcl_au=1.1.2057046286.1743152809; _cmg_csstQOizX=1743152809; _comagic_idQOizX=9229931912.13169841982.1743152808; tmr_lvid=75d657731a575311f0ee7e592ea6eb30; tmr_lvidTS=1743152809450; _gid=GA1.2.1592557004.1743152810; domain_sid=oyjzwFJFxQw2pMxQCpO1V%3A1743152811322; sma_session_id=2240708400; SCBnotShow=-1; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; cookie-accepted=yes; activity=2|-1; SCBporogAct=5000; XSRF-TOKEN=eyJpdiI6ImlWa20wWGd3N0ZXdHY0VmJvUXhUY2c9PSIsInZhbHVlIjoiYXlMWHlWU3NpTDEwRnZyNExlL09SUVk1Uy81UWVpU042QTREb2c3UVBLRGsybEh1b1pvUmFGdVY5VytPTXhCU29LNmN1cUNkTFNmOGswTlI3WmRxdVhmc2JIV3lhSEhWZFIzZU5rQjJud0dyQm5rR0hvMmZoVGZpSEtQQ2IzRjciLCJtYWMiOiI3MTRhMjI4Yjg2NGIyYTM0Yjc4MWIyZGFiMzU3ZjAyOGM1YTIyYTU4OGM4NjQ0ZjBhOWE4ZDE0YjNlZDBlY2M1IiwidGFnIjoiIn0%3D; primavera_session=eyJpdiI6ImNoRUI2T3hXVFdpOEg5aVMvTWVYU3c9PSIsInZhbHVlIjoiWjMyTGpNbC9OcnBRMWRBRVFvK3FYRWduZEtxQ0RTZHZOVy8ydlFySXlvVmtadDRrVlE0SFV4WDU2UGF2Ny9sa1B5VHVFWHJKNFp1bTVHZUpkMzdtY3RCbU5LR3BsdTNMOGV1SjR5U3greXprUmdWOUtsQU51VTRSaUNOR1duZVIiLCJtYWMiOiJlYTc3MTE0YjFjODk4NDQwYzc5ZmYwYWU3M2I5YWJlMmRlOTNkOTY0ZGQwMzg0NzYwYWI1ZjBjNmEwY2QxYzZjIiwidGFnIjoiIn0%3D; _gat_primavera=1; _ga=GA1.1.115922388.1743152809; _ga_77QPZKQE57=GS1.1.1743152809.1.1.1743154754.60.0.0; SCBstart=1743154755189; SCBFormsAlreadyPulled=true; tmr_detect=0%7C1743154756409; SCBindexAct=2752; sma_index_activity=10677',
}

data = {
    'sort': 'area-desc',
    'request_type': 'more',
    'shown': '0',
    'ts': 'eyJpdiI6IktOajZmU2tEZlVTdW1SODVCVEhFV2c9PSIsInZhbHVlIjoiZU9NMWowc1FJa2F5bkFkdUNJWnJEZz09IiwibWFjIjoiOTJkMDlkYmU0YTg5M2E0OGFhZDQwNjFjNDJiYzhkNTQ5MTFkNjgyZWVmZDdmNDBmM2YwZWQzMTE3Y2JjNzEyMiIsInRhZyI6IiJ9',
    'st': 'eyJpdiI6IlFxL05Na3ZLWnYxMGowR2dCaEF0bXc9PSIsInZhbHVlIjoieWExOTZEZlJCR1dBa2swbW5Mc0VKdz09IiwibWFjIjoiMTI4Y2NiYzBlMTI5ZGEzMjllZDExYzJmOTkzMTI5ODg0NDg5MTEwNmRiZWNhOGMyMzJkZjA2ZDdhZGFiZTI1NSIsInRhZyI6IiJ9',
}





flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://primavera.moscow/api/estate-search/results', cookies=cookies, headers=headers, json=data)
    print(response.status_code)

    items = response.json()['data']['flats']


    for i in items:

        url = ''
        developer = "Стадион Спартак"
        project = 'Примавера'
        korpus = extract_digits_or_original(i['building'])
        type = 'Квартиры'
        finish_type = 'Без отделки'
        room_count = extract_digits_or_original(i['title'].split()[0])
        try:
            area = float(i['area'].replace(',', '.'))
        except:
            area = ''
        try:
            old_price = int(i['price']['current'].replace(' ', ''))
        except:
            old_price = ''
        try:
            price = ''
        except:
            price = ''
        section = ''
        try:
            floor = int(i['floor'].split()[1])
        except:
            floor = ''
        flat_number = ''

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
        adress = i['quarter']
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

    if not items:
        break
    data['shown'] = str(int(data['shown']) + 6)
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

