import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver



import requests

cookies = {
    'spid': '1742911906806_a6af7aafd6d36f3da75ead86dab92db1_il331eo3p5486g2p',
    'scbsid_old': '2746015342',
    'tmr_lvid': 'b846073c297ab0f227a0beeff859cbb0',
    'tmr_lvidTS': '1742911907765',
    '_ym_uid': '1742911908725726256',
    '_ym_d': '1742911908',
    '_ga': 'GA1.1.2011517384.1742911908',
    'sma_session_id': '2237662266',
    '_ym_isad': '2',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    'domain_sid': '_s31UW6Md684Fha7bJKQS%3A1742911908297',
    'cookie_consent': 'accepted',
    'SCBporogAct': '5000',
    'spsc': '1742971163602_e4b934355d5e238763fc5c94a895c8ee_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5',
    'PHPSESSID': '7nQ38a9oqA5YE6ye0iPiviXk1D1A3xcC',
    'DOMAIN': 'msk',
    'SCBstart': '1742971187157',
    '_ym_visorc': 'b',
    'backLink': '%2Fmsk%2Fkvartiry-v-novostroikah%2F%3Flast_delivery%3D30%26price%255Bmin%255D%3D7.1%26price%255Bmax%255D%3D26.3%26price_range%255Bmin%255D%3D7.1%26price_range%255Bmax%255D%3D26.3%26obj%255B%255D%3D52%26obj%255B%255D%3D52%26area%255Bmin%255D%3D20%26area%255Bmax%255D%3D65%26area_range%255Bmin%255D%3D20.0%26area_range%255Bmax%255D%3D65.0%26floor%255Bmin%255D%3D2%26floor%255Bmax%255D%3D24%26floor_range%255Bmin%255D%3D2%26floor_range%255Bmax%255D%3D24',
    '_ga_FNTNBKC2H2': 'GS1.1.1742971180.3.1.1742971189.0.0.0',
    '_cmg_csstA05bX': '1742971190',
    '_comagic_idA05bX': '10483368114.14611733089.1742971190',
    'number_phone_site': '74950211258',
    'number_phone_site_arr': '%5B%2274950211258%22%5D',
    'tmr_detect': '0%7C1742971192027',
    'sma_index_activity': '3085',
    'SCBindexAct': '2636',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lsr.ru',
    'Referer': 'https://www.lsr.ru/msk/kvartiry-v-novostroikah/?last_delivery=30&price%5Bmin%5D=7.1&price%5Bmax%5D=26.3&price_range%5Bmin%5D=7.1&price_range%5Bmax%5D=26.3&obj%5B%5D=52&obj%5B%5D=52&area%5Bmin%5D=20&area%5Bmax%5D=65&area_range%5Bmin%5D=20.0&area_range%5Bmax%5D=65.0&floor%5Bmin%5D=2&floor%5Bmax%5D=24&floor_range%5Bmin%5D=2&floor_range%5Bmax%5D=24',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'spid=1742911906806_a6af7aafd6d36f3da75ead86dab92db1_il331eo3p5486g2p; scbsid_old=2746015342; tmr_lvid=b846073c297ab0f227a0beeff859cbb0; tmr_lvidTS=1742911907765; _ym_uid=1742911908725726256; _ym_d=1742911908; _ga=GA1.1.2011517384.1742911908; sma_session_id=2237662266; _ym_isad=2; SCBnotShow=-1; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; domain_sid=_s31UW6Md684Fha7bJKQS%3A1742911908297; cookie_consent=accepted; SCBporogAct=5000; spsc=1742971163602_e4b934355d5e238763fc5c94a895c8ee_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5; PHPSESSID=7nQ38a9oqA5YE6ye0iPiviXk1D1A3xcC; DOMAIN=msk; SCBstart=1742971187157; _ym_visorc=b; backLink=%2Fmsk%2Fkvartiry-v-novostroikah%2F%3Flast_delivery%3D30%26price%255Bmin%255D%3D7.1%26price%255Bmax%255D%3D26.3%26price_range%255Bmin%255D%3D7.1%26price_range%255Bmax%255D%3D26.3%26obj%255B%255D%3D52%26obj%255B%255D%3D52%26area%255Bmin%255D%3D20%26area%255Bmax%255D%3D65%26area_range%255Bmin%255D%3D20.0%26area_range%255Bmax%255D%3D65.0%26floor%255Bmin%255D%3D2%26floor%255Bmax%255D%3D24%26floor_range%255Bmin%255D%3D2%26floor_range%255Bmax%255D%3D24; _ga_FNTNBKC2H2=GS1.1.1742971180.3.1.1742971189.0.0.0; _cmg_csstA05bX=1742971190; _comagic_idA05bX=10483368114.14611733089.1742971190; number_phone_site=74950211258; number_phone_site_arr=%5B%2274950211258%22%5D; tmr_detect=0%7C1742971192027; sma_index_activity=3085; SCBindexAct=2636',
}


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
page_counter = 1

while True:


    data = f'last_delivery=30&price%5Bmin%5D=8.7&price%5Bmax%5D=40.7&price_range%5Bmin%5D=8.7&price_range%5Bmax%5D=40.7&obj%5B%5D=152&obj%5B%5D=152&area%5Bmin%5D=20&area%5Bmax%5D=89&area_range%5Bmin%5D=20.0&area_range%5Bmax%5D=89.0&floor%5Bmin%5D=2&floor%5Bmax%5D=23&floor_range%5Bmin%5D=2&floor_range%5Bmax%5D=23&ob[page]={str(page_counter)}&ob[sort]=price&ob[order]=asc&group[t]=false&ob[id]=152&object=152&a=types&ok=7nQ38a9oqA5YE6ye0iPiviXk1D1A3xcC'

    response = requests.post('https://www.lsr.ru/ajax/search/msk/', cookies=cookies, headers=headers, data=data)
    print(response.status_code)
    items = response.json()['html']
    soup = BeautifulSoup(items, 'html.parser')
    flats_soup = soup.find_all('div', class_=["listingCard listingCard--isFlat", "listingCard listingCard--isFlat listingCard--isPromotion"])
    for i in flats_soup:

        url = ''

        date = datetime.date.today()
        project = ("ЖК Парксайд")

        english = ''
        promzona = ''
        mestopolozhenie = ''
        subway = ''
        distance_to_subway = ''
        time_to_subway = ''
        mck = ''
        distance_to_mck = ''
        time_to_mck = ''
        bkl = ''
        distance_to_bkl = ''
        time_to_bkl = ''
        status = ''
        start = ''
        comment = ''
        developer = "ЛСР"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        all_tags = i.find_all('div', class_='tag tag--isSmall')
        korpus = int(i.find('div', class_= 'listingCard__label').text.strip().split()[1].replace(",", ''))
        konstruktiv = ''
        klass = ''
        if len(all_tags) == 3:
            srok_sdachi = all_tags[0].text.strip()
            if all_tags[2].text.strip() == "С меблировкой":
                finish_type = f"{all_tags[1].text.strip()}, С меблировкой"
            else:
                finish_type = all_tags[1].text.strip()
        else:
            srok_sdachi = ''
            if all_tags[1].text.strip() == "С меблировкой":
                finish_type = f"{all_tags[0].text.strip()}, С меблировкой"
            else:
                finish_type = all_tags[0].text.strip()

        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'

        if i.find('span', class_="h4").text.strip().split()[0] == "Студия":
            room_count = 0
        else:
            room_count = extract_digits_or_original(i.find('span', class_= "h4").text.strip().split()[0])
        area = float(i.find('span', class_='h4 isColorSilverChalice isTextNoWrap').text.strip().split(' ')[0])
        price_per_metr = ''
        old_price = ''

        discount = ''
        price_per_metr_new = ''
        price = extract_digits_or_original(i.find('span', class_= 'h4 isHiddenInGrid').text)
        section = ''
        try:
            floor = int(i.find('div', class_= 'listingCard__label').text.strip().split()[5])
        except:
            floor = i.find('div', class_='listingCard__label').text.strip().split()[5]
        flat_number = ''

        print(
            f"{project}, квартира {flat_number}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not flats_soup:
        break

    print('--------------------------------------------------------------------------------')

    page_counter += 1
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


df = pd.DataFrame(flats, columns=['Дата обновления',
                              'Название проекта',
                              'на англ',
                              'промзона',
                              'Местоположение',
                              'Метро',
                              'Расстояние до метро, км',
                              'Время до метро, мин',
                              'МЦК/МЦД/БКЛ',
                              'Расстояние до МЦК/МЦД, км',
                              'Время до МЦК/МЦД, мин',
                              'БКЛ',
                              'Расстояние до БКЛ, км',
                              'Время до БКЛ, мин',
                              'статус',
                              'старт',
                              'Комментарий',
                              'Девелопер',
                              'Округ',
                              'Район',
                              'Адрес',
                              'Эскроу',
                              'Корпус',
                              'Конструктив',
                              'Класс',
                              'Срок сдачи',
                              'Старый срок сдачи',
                              'Стадия строительной готовности',
                              'Договор',
                              'Тип помещения',
                              'Отделка',
                              'Кол-во комнат',
                              'Площадь, кв.м',
                              'Цена кв.м, руб.',
                              'Цена лота, руб.',
                              'Скидка,%',
                              'Цена кв.м со ск, руб.',
                              'Цена лота со ск, руб.',
                              'секция',
                              'этаж',
                              'номер'])

current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ЛСР"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)