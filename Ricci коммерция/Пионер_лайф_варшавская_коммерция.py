import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    'scbsid_old': '4097698043',
    '_ym_uid': '178187343211014915',
    '_ym_d': '1781873432',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_gcl_au': '1.1.327683562.1781873433',
    '_gid': 'GA1.2.1151603482.1781873433',
    '_gat_UA-121782956-1': '1',
    '_gat_UA-121782956-2': '1',
    '_dc_gtm_UA-121782956-1': '1',
    'mindboxDeviceUUID': 'd6b3597d-4b0b-4e45-8167-0b84971b36f7',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D',
    'adrdel': '1781873433239',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'tmr_lvid': 'fa4116436e70ffd2c272a4a3b5dc721f',
    'tmr_lvidTS': '1781873433255',
    'acs_3': '%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1781959833432%2C%22sl%22%3A%7B%22224%22%3A1781873433432%2C%221228%22%3A1781873433432%7D%7D',
    '_fbp': 'fb.1.1781873433544.367827819408585723',
    '_ct_ids': '3v5hozfy%3A32937%3A1104834170',
    '_ct_session_id': '1104834170',
    '_ct_site_id': '32937',
    '_ct': '1100000000749787196',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'cted': 'modId%3D3v5hozfy%3Bclient_id%3D963862369.1781873433%3Bya_client_id%3D178187343211014915%3Bfbp%3Dfb.1.1781873433544.367827819408585723',
    'domain_sid': 'SfORMLVXfT-7RsdpNr8GE%3A1781873434546',
    'sma_session_id': '2742507234',
    'SCBfrom': 'https%3A%2F%2Fpioneer.ru%2F',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D',
    'SCBstart': '1781873435527',
    'tmr_detect': '0%7C1781873435831',
    'SCBFormsAlreadyPulled': 'true',
    '_ga': 'GA1.2.963862369.1781873433',
    'sma_postview_ready': '1',
    'PHPSESSID': 'a4eldc01vehe1lmk438ro0hhc5',
    'call_s': '___3v5hozfy.1781875243.1104834170.115550:1561177|2___',
    '_ga_T329EBLZZ8': 'GS2.2.s1781873433$o1$g1$t1781873452$j41$l0$h0',
    'sma_index_activity': '1952',
    'SCBindexAct': '1450',
    '_ga_519VME92KM': 'GS2.1.s1781873433$o1$g1$t1781873453$j40$l0$h0',
    'PageCount': '6',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://varshavskaya.life/commercial/search',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=4097698043; _ym_uid=178187343211014915; _ym_d=1781873432; _ym_isad=2; _ym_visorc=w; _gcl_au=1.1.327683562.1781873433; _gid=GA1.2.1151603482.1781873433; _gat_UA-121782956-1=1; _gat_UA-121782956-2=1; _dc_gtm_UA-121782956-1=1; mindboxDeviceUUID=d6b3597d-4b0b-4e45-8167-0b84971b36f7; directCrm-session=%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D; adrdel=1781873433239; adrcid=A0r9KB4fc8duMUv2jPsp-tg; tmr_lvid=fa4116436e70ffd2c272a4a3b5dc721f; tmr_lvidTS=1781873433255; acs_3=%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1781959833432%2C%22sl%22%3A%7B%22224%22%3A1781873433432%2C%221228%22%3A1781873433432%7D%7D; _fbp=fb.1.1781873433544.367827819408585723; _ct_ids=3v5hozfy%3A32937%3A1104834170; _ct_session_id=1104834170; _ct_site_id=32937; _ct=1100000000749787196; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; cted=modId%3D3v5hozfy%3Bclient_id%3D963862369.1781873433%3Bya_client_id%3D178187343211014915%3Bfbp%3Dfb.1.1781873433544.367827819408585723; domain_sid=SfORMLVXfT-7RsdpNr8GE%3A1781873434546; sma_session_id=2742507234; SCBfrom=https%3A%2F%2Fpioneer.ru%2F; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%220bbaadf22d440f0330d4eed28458fa70%22%5D; SCBstart=1781873435527; tmr_detect=0%7C1781873435831; SCBFormsAlreadyPulled=true; _ga=GA1.2.963862369.1781873433; sma_postview_ready=1; PHPSESSID=a4eldc01vehe1lmk438ro0hhc5; call_s=___3v5hozfy.1781875243.1104834170.115550:1561177|2___; _ga_T329EBLZZ8=GS2.2.s1781873433$o1$g1$t1781873452$j41$l0$h0; sma_index_activity=1952; SCBindexAct=1450; _ga_519VME92KM=GS2.1.s1781873433$o1$g1$t1781873453$j40$l0$h0; PageCount=6',
}



flats = []
count = 1

response = requests.get('https://varshavskaya.life/hydra/json/data_com.json', cookies=cookies, headers=headers)
print(response.status_code)
if response.status_code == 200:
    data = response.json()['apartments']


    for j in data.values():

        if j.get("st", '') != 1:
            continue
        date = datetime.date.today()
        project = 'Life Варшавская'
        developer = 'Pioneer'
        room_count = ''
        korpus = j.get('b', '')
        type = j.get('d', '')
        area = j.get("sq", '')
        old_price = j.get("tc", '')
        price = j.get("tc", '')
        floor = j.get('f', '')
        section = ''

        if old_price == price:
            price = None

        print(
            f"{count},{j['n']},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}")

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
