import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    'scbsid_old': '4097698043',
    '_ym_uid': '1781866645356053084',
    '_ym_d': '1781866645',
    'PHPSESSID': 'rmn59ophvke2t7jtj26mvaltlq',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ct_ids': 'x7ivk2ue%3A59982%3A554629870',
    '_ct_session_id': '554629870',
    '_ct_site_id': '59982',
    'call_s': '___x7ivk2ue.1781868445.554629870.499172:1422563|2___',
    '_ct': '2400000000383332371',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'cted': 'modId%3Dx7ivk2ue%3Bya_client_id%3D1781866645356053084',
    'sma_session_id': '2742367497',
    'SCBfrom': 'https%3A%2F%2Fopus-home.ru%2F',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D',
    'SCBstart': '1781866647491',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'cookieWarningAccepted': 'true',
    'sma_index_activity': '9877',
    'SCBindexAct': '2483',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://opus-bc.ru/plans',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=4097698043; _ym_uid=1781866645356053084; _ym_d=1781866645; PHPSESSID=rmn59ophvke2t7jtj26mvaltlq; _ym_isad=2; _ym_visorc=w; _ct_ids=x7ivk2ue%3A59982%3A554629870; _ct_session_id=554629870; _ct_site_id=59982; call_s=___x7ivk2ue.1781868445.554629870.499172:1422563|2___; _ct=2400000000383332371; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; cted=modId%3Dx7ivk2ue%3Bya_client_id%3D1781866645356053084; sma_session_id=2742367497; SCBfrom=https%3A%2F%2Fopus-home.ru%2F; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D; SCBstart=1781866647491; SCBFormsAlreadyPulled=true; sma_postview_ready=1; cookieWarningAccepted=true; sma_index_activity=9877; SCBindexAct=2483',
}



flats = []
count = 1

response = requests.get('https://opus-bc.ru/api/hydra/data/retail', cookies=cookies, headers=headers)
print(response.status_code)
if response.status_code == 200:
    data = response.json()['apartments']
    print(data)

    for j in data.values():
        print(j)
        if j.get("st", '') == 0:
            continue
        date = datetime.date.today()
        project = 'Опус'
        developer = 'Pioneer'
        room_count = ''
        korpus = '1'
        type = ''
        area = j.get("sq", '')
        old_price = j.get("tc", '')
        price = j.get("tc", '')
        floor = j.get('f', '')
        section = ''

        if old_price == price:
            price = None

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, 'с отделкой', room_count, area, '', old_price, '', '', price,
                  section, floor, '']
        flats.append(result)
        count += 1

else:
    print(f'Ошибка: {response.status_code}')

time.sleep(0.05)

project = 'Opus'
developer = 'Pioneer'

save_flats_to_excel(flats, project, developer)
