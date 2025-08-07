import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

cookies = {
    '_ym_uid': '1745939358725624294',
    '_ym_d': '1745939358',
    'scbsid_old': '2796070936',
    '_gcl_au': '1.1.96588284.1750842805',
    'lng': 'ru',
    'sessionid': '8g0eyjzktwdbl5vanxvhgp8bdtgxg9tw',
    '_gid': 'GA1.2.1542608178.1753349241',
    '_cmg_cssts9Nf8': '1753349241',
    '_comagic_ids9Nf8': '10870398951.15178199056.1753349241',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    'residential': '[]',
    'commerce': '[]',
    'country': '[]',
    'parking': '[]',
    'PHPSESSID': 'CkzPIkAFlEybdhCvEAVMSCHd9StaQ8aO',
    'ma_cid': '1753349243447274266',
    'ma_id': '3057594101744728149914',
    'sma_session_id': '2368752419',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%22be3e67a53916489460608b992809da55%22%2C%22a932251185d3bf41fcd7e2656de279f5%22%5D',
    'SCBstart': '1753349250828',
    'sma_postview_ready': '1',
    'cookie': '1',
    'nfCpwHashId': '000b35184a564af72f49d0d6cd75e199fc55710f60dfd2bf47b6554327685155',
    'SCBFormsAlreadyPulled': 'true',
    'counter_monblan': '1',
    'ma_ss_0ad8e677-9813-10a0-8198-186718b40008': '1753349243545993952.1.1753349503.43.1753349243',
    '_gat_gtag_UA_25942975_1': '1',
    'counter_admiral': '3',
    '_ga': 'GA1.1.1693162775.1750842804',
    '_ga_C9YG48HMEJ': 'GS2.1.s1753349240$o3$g1$t1753349509$j2$l0$h0',
    'sma_index_activity': '15169',
    'SCBindexAct': '4476',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://hals-development.ru/realty/object/admiral',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'scbsid_old=2750244825; _ym_uid=174219590563972705; _ym_d=1742195905; _gcl_au=1.1.723038034.1742195906; lng=ru; sessionid=fbc09ff8sbmgur2sm0esard86lsl8657; _gid=GA1.2.2036368207.1742560312; _gat_gtag_UA_25942975_1=1; _cmg_cssts9Nf8=1742560312; _comagic_ids9Nf8=10087264281.14271187536.1742560305; _ym_isad=1; residential=[]; commerce=[]; country=[]; parking=[]; PHPSESSID=OoVnWaJ7AKZXcV985JgOd9fw8jpbD5qC; _ym_visorc=w; sma_session_id=2232439034; SCBfrom=; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%229cb68ccfa454c30c1a145a7087436421%22%2C%2215384b6c442ed8de443d8f25933e9f26%22%5D; SCBstart=1742560315558; sma_postview_ready=1; cookie=1; sma_index_activity=1203; SCBindexAct=952; _ga=GA1.1.2107547660.1742195906; counter_admiral=2; _ga_C9YG48HMEJ=GS1.1.1742560311.4.1.1742560329.42.0.0',
}

params = {
    'page': 'flats',
}

url = 'https://hals-development.ru/ajax/json.php'

flats = []
count = 1

response = requests.get(url, cookies=cookies, headers=headers, params=params, verify=False)

if response.status_code == 200:
    items = response.json()

    for i in items:
        date = datetime.date.today()
        project = i["object"].replace('Элитный жилой комплекс «', '').replace('»', '').replace('Клубный дом «',
                                                                                               '').replace(
            'Премиум-квартал «', '').replace('Квартал бизнес-класса «', '')
        developer = 'Галс'
        korpus = i["block"]
        room_count = int(i["rooms"])
        if room_count == 0:
            room_count = 'Студия'
        type = i["type_name"]
        finish_type = i["decor"]
        section = i["section"]
        floor = int(i["floor"])

        if 'Клубный' in project:
            finish_type = 'Без отделки'

        elif "Монблан" in project:
            korpus = section
            section = ''
            finish_type = 'Без отделки'

        elif 'Дом' in project:
            korpus = section
            section = ''
            if korpus != '1':
                finish_type = 'Без отделки'
            else:
                finish_type = 'Предчистовая'

            type = 'Квартира'

        elif 'Адмирал' in project:
            finish_type = 'Без отделки'
            type = 'Квартира'

        if type == 'Пентхаус':
            type = "Квартира"

        area = float(i["square"])
        old_price = i["price"]
        price = i["price_sale"]

        if finish_type == '':
            finish_type = 'Без отделки'
        if finish_type == '1':
            finish_type = 'С отделкой'

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '',
                  '',
                  '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus,
                  '', '', '', '',
                  '', '', type, finish_type, room_count, area, '', old_price, '',
                  '', price, section, floor, '']
        flats.append(result)
        count += 1

time.sleep(0.05)

project = 'all'
save_flats_to_excel(flats, project, developer)
