import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all
import requests

cookies = {
    '__ddg1_': 'eLsCydsqsGpPEhS31XU6',
    'csrftoken': 'fCcC5D15c7f38F210ba529ec745F36B54617570937bdBf519E82733a3934685b',
    '__ddg9_': '89.188.120.54',
    '_ym_uid': '1742303092473237501',
    '_ym_d': '1742303092',
    '_ym_isad': '1',
    '_ct_ids': '61oc84v1%3A51907%3A776187406',
    '_ct_session_id': '776187406',
    '_ct_site_id': '51907',
    '_ct': '2100000000435866092',
    '_ga': 'GA1.1.4313349.1742303092',
    '_ct_client_global_id': 'b7bf8ff5-0827-5c41-830e-bad9491c1c5e',
    '_ym_visorc': 'w',
    'cted': 'modId%3D61oc84v1%3Bya_client_id%3D1742303092473237501%3Bclient_id%3D4313349.1742303092',
    'call_s': '___61oc84v1.1742304895.776187406.395799:1116273|2___',
    '__ddg10_': '1742303141',
    '__ddg8_': 'di7OrzyfWFdxaCaD',
    '_ga_WR7XBQW1L2': 'GS1.1.1742303091.1.1.1742303141.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Basic c3RtaWNoYWVsLWRldjo2M2s5VFlmSkRAJiNabjc=',
    'priority': 'u=1, i',
    'referer': 'https://stmichael.ru/lots?type=apartments&price_max=183&price_min=13',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-csrftoken': '871b65204Fa4c3371b479aABe0D31299691539BB25862dca0649e956C0e42A8b',
    # 'cookie': '__ddg9_=91.108.227.31; __ddg1_=7laYcMGvYQpJNyjKljT6; csrftoken=871b65204Fa4c3371b479aABe0D31299691539BB25862dca0649e956C0e42A8b; _ym_uid=175334298987968816; _ym_d=1753342989; _ym_isad=1; _ym_visorc=w; cted=modId%3D61oc84v1%3Bya_client_id%3D175334298987968816; _ct_ids=61oc84v1%3A51907%3A843394531; _ct_session_id=843394531; _ct_site_id=51907; call_s=___61oc84v1.1753344790.843394531.395799:1116274|2___; _ct=2100000000480128785; _ct_client_global_id=8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4; scbsid_old=2796070936; sma_session_id=2368633660; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%22a932251185d3bf41fcd7e2656de279f5%22%5D; SCBporogAct=5000; SCBstart=1753342999468; SCBFormsAlreadyPulled=true; __ddg10_=1753343016; __ddg8_=GlmhplFu5Hl7Gnqm; sma_index_activity=1235; SCBindexAct=1185',
}

params = {
    'offset': '0',
    'limit': '20',
    'price_min': '13',
    'price_max': '183',
}

url = 'https://stmichael.ru/api/apartments/'

flats = []
count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()
        items = item.get("results", [])

        for i in items:
            if i['status']=='BOOKED':
                continue
            date = datetime.date.today()
            project = i["project_name"]
            status = ''
            developer = 'St. Michael'
            district = ''
            korpus = i["building_number"]
            room_count = i["rooms"]
            if room_count==0:
                room_count='студия'
            type = i["type"]
            if type == 'flat':
                type = 'Квартира'
            else:
                type = 'Апартаменты'
            try:
                finish_type = i["finishing_name"]
            except KeyError:
                finish_type = ''
            area = float(i["area"])
            old_price = round(float(i["original_price"]))
            discount = ''
            price = round(float(i["price"]))
            section = ''
            floor = i["floor_number"]

            srok_sdachi = ''

            print(
                f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '',
                      '', '', status, '', '', developer, '', district, '', '', korpus, '', '', srok_sdachi, '',
                      '', '', type, finish_type, room_count, area, '', old_price, discount, '', price,
                      section, floor, '']
            flats.append(result)
            count += 1

        # Проверяем, есть ли следующая страница
        next_url = item.get("next")
        if next_url:
            url = next_url  # Переходим на следующую страницу
            params = {}  # Очищаем параметры, так как URL следующей страницы уже содержит их
        else:
            break  # Если следующей страницы нет, выходим из цикла
    else:
        print(f'Ошибка: {response.status_code}')
        break

    time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
