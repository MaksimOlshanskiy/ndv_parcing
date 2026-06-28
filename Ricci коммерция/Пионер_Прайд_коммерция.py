import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    'scbsid_old': '4097698043',
    '_gcl_au': '1.1.1442758578.1781872503',
    '_ym_uid': '1781872503346089409',
    '_ym_d': '1781872503',
    '_ym_isad': '2',
    'mindboxDeviceUUID': 'd6b3597d-4b0b-4e45-8167-0b84971b36f7',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D',
    'sma_session_id': '2742488177',
    'SCBfrom': 'https%3A%2F%2Fpioneer.ru%2F',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D',
    '_ct_ids': '1kfi6z87%3A52402%3A2296485599',
    '_ct_session_id': '2296485599',
    '_ct_site_id': '52402',
    'call_s': '___1kfi6z87.1781874303.2296485599.250668:1561195|2___',
    '_ct': '800000001067458071',
    '_ym_visorc': 'w',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'SCBstart': '1781872504018',
    'cted': 'modId%3D1kfi6z87%3Bya_client_id%3D1781872503346089409',
    'SCBporogAct': '5000',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'cookieWarningAccepted': 'true',
    'PHPSESSID': 't9moi0rh88hnmehvvlt7t9a101',
    'sma_index_activity': '5606',
    'SCBindexAct': '4656',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://pride-home.ru/search-com',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=4097698043; _gcl_au=1.1.1442758578.1781872503; _ym_uid=1781872503346089409; _ym_d=1781872503; _ym_isad=2; mindboxDeviceUUID=d6b3597d-4b0b-4e45-8167-0b84971b36f7; directCrm-session=%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D; sma_session_id=2742488177; SCBfrom=https%3A%2F%2Fpioneer.ru%2F; SCBnotShow=-1; smFpId_old_values=%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D; _ct_ids=1kfi6z87%3A52402%3A2296485599; _ct_session_id=2296485599; _ct_site_id=52402; call_s=___1kfi6z87.1781874303.2296485599.250668:1561195|2___; _ct=800000001067458071; _ym_visorc=w; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; SCBstart=1781872504018; cted=modId%3D1kfi6z87%3Bya_client_id%3D1781872503346089409; SCBporogAct=5000; SCBFormsAlreadyPulled=true; sma_postview_ready=1; cookieWarningAccepted=true; PHPSESSID=t9moi0rh88hnmehvvlt7t9a101; sma_index_activity=5606; SCBindexAct=4656',
}



flats = []
count = 1

response = requests.get('https://pride-home.ru/hydra/json/com.json', cookies=cookies, headers=headers)
print(response.status_code)
if response.status_code == 200:
    data = response.json()['apartments']


    for j in data.values():

        if j.get("st", '') == 0:
            continue
        date = datetime.date.today()
        project = 'Прайд'
        developer = 'Pioneer'
        room_count = ''
        korpus = '1'
        type = j.get('d', '')
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

save_flats_to_excel(flats, project, developer)
