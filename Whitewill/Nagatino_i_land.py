import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from functions import save_flats_to_excel
import requests

cookies = {
    '_ym_uid': '1746434561886246106',
    '_ym_d': '1756196428',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    '_ga': 'GA1.1.1380627496.1756196429',
    'roistat_visit': '16811387',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_is_need_listen_requests': '0',
    'roistat_is_save_data_in_cookie': '1',
    'roistat_phone': '%2B7%20(499)%20681-93-69',
    'roistat_raw_phone': '74996819369',
    'roistat_call_tracking': '1',
    'roistat_phone_replacement': 'null',
    'roistat_phone_script_data': '%5B%7B%22phone%22%3A%22%2B7%20(499)%20681-93-69%22%2C%22css_selectors%22%3A%5B%5D%2C%22replaceable_numbers%22%3A%5B%2274952550161%22%5D%2C%22raw_phone%22%3A%2274996819369%22%7D%5D',
    '___dc': 'b805bafa-905f-4fe7-921b-e5257de2dc92',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_phone%2Croistat_raw_phone%2Croistat_call_tracking%2Croistat_phone_replacement%2Croistat_phone_script_data%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    'client_code': '386194570',
    'popup-expert-closed': 'true',
    'XSRF-TOKEN': 'eyJpdiI6IkFQL0ppU01GYWtBTUVCNFVnUUt3aUE9PSIsInZhbHVlIjoiVG4vUnpEeVdDditpWCtzOG9xeWtQcDVQUG13SGlHcmQ3TmZHWlhPMkNpZGRKVnJIeXVFZEFVbXpPQVBnT1VVWHlmWlVob0dQY0ozTXZkSWZPaUJBU0orVlBoQ1lJV21pRDRVV0crSXlzNE5DMDd6REtXb014MjdNUDI3emJRSDkiLCJtYWMiOiI3N2U1ZDZlNmJiMTVlOGViOTE5OTY0NTM4NGZhOWUyYTI0NWQ3MDY4YjQ4MjcxOWRjMWEyZjRmYWEyMjY3ZjRiIiwidGFnIjoiIn0%3D',
    'whitewill_session': 'eyJpdiI6ImZ1UzFmcVM4THAzSThWQnhweDlnOWc9PSIsInZhbHVlIjoieGN1cnkxdW9wZWVqUTMwcmRFbk1FSW5DQ3cya3pla0JPYU9RZWU1bXlSNGlSYm1laWVzbTVlV1VSZ3dhSWdGOEZrRnhrcXMzdnpCTTJwaEYwdzZENnkvTHBxSWFQbUlzclpmbDNUUHFEcHRBcWJOMG9jazJPZDhVZXFMM2wrdlkiLCJtYWMiOiI2MDBmNTBjZmViMzM5NTU1NDBlNWQ4NWQ4OThkMWEyY2RmYWM2ZWIxMGZjYTgwZDRiNDA5ZjE1YjZhMTY5MzIxIiwidGFnIjoiIn0%3D',
    '_ga_39MXWD06ZJ': 'GS2.1.s1756196428$o1$g1$t1756196509$j52$l0$h1444058629',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://whitewill.ru/buy?filters=complex_id/int_multiple_filter|77',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '_ym_uid=1746434561886246106; _ym_d=1756196428; _ym_isad=2; _ym_visorc=w; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; _ga=GA1.1.1380627496.1756196429; roistat_visit=16811387; roistat_visit_cookie_expire=1209600; roistat_is_need_listen_requests=0; roistat_is_save_data_in_cookie=1; roistat_phone=%2B7%20(499)%20681-93-69; roistat_raw_phone=74996819369; roistat_call_tracking=1; roistat_phone_replacement=null; roistat_phone_script_data=%5B%7B%22phone%22%3A%22%2B7%20(499)%20681-93-69%22%2C%22css_selectors%22%3A%5B%5D%2C%22replaceable_numbers%22%3A%5B%2274952550161%22%5D%2C%22raw_phone%22%3A%2274996819369%22%7D%5D; ___dc=b805bafa-905f-4fe7-921b-e5257de2dc92; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=%5B%5D; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_phone%2Croistat_raw_phone%2Croistat_call_tracking%2Croistat_phone_replacement%2Croistat_phone_script_data%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails; client_code=386194570; popup-expert-closed=true; XSRF-TOKEN=eyJpdiI6IkFQL0ppU01GYWtBTUVCNFVnUUt3aUE9PSIsInZhbHVlIjoiVG4vUnpEeVdDditpWCtzOG9xeWtQcDVQUG13SGlHcmQ3TmZHWlhPMkNpZGRKVnJIeXVFZEFVbXpPQVBnT1VVWHlmWlVob0dQY0ozTXZkSWZPaUJBU0orVlBoQ1lJV21pRDRVV0crSXlzNE5DMDd6REtXb014MjdNUDI3emJRSDkiLCJtYWMiOiI3N2U1ZDZlNmJiMTVlOGViOTE5OTY0NTM4NGZhOWUyYTI0NWQ3MDY4YjQ4MjcxOWRjMWEyZjRmYWEyMjY3ZjRiIiwidGFnIjoiIn0%3D; whitewill_session=eyJpdiI6ImZ1UzFmcVM4THAzSThWQnhweDlnOWc9PSIsInZhbHVlIjoieGN1cnkxdW9wZWVqUTMwcmRFbk1FSW5DQ3cya3pla0JPYU9RZWU1bXlSNGlSYm1laWVzbTVlV1VSZ3dhSWdGOEZrRnhrcXMzdnpCTTJwaEYwdzZENnkvTHBxSWFQbUlzclpmbDNUUHFEcHRBcWJOMG9jazJPZDhVZXFMM2wrdlkiLCJtYWMiOiI2MDBmNTBjZmViMzM5NTU1NDBlNWQ4NWQ4OThkMWEyY2RmYWM2ZWIxMGZjYTgwZDRiNDA5ZjE1YjZhMTY5MzIxIiwidGFnIjoiIn0%3D; _ga_39MXWD06ZJ=GS2.1.s1756196428$o1$g1$t1756196509$j52$l0$h1444058629',
}

params = {
    'filters': 'complex_id/int_multiple_filter|77',
    'page': '1',
    'isMap': '0',
    'sort_direction': '',
    'sort_type': '',
}


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://whitewill.ru/filter/lots', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    items = response.json()['html']
    soup = BeautifulSoup(items, 'html.parser')
    flats_soup = soup.find_all('div', class_="card__content")
    for i in flats_soup:

        url = ''
        date = datetime.date.today()
        project = "Nagatino i-Land"
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
        developer = "Эталон"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = '1'
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        finish_type = 'Без отделки'
        room_count = ''
        area = int(i.find("div", {"data-test-group": "filter_result.card_areas"}).text.strip().replace(' м²', ''))
        price_per_metr = ''
        old_price = int(i.find("span", {"data-currency": "rub"}).text.strip().replace(' ', '').replace('₽', ''))
        discount = ''
        price_per_metr_new = ''
        price = ''
        section = ''
        floor = ''
        flat_number = ''

        print(
            f"{project}, квартира {flat_number}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not flats_soup:
        break

    print('--------------------------------------------------------------------------------')

    params['page'] = str(int(params['page']) + 1)
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)