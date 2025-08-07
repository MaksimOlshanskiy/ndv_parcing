import os

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
import time


# --- Функции ---

def parse_flat_area(link):
    try:
        resp = requests.get(link, headers=headers, cookies=cookies)
        if resp.status_code != 200:
            print(f"Не удалось загрузить страницу квартиры: {link}")
            return None

        soup = BeautifulSoup(resp.text, 'html.parser')
        area_tag = soup.find('div', class_='flat-detail-plan-square')
        if area_tag:
            area_text = area_tag.get_text(strip=True).split(' ')[0].replace(',', '.')
            return float(area_text)
        return None
    except Exception as e:
        print(f"Ошибка при парсинге площади: {e}")
        return None


def parse_rigahills_flats(page=1):
    params = {
        'PAGEN_1': page,
        'otdelka': 'y',
        'ajax': 'Y',
    }

    try:
        response = requests.get(
            'https://rigahills.ru/flats/list/',
            params=params,
            cookies=cookies,
            headers=headers
        )

        if response.status_code != 200:
            print(f"Ошибка запроса: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        flat_items = soup.find_all('div', class_='flats-item')
        flats_data = []

        for item in flat_items:
            flat_data = {}
            flat_data['type'] = item.find('div', class_='flats-item-name').get_text(strip=True)
            if flat_data['type'] == 'Студия':
                flat_data['rooms'] = 'Студия'
                flat_data['type'] = 'Квартира'
            elif flat_data['type'] == 'Однокомнатная квартира':
                flat_data['rooms'] = '1'
                flat_data['type'] = 'Квартира'
            elif flat_data['type'] == 'Двухкомнатная квартира':
                flat_data['rooms'] = '2'
                flat_data['type'] = 'Квартира'
            elif flat_data['type'] == 'Трехкомнатная квартира':
                flat_data['rooms'] = '3'
                flat_data['type'] = 'Квартира'
            elif flat_data['type'] == 'Четырехкомнатная квартира':
                flat_data['rooms'] = '4'
                flat_data['type'] = 'Квартира'
            elif flat_data['type'] == '2-евро квартира':
                flat_data['rooms'] = '2Е'
                flat_data['type'] = 'Квартира'
            elif flat_data['type'] == '3-евро квартира':
                flat_data['rooms'] = '3Е'
                flat_data['type'] = 'Квартира'

            price_discount = item.find('div', class_='price-discount')
            price_main = item.find('div', class_='price-main')

            flat_data['old_price'] = int(price_main.get_text(strip=True).replace(' ', '')) if price_main else None
            flat_data['price'] = int(price_discount.get_text(strip=True).replace(' ', '')) if price_discount else None

            if flat_data['old_price'] == flat_data['price']:
                flat_data['price'] = None

            img = item.find('img')
            if img and 'src' in img.attrs:
                img_src = img['src']
                filename = img_src.split('/')[-1]
                match = re.match(r'k(\d+)_s(\d+)_f(\d+)_r(\d+)', filename)
                if match:
                    flat_data['korpus'] = int(match.group(1))
                    flat_data['section'] = int(match.group(2))
                    flat_data['floor'] = int(match.group(3))

            link_tag = item.find('a', href=True)
            if link_tag:
                flat_data['link'] = 'https://rigahills.ru' + link_tag['href']

            flats_data.append(flat_data)

        return flats_data

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def parse_all_flats():
    base_url = "https://rigahills.ru/flats/list/"
    all_flats = []
    page = 1

    while True:
        print(f"Обрабатываю страницу {page}...")
        flats = parse_rigahills_flats(page)

        if not flats:
            break

        all_flats.extend(flats)

        soup = BeautifulSoup(requests.get(
            base_url,
            params={'filter': 'y', 'PAGEN_1': page},
            headers=headers,
            cookies=cookies
        ).text, 'html.parser')

        next_page = soup.find('a', class_='ix-show-more-btn')
        if not next_page:
            break

        page += 1

    return all_flats


# --- Cookies и headers ---

cookies = {
    'SCBFormsAlreadyPulled': 'true',
    'SCBFormsAlreadyPulled': 'true',
    '_ym_uid': '174360073469485371',
    '_ym_d': '1743600734',
    'BX_USER_ID': 'c3c0769764c13959e15059f6700f7e1e',
    '_ct': '2600000000174411589',
    'scbsid_old': '2796070936',
    '_ga': 'GA1.1.188716588.1748337937',
    '_ct_client_global_id': '8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4',
    'SCBnotShow': '-1',
    'PHPSESSID': 'fHWvagZTiK8wVzgijicVlTS4CGv7GK5Q',
    '_ym_isad': '1',
    'cted': 'modId%3Dm32s11lc%3Bclient_id%3D188716588.1748337937%3Bya_client_id%3D174360073469485371',
    '_ym_visorc': 'w',
    '_ct_ids': 'm32s11lc%3A63521%3A268294842',
    '_ct_session_id': '268294842',
    '_ct_site_id': '63521',
    'sma_session_id': '2341182289',
    'SCBfrom': '',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%22408b57183b182c79d2b9a0b3fa0d260b%22%2C%22be3e67a53916489460608b992809da55%22%2C%22ecfc7f3c204692d576ab5de3d3ac35c6%22%5D',
    'SCBstart': '1751033114120',
    '_ga_8QHK2T2PDM': 'GS2.1.s1751033113$o4$g1$t1751033285$j59$l0$h773512356',
    'call_s': '___m32s11lc.1751035085.268294842.357572:1011886|2___',
    'sma_index_activity': '7163',
    'SCBindexAct': '1294',
}

headers = {
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://rigahills.ru/flats/list/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'SCBFormsAlreadyPulled=true; SCBFormsAlreadyPulled=true; _ym_uid=174360073469485371; _ym_d=1743600734; BX_USER_ID=c3c0769764c13959e15059f6700f7e1e; _ct=2600000000174411589; scbsid_old=2796070936; _ga=GA1.1.188716588.1748337937; _ct_client_global_id=8ca69651-7fe7-51a0-a8bb-a3b89b29cfd4; SCBnotShow=-1; PHPSESSID=fHWvagZTiK8wVzgijicVlTS4CGv7GK5Q; _ym_isad=1; cted=modId%3Dm32s11lc%3Bclient_id%3D188716588.1748337937%3Bya_client_id%3D174360073469485371; _ym_visorc=w; _ct_ids=m32s11lc%3A63521%3A268294842; _ct_session_id=268294842; _ct_site_id=63521; sma_session_id=2341182289; SCBfrom=; SCBporogAct=5000; smFpId_old_values=%5B%22408b57183b182c79d2b9a0b3fa0d260b%22%2C%22be3e67a53916489460608b992809da55%22%2C%22ecfc7f3c204692d576ab5de3d3ac35c6%22%5D; SCBstart=1751033114120; _ga_8QHK2T2PDM=GS2.1.s1751033113$o4$g1$t1751033285$j59$l0$h773512356; call_s=___m32s11lc.1751035085.268294842.357572:1011886|2___; sma_index_activity=7163; SCBindexAct=1294',
}

# --- Точка входа ---

if __name__ == "__main__":
    all_flats = parse_all_flats()
    if all_flats:
        print(f"Всего найдено {len(all_flats)} квартир")

        for i, flat in enumerate(all_flats, 1):
            if flat.get('link'):
                print(f"[{i}/{len(all_flats)}] Парсинг площади по ссылке...")
                flat['area'] = parse_flat_area(flat['link'])
                time.sleep(0.05)

        current_date = datetime.today().date()
        formatted_flats = []

        for flat in all_flats:
            formatted = {
                'Дата обновления': current_date,
                'Название проекта': 'Riga Hills',
                'на англ': '',
                'промзона': '',
                'Местоположение': '',
                'Метро': '',
                'Расстояние до метро, км': '',
                'Время до метро, мин': '',
                'МЦК/МЦД/БКЛ': '',
                'Расстояние до МЦК/МЦД, км': '',
                'Время до МЦК/МЦД, мин': '',
                'БКЛ': '',
                'Расстояние до БКЛ, км': '',
                'Время до БКЛ, мин': '',
                'статус': '',
                'старт': '',
                'Комментарий': '',
                'Девелопер': 'Юнион',
                'Округ': '',
                'Район': '',
                'Адрес': '',
                'Эскроу': '',
                'Корпус': flat.get('korpus'),
                'Конструктив': '',
                'Класс': '',
                'Срок сдачи': '',
                'Старый срок сдачи': '',
                'Стадия строительной готовности': '',
                'Договор': '',
                'Тип помещения': flat.get('type'),
                'Отделка': 'Предчистовая',
                'Кол-во комнат': flat.get('rooms'),
                'Площадь, кв.м': flat.get('area'),
                'Цена кв.м, руб.': '',
                'Цена лота, руб.': flat.get('old_price'),
                'Скидка,% ': '',
                'Цена кв.м со ск, руб.': '',
                'Цена лота со ск, руб.': flat.get('price'),
                'секция': flat.get('section'),
                'этаж': flat.get('floor'),
                'номер': ''
            }

            formatted_flats.append(formatted)

        save_flats_to_excel(formatted_flats, 'Рига whitebox', 'Юнион')
    else:
        print("Не удалось получить данные о квартирах")
