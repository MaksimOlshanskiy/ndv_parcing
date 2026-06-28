import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from functions import save_flats_to_excel


cookies = {
    'spjs': '1780219521121_44b427fc_013526a2_a862a9bd2bea515a329561d19205ce27_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',
    'spid': '1780219521121_9b77a37a873a41294647253dfd63d087_kmoqps07galqhuxw',
    '_ym_uid': '178021952530764829',
    '_ym_d': '1780219525',
    'tmr_lvid': '7ae42b76dd5bd8a05bba1ab0142bc909',
    'tmr_lvidTS': '1780219524785',
    'scbsid_old': '4097698043',
    'uxs_uid': 'a78fc220-5cd2-11f1-8588-29484beaf526',
    '_ga': 'GA1.1.264034229.1780219527',
    'adrdel': '1780219529054',
    'adrdel': '1780219529054',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1780305929085%2C%22sl%22%3A%7B%22224%22%3A1780219529085%2C%221228%22%3A1780219529085%7D%7D',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1780305929085%2C%22sl%22%3A%7B%22224%22%3A1780219529085%2C%221228%22%3A1780219529085%7D%7D',
    'mindboxDeviceUUID': 'd6b3597d-4b0b-4e45-8167-0b84971b36f7',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '_cmg_csstvfLiQ': '1780260734',
    '_comagic_idvfLiQ': '12201591103.16755725683.1780260731',
    'spsc': '1781618515641_5457b2bbd8adaf75a2dde8fc1d525fd4_YFFv8xBSXhZdrc7.EyCpz82JudYTIZxyZfxHvY2UHzkZ',
    'sma_session_id': '2738930617',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    'SCBstart': '1781618518227',
    'SCBporogAct': '5000',
    'sessionId': '17816185192241636692',
    'SCBFormsAlreadyPulled': 'true',
    'smFpId_old_values': '%5B%2269a8c60d87e15c5e811dc898ec400d63%22%2C%2202b9df5f157e98e4dbcf128531ba7d2f%22%2C%220bbaadf22d440f0330d4eed28458fa70%22%5D',
    'sma_postview_ready': '1',
    'PHPSESSID': 'u63j7uk8k77f1aqc06cqi47q84',
    'SCBindexAct': '1660',
    '_ga_H5S7YBLWM3': 'GS2.1.s17816185192241636692$o6$g1$t1781618557$j22$l0$h0',
    '_ga_70ZZHDSCR6': 'GS2.1.s1781618519$o6$g1$t1781618557$j22$l0$h0',
    'sma_index_activity': '2160',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': '',
    'baggage': 'sentry-environment=production,sentry-public_key=64d42d1ec99f4044ff0df570a905dbca,sentry-trace_id=ea9bdca9923d4d8a95fe2b49156d0f6c,sentry-sample_rate=0.1,sentry-transaction=%2Fcommercials%2Fpomeshcheniya%2F*,sentry-sampled=false',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.mr-group.ru/commercials/pomeshcheniya/page-2/',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'ea9bdca9923d4d8a95fe2b49156d0f6c-a148c6eedd7272cb-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': 'spjs=1780219521121_44b427fc_013526a2_a862a9bd2bea515a329561d19205ce27_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; spid=1780219521121_9b77a37a873a41294647253dfd63d087_kmoqps07galqhuxw; _ym_uid=178021952530764829; _ym_d=1780219525; tmr_lvid=7ae42b76dd5bd8a05bba1ab0142bc909; tmr_lvidTS=1780219524785; scbsid_old=4097698043; uxs_uid=a78fc220-5cd2-11f1-8588-29484beaf526; _ga=GA1.1.264034229.1780219527; adrdel=1780219529054; adrdel=1780219529054; adrcid=A0r9KB4fc8duMUv2jPsp-tg; adrcid=A0r9KB4fc8duMUv2jPsp-tg; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1780305929085%2C%22sl%22%3A%7B%22224%22%3A1780219529085%2C%221228%22%3A1780219529085%7D%7D; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1780305929085%2C%22sl%22%3A%7B%22224%22%3A1780219529085%2C%221228%22%3A1780219529085%7D%7D; mindboxDeviceUUID=d6b3597d-4b0b-4e45-8167-0b84971b36f7; directCrm-session=%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _cmg_csstvfLiQ=1780260734; _comagic_idvfLiQ=12201591103.16755725683.1780260731; spsc=1781618515641_5457b2bbd8adaf75a2dde8fc1d525fd4_YFFv8xBSXhZdrc7.EyCpz82JudYTIZxyZfxHvY2UHzkZ; sma_session_id=2738930617; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; SCBstart=1781618518227; SCBporogAct=5000; sessionId=17816185192241636692; SCBFormsAlreadyPulled=true; smFpId_old_values=%5B%2269a8c60d87e15c5e811dc898ec400d63%22%2C%2202b9df5f157e98e4dbcf128531ba7d2f%22%2C%220bbaadf22d440f0330d4eed28458fa70%22%5D; sma_postview_ready=1; PHPSESSID=u63j7uk8k77f1aqc06cqi47q84; SCBindexAct=1660; _ga_H5S7YBLWM3=GS2.1.s17816185192241636692$o6$g1$t1781618557$j22$l0$h0; _ga_70ZZHDSCR6=GS2.1.s1781618519$o6$g1$t1781618557$j22$l0$h0; sma_index_activity=2160',
}



params = {
    'category': 'commercials',
    'page': '1',
    'limit': '1000',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:
    try:
        response = requests.get('https://www.mr-group.ru/api/sale/products', params=params, cookies=cookies, headers=headers)
    except:
        break
    try:
        items = response.json()["items"]
    except:
        break

    for i in items:

        if i['status']['code'] == 'booked':
            continue

        url = ""

        date = datetime.date.today()
        project = i["project"]["name"]
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
        developer = "MR"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i["building"]["name"].replace('Корпус ', '')
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = ''
        finish_type = ""
        room_count = int(i["rooms_number"])
        area = i["area"]
        price_per_metr = ''
        old_price = ""
        discount = ''
        price_per_metr_new = ''
        if not i['discount']:
            price = ''
            old_price = i["price"]
        else:
            price = i['discount']['price']
            old_price = i["price"]
        section = ''
        floor = i["floor"]
        flat_number = ''

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break
    print(len(flats))
    params["page"] = str(int(params["page"]) + 1)
    sleep_time = random.uniform(7, 11)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)

