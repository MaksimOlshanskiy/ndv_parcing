import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver



headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://nice-loft.ru/search-lot?priceStart=6&priceEnd=23&squareStart=16&squareEnd=106',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-xsrf-token': 'eyJpdiI6InFFa2J1aVBVMllST1BZb0o4K1N2N3c9PSIsInZhbHVlIjoiSDUwcFpSdGcrMGFlSDRCRFRza1A3WVB2eFZOMG85Y3lsZ0c0bTV3enk3SmdaWHVDb21LOGFIQ3NLSU5CMmd3ZUUyN2xlRm5qSEkvOGhXWUVKSHNVZ0IrR0Y1cjc0b21hTktkQzlIT2VsaHkybzFudVl2YmgvdDh0WDhrYmVUaVUiLCJtYWMiOiI4MWE5ZTQxODc5NmM3MGQ0OGI1OTJhYzUxZWU2OWEyZmY1ZDFhMjM3NjAwNGZhY2EzYmZkMjM5MjJlMzgxMTEyIn0=',
    # 'cookie': '_ym_uid=1741358700301867031; _ym_d=1741358700; tmr_lvid=7eba1edd72b4140ebc326f27129cc0b9; tmr_lvidTS=1741358700073; _ct=1800000000438576885; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; cted=modId%3Divnmp5ss%3Bya_client_id%3D1741358700301867031; _ym_isad=2; _ym_visorc=w; scbsid_old=2725937795; _ct_ids=ivnmp5ss%3A45670%3A661050033; _ct_session_id=661050033; _ct_site_id=45670; WhiteCallback_visitorId=19425354114; WhiteCallback_visit=30897911865; WhiteSaas_uniqueLead=no; domain_sid=X6Yu_XrBUjJHD89FeWA5p%3A1742561962453; sma_session_id=2232477207; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; smFpId_old_values=%5B%22ec8200dec572541a6b5585a0e4760a2b%22%5D; SCBstart=1742561963281; SCBporogAct=5000; SCBFormsAlreadyPulled=true; call_s=___ivnmp5ss.1742563771.661050033.200781:677691|2___; tmr_detect=0%7C1742561975678; WhiteCallback_timeAll=19; WhiteCallback_timePage=19; WhiteCallback_openedPages=VNMrx; XSRF-TOKEN=eyJpdiI6InFFa2J1aVBVMllST1BZb0o4K1N2N3c9PSIsInZhbHVlIjoiSDUwcFpSdGcrMGFlSDRCRFRza1A3WVB2eFZOMG85Y3lsZ0c0bTV3enk3SmdaWHVDb21LOGFIQ3NLSU5CMmd3ZUUyN2xlRm5qSEkvOGhXWUVKSHNVZ0IrR0Y1cjc0b21hTktkQzlIT2VsaHkybzFudVl2YmgvdDh0WDhrYmVUaVUiLCJtYWMiOiI4MWE5ZTQxODc5NmM3MGQ0OGI1OTJhYzUxZWU2OWEyZmY1ZDFhMjM3NjAwNGZhY2EzYmZkMjM5MjJlMzgxMTEyIn0%3D; niceloft_session=eyJpdiI6IjZWanlNNk16aWpsTnR0RDVpUnlsZnc9PSIsInZhbHVlIjoidFJVNmFDWTcvQnpTSmRtYnhqSDBKa2Q2aE5xWjBBaS9xMmFnbTNRQzVQdWRHODZDVDRVandQc1hjRGwwWmtvN3ZUdm9lcTZnUjA4MGZ4QnZZaHB4UHliVm0wbkNSVkpRbGJiRzRIVmRyUW5iUSs4YzlBV3dQMzFSbmpzUnljZkYiLCJtYWMiOiJhN2M3MmU0NmMxYTgzYzhlYmE5ZGZmYzM0MjMwZGI1YTdmYzg4MjU5MjM5ZjgwMTNkMGE2Y2FkNjUyYjhhMzE5In0%3D; activity=6|20; sma_index_activity=724; SCBindexAct=524',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

web_site = f'https://willtowers.ru/params/'
driver = webdriver.Chrome()
driver.get(url=web_site)
page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
soup = BeautifulSoup(page_content, 'html.parser')

time.sleep(2)

flats_soup = soup.find_all('div', class_="params-body__item-info")

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



for y in range(0, len(flats_soup)):



    td_elements = flats_soup[y].find_all('span')



    url = ''

    date = datetime.date.today()
    project = "Вилл Тауэрс"

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
    developer = "Центр-Инвест"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    korpus = td_elements[2].text.strip()
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    type = 'Квартиры'
    finish_type = "Без отделки"
    if td_elements[4].text.strip() == 'c':
        room_count = 0
    else:
        room_count = int(td_elements[4].text.strip())
    area = float(td_elements[5].text.strip())
    price_per_metr = ''
    old_price = int(td_elements[7].text.strip().replace(' ', ''))

    discount = ''
    price_per_metr_new = ''
    price = int(td_elements[6].find('div', class_='params-body__price-main').text.replace(" ", ''))
    section = ''
    floor = int(td_elements[3].text.strip())
    flat_number = int(td_elements[1].text.strip())

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
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)