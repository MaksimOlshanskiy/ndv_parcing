import datetime
import time
import random
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

'''
Иногда надо менять base_url и проверять ссылку в headers и данные в params
'''

# Настройки запроса
base_url =     'https://afi-park.ru/_next/data/qHSv8pGINzwrfEs7NqRbe/param.json'
cookies = {
    'scbsid_old': '2796070936',
    '_ym_uid': '1745310982287293563',
    '_ym_d': '1745310982',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    'fav': '[]',
    '_gid': 'GA1.2.1869136493.1750841467',
    '_gat_UA-233170057-1': '1',
    '_cmg_csst6BzgD': '1750841467',
    '_comagic_id6BzgD': '10688711056.14968917321.1750841466',
    'sma_session_id': '2338846633',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'SCBstart': '1750841468143',
    'smFpId_old_values': '%5B%2204b0ffbac42ccceb635ec5bff5b15618%22%2C%22408b57183b182c79d2b9a0b3fa0d260b%22%2C%22be3e67a53916489460608b992809da55%22%5D',
    '_ga': 'GA1.2.306144266.1745310982',
    'SCBporogAct': '5000',
    '_ga_WTP9H68PBV': 'GS2.1.s1750841466$o4$g1$t1750841473$j53$l0$h0',
    'SCBFormsAlreadyPulled': 'true',
    'sma_index_activity': '2181',
    'SCBindexAct': '1731',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://afi-park.ru/param?price_min=11.4&price_max=44',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'x-nextjs-data': '1',
    # 'cookie': 'scbsid_old=2796070936; _ym_uid=1745310982287293563; _ym_d=1745310982; fav=[]; _ym_isad=1; _ym_visorc=w; _ga=GA1.2.306144266.1745310982; _gid=GA1.2.1979708302.1748252266; _gat_UA-233170057-1=1; _cmg_csst6BzgD=1748252267; _comagic_id6BzgD=10502752376.14752746421.1748252269; sma_session_id=2306882647; SCBfrom=; smFpId_old_values=%5B%2204b0ffbac42ccceb635ec5bff5b15618%22%2C%22408b57183b182c79d2b9a0b3fa0d260b%22%5D; SCBnotShow=-1; SCBporogAct=5000; PHPSESSID=CZTKXdeyuDhKgmSlSajREa6mHCjUMzH6; SCBstart=1748252268029; _ga_WTP9H68PBV=GS2.1.s1748252265$o3$g1$t1748252290$j0$l0$h0; sma_index_activity=3973; SCBindexAct=4990',
}

project = "Сиреневый парк"
developer = "АФИ"
flats = []

try:
    response = requests.get(
        base_url,
        params={'price_min': '11.4', 'price_max': '44', },
        cookies=cookies,
        headers=headers,
    )
    response.raise_for_status()

    data = response.json()
    queries = data.get('pageProps', {}).get('initialState', {}).get('api', {}).get('queries', {})
    param_query_key = next((k for k in queries.keys() if 'getParam' in k), None)

    if not param_query_key:
        raise Exception("Не удалось найти данные о квартирах")

    items = queries[param_query_key].get('data', {}).get('list', [])

    # Обрабатываем квартиры
    count = 0
    for item in items:
        count += 1
        date = datetime.date.today()
        korpus = item.get('corpus', '')
        finish_type = item.get('decor', '')
        if finish_type == 'чистовая':
            finish_type = 'С отделкой'
        room_count = item.get('rooms', '')

        if room_count == 'С':
            room_count = 'студия'

        type = 'Квартира'
        area = item.get('square', '')
        old_price = item.get('price', '')
        price = item.get('price_discount', '')
        section = item.get('section', '')
        floor = item.get('floor', '')

        print(
            f"{count}, {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [
            date, project, '', '', '', '', '',
            '', '', '', '', '',
            '', '', '', '', '', developer, '', '',
            '', '', korpus, '', '', '', '',
            '', '', type, finish_type.capitalize(), room_count, area, '',
            old_price, '', '', price, section, floor, ''
        ]
        flats.append(result)

        time.sleep(0.05)

    save_flats_to_excel(flats, project, developer)

    print(f"Успешно сохранено {len(flats)} квартир")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к серверу: {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")

# Задержка перед завершением
time.sleep(random.uniform(10, 15))
