import datetime
import time
import requests

from functions import save_flats_to_excel

from save_to_excel import save_flats_to_excel_old_new_all

flats = []
count = 1

cookies = {
    'flomni_641ae9eee9a473ff3717a7c0': '{%22userHash%22:%22f62815d0-467e-467e-afaa-97d0431bbd55%22}',
    '_ym_uid': '1745481418255241855',
    '_ym_d': '1755769783',
    'scbsid_old': '2746015342',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '_gcl_au': '1.1.95159126.1755769785',
    'adtech_uid': 'cb586a57-4870-405e-96b5-a321c07af315%3Adsk1.ru',
    'top100_id': 't1.7712236.1361148438.1755769785039',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'tmr_lvid': '389d6d0dd297aeaee488ca2c3c29679c',
    'tmr_lvidTS': '1745481418363',
    '__upin': 'uiym2TZM/0r3xWqRBX6KrA',
    'as-user': '7bd7f275-712f-4908-9cc9-a064b62c8188',
    'OAuth': '1431901788',
    'wr_visit_id': '1431901788',
    'mars': '40d992782fe54f93b52066286d09883f',
    'SCBstart': '1755769788285',
    'SCBporogAct': '5000',
    'lptChatClientId': '1755769788663-76284',
    'SCBFormsAlreadyPulled': 'true',
    'lp_tracker_id': '76284',
    'ip': 'false',
    'lptracker_visitor_id': 'false',
    'lptracker_view_id': 'f9d1bde9-86bd-4891-a701-307476bde801',
    '_fsid': 's%3AhTLZhwGsGvClFGW2qiTXczwZp1u54iVk.rap3JURKya%2FCJCT6xYoE3UoLcGx01DAIyPRhlR%2FsS0c',
    '_cmg_csst1P1xK': '1757578666',
    '_comagic_id1P1xK': '11168033006.15522119306.1757578666',
    '_ym_isad': '2',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1757665068551%2C%22sl%22%3A%7B%22224%22%3A1757578668551%2C%221228%22%3A1757578668551%7D%7D',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1757665068551%2C%22sl%22%3A%7B%22224%22%3A1757578668551%2C%221228%22%3A1757578668551%7D%7D',
    'adrdel': '1757578668905',
    'adrdel': '1757578668905',
    'sma_session_id': '2421915745',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22dcd0255870a3687c10d524802104e593%22%2C%222488b0e958469f2da6c6193c8be92e7e%22%5D',
    'domain_sid': 'nxLWAutHoCpiHIKzocVpy%3A1757578671751',
    'rai': '5408814677c6449daca6bcd84ce123b1',
    'counter': '4',
    '_yasc': 'K2m4FiUGRdL2A7RzA93Jcy45LaZk9KdmE5fGHWE5tN7adDpJe5YnqsVtzxeuMnTaTg==',
    '_ym_visorc': 'w',
    'gtm_session_start': '1757582337335',
    'startSession': 'true',
    'sma_postview_ready': '1',
    'gtm_session_threshold': 'true',
    'tmr_detect': '0%7C1757582444635',
    '2_plus_60sec_on_site': '1',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    'SCBindexAct': '1001',
    'PageNumber': '17',
    'pageviewTimerDsk1': '590',
    'startDate': '1757582888953',
    'counter_dsk1': '25',
    'SCBindexAct': '4975',
    't3_sid_7712236': 's1.972930359.1757578669364.1757582904045.1.56.12.1..',
    'sma_index_activity': '36863',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'apiclient': 'DSK',
    'if-none-match': 'W/"f111-aH/TH5ff1nDg6gSGMpKgfE1U+6U"',
    'priority': 'u=1, i',
    'referer': 'https://www.dsk1.ru/kommercheskaya-nedvizhimost/1-sheremetevskij',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': 'flomni_641ae9eee9a473ff3717a7c0={%22userHash%22:%22f62815d0-467e-467e-afaa-97d0431bbd55%22}; _ym_uid=1745481418255241855; _ym_d=1755769783; scbsid_old=2746015342; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _gcl_au=1.1.95159126.1755769785; adtech_uid=cb586a57-4870-405e-96b5-a321c07af315%3Adsk1.ru; top100_id=t1.7712236.1361148438.1755769785039; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; tmr_lvid=389d6d0dd297aeaee488ca2c3c29679c; tmr_lvidTS=1745481418363; __upin=uiym2TZM/0r3xWqRBX6KrA; as-user=7bd7f275-712f-4908-9cc9-a064b62c8188; OAuth=1431901788; wr_visit_id=1431901788; mars=40d992782fe54f93b52066286d09883f; SCBstart=1755769788285; SCBporogAct=5000; lptChatClientId=1755769788663-76284; SCBFormsAlreadyPulled=true; lp_tracker_id=76284; ip=false; lptracker_visitor_id=false; lptracker_view_id=f9d1bde9-86bd-4891-a701-307476bde801; _fsid=s%3AhTLZhwGsGvClFGW2qiTXczwZp1u54iVk.rap3JURKya%2FCJCT6xYoE3UoLcGx01DAIyPRhlR%2FsS0c; _cmg_csst1P1xK=1757578666; _comagic_id1P1xK=11168033006.15522119306.1757578666; _ym_isad=2; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1757665068551%2C%22sl%22%3A%7B%22224%22%3A1757578668551%2C%221228%22%3A1757578668551%7D%7D; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1757665068551%2C%22sl%22%3A%7B%22224%22%3A1757578668551%2C%221228%22%3A1757578668551%7D%7D; adrdel=1757578668905; adrdel=1757578668905; sma_session_id=2421915745; SCBnotShow=-1; smFpId_old_values=%5B%22dcd0255870a3687c10d524802104e593%22%2C%222488b0e958469f2da6c6193c8be92e7e%22%5D; domain_sid=nxLWAutHoCpiHIKzocVpy%3A1757578671751; rai=5408814677c6449daca6bcd84ce123b1; counter=4; _yasc=K2m4FiUGRdL2A7RzA93Jcy45LaZk9KdmE5fGHWE5tN7adDpJe5YnqsVtzxeuMnTaTg==; _ym_visorc=w; gtm_session_start=1757582337335; startSession=true; sma_postview_ready=1; gtm_session_threshold=true; tmr_detect=0%7C1757582444635; 2_plus_60sec_on_site=1; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; SCBindexAct=1001; PageNumber=17; pageviewTimerDsk1=590; startDate=1757582888953; counter_dsk1=25; SCBindexAct=4975; t3_sid_7712236=s1.972930359.1757578669364.1757582904045.1.56.12.1..; sma_index_activity=36863',
}

params = {
    'client': [
        'DSK',
        'FSK',
    ],
    'complex_slug': '1-leningradskij',
    'limit': '500',
}

response = requests.get('https://www.dsk1.ru/api/v3/commercial/all', params=params, cookies=cookies, headers=headers)
items = response.json()

for i in items:
    url = i["externalId"]
    date = datetime.date.today()
    project = i["project"]["title"]
    developer = "ДСК-1"
    korpus = str(i["corpus"]["number"].replace(',','.'))
    type = ''
    room_count = ''
    finish_type = i['finishing']

    area = i["areaTotal"]
    old_price = i["priceWoDiscount"]
    price = i["price"]
    section = i["section"]["number"]
    floor = int(i["floor"]["number"])

    if old_price == price:
        price = None

    print(
        f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, отделка: {finish_type}")

    result = [
        date, project, '', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', developer,
        '', '', '', '', korpus, '', '', '', '', '',
        '', type, finish_type, room_count, area, '', old_price, '', '',
        price, section, floor, ''
    ]
    flats.append(result)
    count += 1

time.sleep(0.2)  # Задержка между запросами

save_flats_to_excel(flats, project, developer)
