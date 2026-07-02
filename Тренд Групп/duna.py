import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

cookies = {
    'fav': '[]',
    '_ym_uid': '1783020388946989798',
    '_ym_d': '1783020388',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'mgo_sb_migrations': '1418474375998%253D1',
    'mgo_sb_current': 'typ%253Dorganic%257C%252A%257Csrc%253Dgoogle%257C%252A%257Cmdm%253Dorganic%257C%252A%257Ccmp%253D%2528none%2529%257C%252A%257Ccnt%253D%2528none%2529%257C%252A%257Ctrm%253D%2528none%2529%257C%252A%257Cmango%253D%2528none%2529',
    'mgo_sb_first': 'typ%253Dorganic%257C%252A%257Csrc%253Dgoogle%257C%252A%257Cmdm%253Dorganic%257C%252A%257Ccmp%253D%2528none%2529%257C%252A%257Ccnt%253D%2528none%2529%257C%252A%257Ctrm%253D%2528none%2529%257C%252A%257Cmango%253D%2528none%2529',
    'mgo_uid': 'UmzIvmgeYuEMThhmNL7z',
    'mgo_cnt': '1',
    'mgo_sid': 'gbbcthkbc411001p7jjp',
    '_ymab_param': 'XQCEMFYfxpeaE4f_aY3RyiLs4Y3Tv5nmGzBy9nrNvpvwiaSSVqdXh_cijA6-FghN9K2pYi1FaBWovlUc69KWLah2-vw',
    'PHPSESSID': 'XFubWd6rwiyh7IDuQcGLO62mL9WGl4Di',
    'mgo_sb_session': 'pgs%253D4%257C%252A%257Ccpg%253Dhttps%253A%252F%252Fxn--80ahfqq5h.xn--p1ai%252Frealty',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://xn--80ahfqq5h.xn--p1ai/realty',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': 'fav=[]; _ym_uid=1783020388946989798; _ym_d=1783020388; _ym_isad=2; _ym_visorc=w; mgo_sb_migrations=1418474375998%253D1; mgo_sb_current=typ%253Dorganic%257C%252A%257Csrc%253Dgoogle%257C%252A%257Cmdm%253Dorganic%257C%252A%257Ccmp%253D%2528none%2529%257C%252A%257Ccnt%253D%2528none%2529%257C%252A%257Ctrm%253D%2528none%2529%257C%252A%257Cmango%253D%2528none%2529; mgo_sb_first=typ%253Dorganic%257C%252A%257Csrc%253Dgoogle%257C%252A%257Cmdm%253Dorganic%257C%252A%257Ccmp%253D%2528none%2529%257C%252A%257Ccnt%253D%2528none%2529%257C%252A%257Ctrm%253D%2528none%2529%257C%252A%257Cmango%253D%2528none%2529; mgo_uid=UmzIvmgeYuEMThhmNL7z; mgo_cnt=1; mgo_sid=gbbcthkbc411001p7jjp; _ymab_param=XQCEMFYfxpeaE4f_aY3RyiLs4Y3Tv5nmGzBy9nrNvpvwiaSSVqdXh_cijA6-FghN9K2pYi1FaBWovlUc69KWLah2-vw; PHPSESSID=XFubWd6rwiyh7IDuQcGLO62mL9WGl4Di; mgo_sb_session=pgs%253D4%257C%252A%257Ccpg%253Dhttps%253A%252F%252Fxn--80ahfqq5h.xn--p1ai%252Frealty',
}

params = {
    'cmd': 'flats',
}



flats = []
count = 0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

response = requests.get('https://xn--80ahfqq5h.xn--p1ai/ajax/', params=params, cookies=cookies, headers=headers)
print(response.status_code)
items = response.json()['flats']
for i in items:
    print(i)
    date = datetime.date.today()
    project = "Дюна"
    developer = 'Тренд групп'

    korpus = i['CORPUS_NUMBER']
    room_count = i["ROOMS"]
    type = i["CATEGORY"].replace('квартира', 'квартиры')
    area = i['TOTAL_AREA']
    price = i['PRICE']
    floor = i["FLOOR_NUM"]

    print(
        f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

    result = [date, project, '', '', '', '', '', '', '', '', '', '',
              '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
              '', '', type, 'Предчистовая', room_count, area, '', int(price), '', '', '',
              '', floor, '']
    flats.append(result)
    count += 1


save_flats_to_excel(flats, project, developer)
