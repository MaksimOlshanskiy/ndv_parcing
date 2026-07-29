import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all
import requests

cookies = {
    '_ym_uid': '1776591913437946397',
    '_ym_d': '1776591913',
    'device_view': 'full',
    'tmr_lvid': 'c18eca6cb3da30e034ac685e519f1725',
    'tmr_lvidTS': '1776591911319',
    '_dmp_cookie_deny': '1',
    '_ct': '700000001920935760',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'domain_sid': 'MoUm9hd-oxZ5HqjonnMpA%3A1782897972957',
    'origin_referer': 'https%3A%2F%2Fwww.ndv.ru%2F',
    'tmr_detect': '0%7C1782898496093',
}

cookies = {
    '__ddg9_': '5.228.114.84',
    '__ddg1_': '4thLbwRSnUGtmVnRLzJq',
    'PHPSESSID': 'vStgkUMifkQFDjFPWC0bMIyejQP7Lai2',
    'city': 'serpukhov',
    'scbsid_old': '16031261345',
    'tmr_lvid': '4f5c65bcda72c22bbd544cbd16bceb3c',
    'tmr_lvidTS': '1780231023662',
    '_ym_uid': '1780231024638157993',
    '_ym_d': '1785261276',
    '_ym_isad': '2',
    '_cmg_csst9UKlD': '1785261277',
    '_comagic_id9UKlD': '12501387013.17093928278.1785261276',
    '_ym_visorc': 'w',
    'domain_sid': 'EvYtJHstLQ3qBm2ZjMfIX%3A1785261277553',
    'sma_session_id': '2788741872',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'SCBstart': '1785261278017',
    'smFpId_old_values': '%5B%221760a41b46d1a0c018f5c6bd064f5ef3%22%5D',
    'sma_postview_ready': '1',
    'tmr_detect': '0%7C1785261403003',
    'SCBindexAct': '4704',
    'sma_index_activity': '13044',
    '__ddg8_': 'PsWZyconCN3Ufygz',
    '__ddg10_': '1785261409',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://avadom.ru/objects/',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    # 'cookie': '__ddg9_=5.228.114.84; __ddg1_=4thLbwRSnUGtmVnRLzJq; PHPSESSID=vStgkUMifkQFDjFPWC0bMIyejQP7Lai2; city=serpukhov; scbsid_old=16031261345; tmr_lvid=4f5c65bcda72c22bbd544cbd16bceb3c; tmr_lvidTS=1780231023662; _ym_uid=1780231024638157993; _ym_d=1785261276; _ym_isad=2; _cmg_csst9UKlD=1785261277; _comagic_id9UKlD=12501387013.17093928278.1785261276; _ym_visorc=w; domain_sid=EvYtJHstLQ3qBm2ZjMfIX%3A1785261277553; sma_session_id=2788741872; SCBfrom=; SCBnotShow=-1; SCBporogAct=5000; SCBstart=1785261278017; smFpId_old_values=%5B%221760a41b46d1a0c018f5c6bd064f5ef3%22%5D; sma_postview_ready=1; tmr_detect=0%7C1785261403003; SCBindexAct=4704; sma_index_activity=13044; __ddg8_=PsWZyconCN3Ufygz; __ddg10_=1785261409',
}



flats = []
count = 0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

response = requests.get(
    'https://avadom.ru/local/api/new/apartments/?onlyAvailable=true&projects[]=94274',
    cookies=cookies,
    headers=headers,
)
print(response.status_code)
if response.status_code == 200:
    items = response.json()

    for i in items:
        date = datetime.date.today()
        project = i['objectName']
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
        developer = "СЗ ГОРОДСКОЙ БОР"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i["literNum"]
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = i['deadline']
        stadia = ''
        dogovor = ''
        type_ = i['type'].replace('Квартира', "Квартиры")
        room_count = ''
        area = i["area"]
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''
        section = ''
        floor = i["floorNum"]
        flat_number = ''
        finish_type = 'С отделкой'
        old_price = i["price"].replace(' ', "")
        price = i["price"].replace(' ', "")

        print(
            f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                  mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type_, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)





save_flats_to_excel(flats, 'all', developer)
