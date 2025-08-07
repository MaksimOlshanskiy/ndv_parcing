import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    'scbsid_old': '2750244825',
    '_ym_uid': '1742456422939317968',
    '_ym_d': '1742456422',
    '_ym_isad': '1',
    '_ga': 'GA1.1.341132259.1742456423',
    '_ym_visorc': 'w',
    '__hid': '0195b27f-12f2-75b1-ad69-d4f1fe01a4a2',
    '__buttonly_id': '29419616',
    'BX_USER_ID': '7c7565be1314918dd51b7cd2a5978979',
    'sma_session_id': '2230764664',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%2215384b6c442ed8de443d8f25933e9f26%22%5D',
    '_cmg_csstg0WNQ': '1742456607',
    '_comagic_idg0WNQ': '10078105831.14260264891.1742456602',
    'PHPSESSID': '1UtN84gQB5913RWUD2WRJfVTkCybyWz3',
    'SCBFormsAlreadyPulled': 'true',
    'SCBporogAct': '5000',
    'sma_index_activity': '14834',
    'SCBindexAct': '3179',
    '_ga_Y4NL1WNYFK': 'GS1.1.1742456422.1.1.1742458548.0.0.0',
    'counter_rodinapark': '2',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://rodinapark.ru/params/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'scbsid_old=2750244825; _ym_uid=1742456422939317968; _ym_d=1742456422; _ym_isad=1; _ga=GA1.1.341132259.1742456423; _ym_visorc=w; __hid=0195b27f-12f2-75b1-ad69-d4f1fe01a4a2; __buttonly_id=29419616; BX_USER_ID=7c7565be1314918dd51b7cd2a5978979; sma_session_id=2230764664; SCBnotShow=-1; smFpId_old_values=%5B%2215384b6c442ed8de443d8f25933e9f26%22%5D; _cmg_csstg0WNQ=1742456607; _comagic_idg0WNQ=10078105831.14260264891.1742456602; PHPSESSID=1UtN84gQB5913RWUD2WRJfVTkCybyWz3; SCBFormsAlreadyPulled=true; SCBporogAct=5000; sma_index_activity=14834; SCBindexAct=3179; _ga_Y4NL1WNYFK=GS1.1.1742456422.1.1.1742458548.0.0.0; counter_rodinapark=2',
}

params = {
    'page': 'flats',
}

url = 'https://rodinapark.ru/ajax/json.php'

flats = []
count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s




response = requests.get(url, params=params, cookies=cookies, headers=headers)

if response.status_code == 200:
    items = response.json()

    for i in items:
        date = datetime.date.today()
        project = 'Родина парк'
        developer = 'Родина Групп'
        korpus = i["building"]
        room_count = i["bedroom"]
        try:
            if '-евро' in room_count:
                room_count=room_count.split('-')[0]+'Е'
        except:
            room_count=i["bedroom"]
        area = i["area"]
        price = i["cost"]
        floor = i["floor"]

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', "Квартира", 'Без отделки', room_count, area, '', price, '', '', '',
                  '', floor, '']
        flats.append(result)
        count += 1
else:
    print(f'Ошибка: {response.status_code}')


time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
