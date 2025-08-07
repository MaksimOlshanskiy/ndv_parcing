import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

cookies = {
    'csrftoken': 'QpkwGmZagqImviY9NtdC1WfAIeMYtAzDjUTTORuUZ23YiCKafvo5uXlszItv4iCo',
    '_ga': 'GA1.1.53422926.1744192078',
    '_ct_ids': '2c49810a%3A8292%3A3599307973',
    '_ct_session_id': '3599307973',
    '_ct_site_id': '8292',
    '_ct': '300000001875855025',
    '_ct_client_global_id': '8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4',
    'scbsid_old': '2796070936',
    '_ym_uid': '1744192078483093664',
    '_ym_d': '1744192078',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    'cted': 'modId%3D2c49810a%3Bclient_id%3D53422926.1744192078%3Bya_client_id%3D1744192078483093664',
    'sma_session_id': '2255411124',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%2204b0ffbac42ccceb635ec5bff5b15618%22%5D',
    'SCBporogAct': '5000',
    'SCBstart': '1744192082177',
    'session_time_sent': '60',
    'session_time': '68.15',
    'call_s': '___2c49810a.1744193951.3599307973.19058:102056|2___',
    '_ga_189N5HVTV5': 'GS1.1.1744192077.1.1.1744192320.60.0.0',
    '_ga_KRF8PY3CGV': 'GS1.1.1744192077.1.1.1744192320.0.0.0',
    'sma_index_activity': '8623',
    'SCBindexAct': '2369',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://kaskad-park.ru/objects/?realty=townhouse&show_booked=2&offset=0&limit=20&price_0=13700000&price_1=37948337',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'csrftoken=QpkwGmZagqImviY9NtdC1WfAIeMYtAzDjUTTORuUZ23YiCKafvo5uXlszItv4iCo; _ga=GA1.1.53422926.1744192078; _ct_ids=2c49810a%3A8292%3A3599307973; _ct_session_id=3599307973; _ct_site_id=8292; _ct=300000001875855025; _ct_client_global_id=8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4; scbsid_old=2796070936; _ym_uid=1744192078483093664; _ym_d=1744192078; _ym_isad=1; _ym_visorc=w; cted=modId%3D2c49810a%3Bclient_id%3D53422926.1744192078%3Bya_client_id%3D1744192078483093664; sma_session_id=2255411124; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; smFpId_old_values=%5B%2204b0ffbac42ccceb635ec5bff5b15618%22%5D; SCBporogAct=5000; SCBstart=1744192082177; session_time_sent=60; session_time=68.15; call_s=___2c49810a.1744193951.3599307973.19058:102056|2___; _ga_189N5HVTV5=GS1.1.1744192077.1.1.1744192320.60.0.0; _ga_KRF8PY3CGV=GS1.1.1744192077.1.1.1744192320.0.0.0; sma_index_activity=8623; SCBindexAct=2369',
}

params = {
    'show_booked': '2',
    'offset': 0,
    'limit': '20',
    'price_0': '13700000',
    'price_1': '37948337',
}

url = 'https://kaskad-park.ru/api/townhouse/'

flats = []
count=0

response = requests.get(url, cookies=cookies, params=params, headers=headers)

if response.status_code == 200:
    item = response.json()

    items = item.get("results", [])

    for i in items:
        count+=1
        date = datetime.date.today()
        project = 'Каскад Парк'
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
        developer = "Каскад"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i['building']
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Таунхаус'
        finish_type = 'С отделкой '
        room_count = ''
        area = i['area']
        price_per_metr = ''
        old_price = float(i['old_price'])
        discount = ''
        price_per_metr_new = ''
        price = float(i["price"])
        section = int(i['section'])
        floor = ''
        flat_number = ''

        if old_price == price:
            price = None

        print(
            f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                  mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

else:
    print(f'Ошибка: {response.status_code}')

time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
