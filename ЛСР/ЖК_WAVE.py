import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests
from functions import save_flats_to_excel

cookies = {
    'tmr_lvid': 'b846073c297ab0f227a0beeff859cbb0',
    'tmr_lvidTS': '1742911907765',
    '_ym_uid': '1742911908725726256',
    '_ym_d': '1742911908',
    '_ga_09LLC3Q7HR': 'GS1.2.1742978855.1.0.1742978855.0.0.0',
    '_ga': 'GA1.1.2011517384.1742911908',
    '_cmg_csst7Pddw': '1745507826',
    '_comagic_id7Pddw': '10313394311.14534335851.1745507826',
    'scbsid_old': '2746015342',
    'cookie_consent': 'accepted',
    'spid': '1750341260887_e8966188f22fa893f1c6b051cebd99a2_141i7jfp6fqw39e6',
    '_ga_FNTNBKC2H2': 'GS2.1.s1750930106$o32$g0$t1750930106$j60$l0$h0',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22b0d44eece823d71c253568fc397e79de%22%2C%22f0a18207107a745e280d9357abcbd51d%22%2C%22d3b2a7a62667c988953915d7d3b4139e%22%2C%22ca505640ddf99ec8d4755fa1299dcd1a%22%2C%22d9eadf726ef363c2da5f2fae87307f58%22%2C%22a7ea49fc46c5a5b146d731ca169a44ef%22%5D',
    'number_phone_site': '74950195932',
    'PHPSESSID': '9I6cUsbCaYXxEGNhbfAopnQOP0VhDSVT',
    '_ym_isad': '2',
    'domain_sid': '_s31UW6Md684Fha7bJKQS%3A1753949604008',
    'number_phone_site_arr': '%5B%2274950195932%22%5D',
    'SCBporogAct': '5000',
    'spsc': '1753958548021_40f81be9ad755fd9cf6149a54670a096_i4iKRQbkMcJUe7njxsBLkMHbkgY4wDDubwCgXbidZGMZ',
    'DOMAIN': 'msk',
    'backLink': '%2Fmsk%2Fkvartiry-v-novostroikah%2F%3Fprice%255Bmin%255D%3D8.9%26price%255Bmax%255D%3D78.7%26price_range%255Bmin%255D%3D8.9%26price_range%255Bmax%255D%3D78.7%26last_delivery%3D32%26obj%255B%255D%3D202%26obj%255B%255D%3D202%26area%255Bmin%255D%3D19%26area%255Bmax%255D%3D108%26area_range%255Bmin%255D%3D19.0%26area_range%255Bmax%255D%3D108.0%26floor%255Bmin%255D%3D2%26floor%255Bmax%255D%3D52%26floor_range%255Bmin%255D%3D2%26floor_range%255Bmax%255D%3D52',
    '_ym_visorc': 'b',
    '_cmg_csstA05bX': '1753958553',
    '_comagic_idA05bX': '11379380619.15618176149.1753958552',
    'tmr_detect': '0%7C1753958554137',
    'sma_session_id': '2376713573',
    'SCBfrom': 'https%3A%2F%2Fwww.lsr.ru%2Fmsk%2Fzhilye-kompleksy%2Fwave%2F',
    'SCBindexAct': '4812',
    'sma_index_activity': '505',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lsr.ru',
    'Referer': 'https://www.lsr.ru/msk/kvartiry-v-novostroikah/?price%5Bmin%5D=8.9&price%5Bmax%5D=78.7&price_range%5Bmin%5D=8.9&price_range%5Bmax%5D=78.7&last_delivery=32&obj%5B%5D=202&obj%5B%5D=202&area%5Bmin%5D=19&area%5Bmax%5D=108&area_range%5Bmin%5D=19.0&area_range%5Bmax%5D=108.0&floor%5Bmin%5D=2&floor%5Bmax%5D=52&floor_range%5Bmin%5D=2&floor_range%5Bmax%5D=52',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'tmr_lvid=b846073c297ab0f227a0beeff859cbb0; tmr_lvidTS=1742911907765; _ym_uid=1742911908725726256; _ym_d=1742911908; _ga_09LLC3Q7HR=GS1.2.1742978855.1.0.1742978855.0.0.0; _ga=GA1.1.2011517384.1742911908; _cmg_csst7Pddw=1745507826; _comagic_id7Pddw=10313394311.14534335851.1745507826; scbsid_old=2746015342; cookie_consent=accepted; spid=1750341260887_e8966188f22fa893f1c6b051cebd99a2_141i7jfp6fqw39e6; _ga_FNTNBKC2H2=GS2.1.s1750930106$o32$g0$t1750930106$j60$l0$h0; SCBnotShow=-1; smFpId_old_values=%5B%22b0d44eece823d71c253568fc397e79de%22%2C%22f0a18207107a745e280d9357abcbd51d%22%2C%22d3b2a7a62667c988953915d7d3b4139e%22%2C%22ca505640ddf99ec8d4755fa1299dcd1a%22%2C%22d9eadf726ef363c2da5f2fae87307f58%22%2C%22a7ea49fc46c5a5b146d731ca169a44ef%22%5D; number_phone_site=74950195932; PHPSESSID=9I6cUsbCaYXxEGNhbfAopnQOP0VhDSVT; _ym_isad=2; domain_sid=_s31UW6Md684Fha7bJKQS%3A1753949604008; number_phone_site_arr=%5B%2274950195932%22%5D; SCBporogAct=5000; spsc=1753958548021_40f81be9ad755fd9cf6149a54670a096_i4iKRQbkMcJUe7njxsBLkMHbkgY4wDDubwCgXbidZGMZ; DOMAIN=msk; backLink=%2Fmsk%2Fkvartiry-v-novostroikah%2F%3Fprice%255Bmin%255D%3D8.9%26price%255Bmax%255D%3D78.7%26price_range%255Bmin%255D%3D8.9%26price_range%255Bmax%255D%3D78.7%26last_delivery%3D32%26obj%255B%255D%3D202%26obj%255B%255D%3D202%26area%255Bmin%255D%3D19%26area%255Bmax%255D%3D108%26area_range%255Bmin%255D%3D19.0%26area_range%255Bmax%255D%3D108.0%26floor%255Bmin%255D%3D2%26floor%255Bmax%255D%3D52%26floor_range%255Bmin%255D%3D2%26floor_range%255Bmax%255D%3D52; _ym_visorc=b; _cmg_csstA05bX=1753958553; _comagic_idA05bX=11379380619.15618176149.1753958552; tmr_detect=0%7C1753958554137; sma_session_id=2376713573; SCBfrom=https%3A%2F%2Fwww.lsr.ru%2Fmsk%2Fzhilye-kompleksy%2Fwave%2F; SCBindexAct=4812; sma_index_activity=505',
}



if __name__ == "__main__":

    data = {
  'price[min]': '1',
  'price[max]': '99.1',
  'price_range[min]': '1.7',
  'price_range[max]': '99.1',
  'last_delivery': '32',
  'obj[]': ['202', '202'],
  'area[min]': '1',
  'area[max]': '1089',
  'area_range[min]': '1.0',
  'area_range[max]': '1089.0',
  'floor[min]': '1',
  'floor[max]': '99',
  'floor_range[min]': '1',
  'floor_range[max]': '99',
  'ob[page]': '2',
  'ob[sort]': 'price',
  'ob[order]': 'asc',
  'group[t]': 'false',
  'ob[id]': '202',
  'object': '202',
  'a': 'types',
  'ok': '9I6cUsbCaYXxEGNhbfAopnQOP0VhDSVT'
}


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
page_counter = 1

while True:

    response = requests.post('https://www.lsr.ru/ajax/search/msk/', cookies=cookies, headers=headers, data=data)
    print(response.status_code)
    items = response.json()
    soup = BeautifulSoup(items['html'], 'html.parser')
    flats_soup = soup.find_all('div', class_=["listingCard listingCard--isFlat", "listingCard--isPromotion"])
    soup2 = BeautifulSoup(items['object_link'], 'html.parser')
    flats_soup2 = soup2.find('a')

    for i in flats_soup:

        url = ''
        date = datetime.date.today()
        project = flats_soup2.text.strip().replace('в ЖК ', '')
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
        try:
            korpus = int(i.find('span', class_= 'label l3').text.strip().split()[1].replace(",", ''))
        except ValueError:
            korpus = i.find('span', class_= 'label l3').text.strip().replace('Wave, ', '')
        konstruktiv = ''
        klass = ''
        if len(all_tags) == 3:
            srok_sdachi = all_tags[0].text.strip()
            if all_tags[2].text.strip() == "С меблировкой":
                finish_type = f"{all_tags[1].text.strip()} и доп опциями"
            else:
                finish_type = all_tags[1].text.strip()
        else:
            srok_sdachi = ''
            if all_tags[1].text.strip() == "С меблировкой":
                finish_type = f"{all_tags[0].text.strip()} и доп опциями"
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
        old_price = extract_digits_or_original(i.find('span', class_= 'h4 isHiddenInGrid').text)
        discount = ''
        price_per_metr_new = ''
        price = ''
        section = ''
        try:
            floor = int(i.find('div', class_= 'listingCard__label').text.strip().split()[4])
        except:
            floor = i.find('div', class_='listingCard__label').text.strip().split()[4]
        flat_number = ''

        print(
            f"{project}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
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

    data['ob[page]'] = str(int(data['ob[page]']) + 1)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)