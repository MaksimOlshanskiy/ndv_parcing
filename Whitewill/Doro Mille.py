import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    '_ym_uid': '1746434561886246106',
    '_ym_d': '1768486492',
    '_ga': 'GA1.1.1557249637.1768486493',
    '___dc': 'b805bafa-905f-4fe7-921b-e5257de2dc92',
    'client_code': '397554134',
    '_ym_isad': '2',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_call_tracking': '1',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    '_ga_39MXWD06ZJ': 'GS2.1.s1770966361$o3$g0$t1770966361$j60$l0$h1917287291',
    '_ym_visorc': 'w',
    'roistat_visit': '18892423',
    'roistat_marker': 'seo_yandex_search',
    'roistat_marker_old': 'seo_yandex_search',
    'roistat_phone_replacement': 'null',
    'roistat_phone_script_data': '%5B%7B%22phone%22%3A%22%2B7%20(499)%20111-59-68%22%2C%22css_selectors%22%3A%5B%5D%2C%22replaceable_numbers%22%3A%5B%2274952550161%22%5D%2C%22raw_phone%22%3A%2274991115968%22%7D%5D',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old%2Croistat_phone%2Croistat_raw_phone%2Croistat_call_tracking%2Croistat_phone_replacement%2Croistat_phone_script_data%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    'locale_popup': 'accepted',
    'XSRF-TOKEN': 'eyJpdiI6Ik9aR2Y0NDYwS3ZBdzhVU0xKaGV2Z1E9PSIsInZhbHVlIjoiclIyOVNLNXdRblJ4TWNWUzA1QlNkWjZWdmM1emQzMm8xTExjc2RsdGhxZEJKTGFNbkFMVFJhcE9hVnlHQ0lqMEwwTG03WElpZTJLTksyUk5zVHN5Nzl4KzZRNjhkNHBlZ05oWU9EMWxvcUV2NWs0NFNiQUpCSGZhYnYyMGxWU3oiLCJtYWMiOiIyNjE1NGQwOWM4Yjc5NWI5MjQ1ZDNjNDM4MmI5ZWJmZGMxYmY1YTMzNTgyY2E5OGI2OTUyMWFhMmQyODU0YzlmIiwidGFnIjoiIn0%3D',
    'whitewill_session': 'eyJpdiI6Im9GTkxXdGtnTnh3bUJuVy9FWmlUUFE9PSIsInZhbHVlIjoiOE5KQTNvSW9vNUtvcnBkNk16RGVSQUtwb1NRRHVIUFNIRWQrUWR3cUtidklCWGFhUjRXWUpKQkliRFA3VVRISDluRFVSd3BXUTZtcmFIZDJGd3YwWEFMbmw0aFBnTXVzTEp5N3hZN09Ud2gvSTBrYTBrYnpWTXNpa2dkUlVQRUMiLCJtYWMiOiIyNzcyYTExNzk3ZGY5ZmM4NmI4ZDY4NjdhMjQwMzA3OTVlZjZhZTU3NWUyMzgyM2UyOTQ4ODYxZTcxZjhiNDE1IiwidGFnIjoiIn0%3D',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://whitewill.ru/buy?filters=is_built/bool_filter|1;complex_id/int_multiple_filter|1028',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'x-xsrf-token': 'eyJpdiI6Ik9aR2Y0NDYwS3ZBdzhVU0xKaGV2Z1E9PSIsInZhbHVlIjoiclIyOVNLNXdRblJ4TWNWUzA1QlNkWjZWdmM1emQzMm8xTExjc2RsdGhxZEJKTGFNbkFMVFJhcE9hVnlHQ0lqMEwwTG03WElpZTJLTksyUk5zVHN5Nzl4KzZRNjhkNHBlZ05oWU9EMWxvcUV2NWs0NFNiQUpCSGZhYnYyMGxWU3oiLCJtYWMiOiIyNjE1NGQwOWM4Yjc5NWI5MjQ1ZDNjNDM4MmI5ZWJmZGMxYmY1YTMzNTgyY2E5OGI2OTUyMWFhMmQyODU0YzlmIiwidGFnIjoiIn0=',
    # 'cookie': '_ym_uid=1746434561886246106; _ym_d=1768486492; _ga=GA1.1.1557249637.1768486493; ___dc=b805bafa-905f-4fe7-921b-e5257de2dc92; client_code=397554134; _ym_isad=2; roistat_visit_cookie_expire=1209600; roistat_call_tracking=1; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=%5B%5D; _ga_39MXWD06ZJ=GS2.1.s1770966361$o3$g0$t1770966361$j60$l0$h1917287291; _ym_visorc=w; roistat_visit=18892423; roistat_marker=seo_yandex_search; roistat_marker_old=seo_yandex_search; roistat_phone_replacement=null; roistat_phone_script_data=%5B%7B%22phone%22%3A%22%2B7%20(499)%20111-59-68%22%2C%22css_selectors%22%3A%5B%5D%2C%22replaceable_numbers%22%3A%5B%2274952550161%22%5D%2C%22raw_phone%22%3A%2274991115968%22%7D%5D; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old%2Croistat_phone%2Croistat_raw_phone%2Croistat_call_tracking%2Croistat_phone_replacement%2Croistat_phone_script_data%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails; locale_popup=accepted; XSRF-TOKEN=eyJpdiI6Ik9aR2Y0NDYwS3ZBdzhVU0xKaGV2Z1E9PSIsInZhbHVlIjoiclIyOVNLNXdRblJ4TWNWUzA1QlNkWjZWdmM1emQzMm8xTExjc2RsdGhxZEJKTGFNbkFMVFJhcE9hVnlHQ0lqMEwwTG03WElpZTJLTksyUk5zVHN5Nzl4KzZRNjhkNHBlZ05oWU9EMWxvcUV2NWs0NFNiQUpCSGZhYnYyMGxWU3oiLCJtYWMiOiIyNjE1NGQwOWM4Yjc5NWI5MjQ1ZDNjNDM4MmI5ZWJmZGMxYmY1YTMzNTgyY2E5OGI2OTUyMWFhMmQyODU0YzlmIiwidGFnIjoiIn0%3D; whitewill_session=eyJpdiI6Im9GTkxXdGtnTnh3bUJuVy9FWmlUUFE9PSIsInZhbHVlIjoiOE5KQTNvSW9vNUtvcnBkNk16RGVSQUtwb1NRRHVIUFNIRWQrUWR3cUtidklCWGFhUjRXWUpKQkliRFA3VVRISDluRFVSd3BXUTZtcmFIZDJGd3YwWEFMbmw0aFBnTXVzTEp5N3hZN09Ud2gvSTBrYTBrYnpWTXNpa2dkUlVQRUMiLCJtYWMiOiIyNzcyYTExNzk3ZGY5ZmM4NmI4ZDY4NjdhMjQwMzA3OTVlZjZhZTU3NWUyMzgyM2UyOTQ4ODYxZTcxZjhiNDE1IiwidGFnIjoiIn0%3D',
}

params = {
    'filters': 'complex_id/int_multiple_filter|1028',
    'page': '1',
}

flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://whitewill.ru/api/v1/filter/sale/lots', params=params, cookies=cookies, headers=headers)
    items = response.json()['moscowLotFilterResultDTO']['moscowLotCardDTOs']

    for i in items:

        url = ''
        developer = ""
        project = i['complexTitle']
        korpus = ''
        section = ''
        type = ''
        finish_type = i['lotCardInfoListDTO']['lotCardInfoItemDTOs'][2]['value']
        room_count = ''
        flat_number = ''
        try:
            area = i['area']
        except:
            area = ''
        try:
            old_price = i['lotCardPriceListDTO']['lotCardPriceItemDTOs'][0]['price']
        except:
            old_price = ''
        try:
            price = int()
        except:
            price = ''
        try:
            floor = i['lotCardInfoListDTO']['lotCardInfoItemDTOs'][1]['value']
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

    break
    params['page'] = str(int(params['page']) + 1)
    print(params)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

df = pd.DataFrame(flats, columns=['Дата обновления',
 'Название проекта',
 'на англ',
 'промзона',
 'Местоположение',
 'Метро',
 'Расстояние до метро, км',
 'Время до метро, мин',
 'МЦК/МЦД/БКЛ',
 'Расстояние до МЦК/МЦД, км',
 'Время до МЦК/МЦД, мин',
 'БКЛ',
 'Расстояние до БКЛ, км',
 'Время до БКЛ, мин',
 'статус',
 'старт',
 'Комментарий',
 'Девелопер',
 'Округ',
 'Район',
 'Адрес',
 'Эскроу',
 'Корпус',
 'Конструктив',
 'Класс',
 'Срок сдачи',
 'Старый срок сдачи',
 'Стадия строительной готовности',
 'Договор',
 'Тип помещения',
 'Отделка',
 'Кол-во комнат',
 'Площадь, кв.м',
 'Цена кв.м, руб.',
 'Цена лота, руб.',
 'Скидка,%',
 'Цена кв.м со ск, руб.',
 'Цена лота со ск, руб.',
 'секция',
 'этаж',
 'номер'])



# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

