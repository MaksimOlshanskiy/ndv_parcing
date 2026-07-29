"""
Сначала обновляем куки
Затем меняем в params - complex_ids на нужный
Его можно найти в адресной строке нужного ЖК

Обращать внимание на код кнопки вперёд. Он иногда меняется.
"""



import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from functions import save_flats_to_excel

developer = ''
project = ''
area = ''

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

cookies = {
    'ns_session': '8d885eed-c151-4167-9919-8657ec697ffe',
    '_ym_uid': '1765012936500443323',
    '_ym_d': '1782939022',
    'logoSuffix': '',
    'iosAppLink': '',
    'showDddIntro': 'false',
    'dddIntroOnline': 'false',
    'showDddWidgets': 'true',
    'RETENTION_COOKIES_NAME': '73a09f72fd964582843061b4531b1749:PzMXzDiTZwMDclesDmpsDzCazRc',
    'sessionId': '12791819e59a41f69051746fca5dad7a:kEQkdePJp_BacogdDvlAn091-70',
    'UNIQ_SESSION_ID': 'd58e9846198b4c0289a92ac3432ed3b7:UMgljoWSM32ON1aIaU9IGAv1Sq8',
    '_sv': 'SV1.9d1bff91-155a-4ed9-8572-9e1d8eb6aebc.1782939008',
    'adtech_uid': 'c9082c41-db22-46c2-ad5a-794db0f6fa39%3Adomclick.ru',
    'top100_id': 't1.7711713.584217383.1782939023617',
    'tmr_lvid': '6509c7cbd63e89eea195eb14c34fbb17',
    'tmr_lvidTS': '1773855203088',
    'regionAlert': '1',
    'favoriteHintShowed': 'true',
    'canary-bind-id-16493': 'prev-1',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}',
    'qrator_jsr': 'v2.0.1785337027.269.05e47254hqdvF3r1|h8RwHcbefUTluKGw|3jPqlEP8K691c6a8Amvzs3wmDLpKUJHQe3jxF9sZMNtL3IODsVBLPLhPiHU+w/4MzhJbYVNCpQ3bf3BNl6nRmg==-u88XXm03Rwb9HAstFF7ptHbSIQc=-00',
    'qrator_jsid2': 'v2.0.1785337027.269.05e47254hqdvF3r1|CjvLd5kbEfTL0A7L|t0O/XWjM1OAwt8BqCqcThKXE1TwgqY+nLy7caJg+IluV5O/u0dVobuNpQQOaFqnT5co8sZTO3vs+sciIV5uTWriJHHnNEC/E6n6LxEchUPxqQ2m1b606RqHwlCGo0ZsVcHqaHKlXl1er8HxTjChedCAiqURTvPzuKIX1+9A8DUE=-x+E2wm1YHXgHV8uBcsVvZrUJLzo=',
    'canary-bind-id-16542': 'prev-1',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.9d1bff91-155a-4ed9-8572-9e1d8eb6aebc.1782939008.1785337030',
    '_sas': 'SV1.9d1bff91-155a-4ed9-8572-9e1d8eb6aebc.1782939008.1785337033',
    't3_sid_7711713': 's1.1016988686.1785337030788.1785337195914.7.7.2.1..',
    'tmr_reqNum': '457',
    't3_sid_7731951': 's1.270570886.1785337030781.1785337200765.6.19.2.1..',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://domclick.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=8d885eed-c151-4167-9919-8657ec697ffe; _ym_uid=1765012936500443323; _ym_d=1782939022; logoSuffix=; iosAppLink=; showDddIntro=false; dddIntroOnline=false; showDddWidgets=true; RETENTION_COOKIES_NAME=73a09f72fd964582843061b4531b1749:PzMXzDiTZwMDclesDmpsDzCazRc; sessionId=12791819e59a41f69051746fca5dad7a:kEQkdePJp_BacogdDvlAn091-70; UNIQ_SESSION_ID=d58e9846198b4c0289a92ac3432ed3b7:UMgljoWSM32ON1aIaU9IGAv1Sq8; _sv=SV1.9d1bff91-155a-4ed9-8572-9e1d8eb6aebc.1782939008; adtech_uid=c9082c41-db22-46c2-ad5a-794db0f6fa39%3Adomclick.ru; top100_id=t1.7711713.584217383.1782939023617; tmr_lvid=6509c7cbd63e89eea195eb14c34fbb17; tmr_lvidTS=1773855203088; regionAlert=1; favoriteHintShowed=true; canary-bind-id-16493=prev-1; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; qrator_jsr=v2.0.1785337027.269.05e47254hqdvF3r1|h8RwHcbefUTluKGw|3jPqlEP8K691c6a8Amvzs3wmDLpKUJHQe3jxF9sZMNtL3IODsVBLPLhPiHU+w/4MzhJbYVNCpQ3bf3BNl6nRmg==-u88XXm03Rwb9HAstFF7ptHbSIQc=-00; qrator_jsid2=v2.0.1785337027.269.05e47254hqdvF3r1|CjvLd5kbEfTL0A7L|t0O/XWjM1OAwt8BqCqcThKXE1TwgqY+nLy7caJg+IluV5O/u0dVobuNpQQOaFqnT5co8sZTO3vs+sciIV5uTWriJHHnNEC/E6n6LxEchUPxqQ2m1b606RqHwlCGo0ZsVcHqaHKlXl1er8HxTjChedCAiqURTvPzuKIX1+9A8DUE=-x+E2wm1YHXgHV8uBcsVvZrUJLzo=; canary-bind-id-16542=prev-1; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.9d1bff91-155a-4ed9-8572-9e1d8eb6aebc.1782939008.1785337030; _sas=SV1.9d1bff91-155a-4ed9-8572-9e1d8eb6aebc.1782939008.1785337033; t3_sid_7711713=s1.1016988686.1785337030788.1785337195914.7.7.2.1..; tmr_reqNum=457; t3_sid_7731951=s1.270570886.1785337030781.1785337200765.6.19.2.1..',
}


params = {
    'address': '1d1463ae-c80f-4d19-9331-a1b68a85b553',
    'limit': '20',
    'sort': 'qi',
    'sort_dir': 'desc',
    'deal_type': 'sale',
    'category': 'living',
    'offer_type': 'layout',
    'complex_ids': '112971',
    'complex_name': 'ЖК Радость',
    'from_developer': '1',
    'offset': '0'
}



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://bff-search-web.domclick.ru/api/offers/v1', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    items = response.json()['result']['items']

    for i in items:

        url = ""
        date = datetime.date.today()
        try:
            project = i['complex']['name']
        except:
            continue
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
        developer = i['developerName']
        okrug = ''
        district = ''
        adress = i['address']['displayName']
        eskrou = ''
        korpus = ''
        konstruktiv = ''
        klass = ''
        try:
            quarter = i['complex']['building']['endBuildQuarter']
            year = i['complex']['building']['endBuildYear']
        except:
            quarter = ''
            year = ''
        srok_sdachi = f"{quarter} квартал {year} года"
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if i['generalInfo']['isApartment'] == False:
            type = 'Квартиры'
        else:
            type = "Апартаменты"
        room_count = i['generalInfo']['rooms']
        area = i['generalInfo']['area']
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''
        price = ''
        old_price = int(i["price"])
        section = ''
        floor = int(i['generalInfo']['maxFloor'])
        flat_number = ''



        if i['developerOffersCount'] > 1:

            web_url = i['path']
            print(web_url)

            driver.get(web_url)
            for name, value in cookies.items():
                cookie_dict = {
                    'name': name,
                    'value': value
                }
                driver.add_cookie(cookie_dict)

            driver.get(web_url)
            time.sleep(4)
            while True:

                page_content = driver.page_source
                soup = BeautifulSoup(page_content, 'html.parser')
                items2 = soup.find_all(class_='tHj6o')

                for item in range(1,len(items2)):

                    y = items2[item]


                    url2 = ""
                    date2 = datetime.date.today()
                    project2 = project
                    english2 = ''
                    promzona2 = ''
                    mestopolozhenie2 = ''
                    subway2 = ''
                    distance_to_subway2 = ''
                    time_to_subway2 = ''
                    mck2 = ''
                    distance_to_mck2 = ''
                    time_to_mck2 = ''
                    bkl2 = ''
                    distance_to_bkl2 = ''
                    time_to_bkl2 = ''
                    status2 = ''
                    start2 = ''
                    comment2 = ''
                    developer2 = developer
                    okrug2 = ''
                    district2 = ''
                    adress2 = adress
                    eskrou2 = ''
                    try:
                        korpus2 = soup.find('span', class_= 'Is5nd').text.replace('Корпус: ', '').replace('Корпус ', '').replace('№', '').strip()
                    except:
                        korpus2 = ''
                    konstruktiv2 = ''
                    klass2 = ''
                    quarter2 = ''
                    year2 = ''
                    srok_sdachi2 = srok_sdachi
                    srok_sdachi_old2 = ''
                    stadia2 = ''
                    dogovor2 = ''
                    type2 = type
                    finish_type2 = y.get_text(separator='!').split('!')[4]
                    room_count2 = room_count
                    area2 = area
                    price_per_metr2 = ''
                    discount2 = ''
                    price_per_metr_new2 = ''
                    price2 = ''
                    old_price2 = int(y.find(class_= 'VkJXv').get_text(strip=True).replace(' ₽', '').replace(' ', '').replace('Новое', ''))
                    section2 = ''
                    floor2 = int(y.get_text(separator='!').split('!')[1])
                    flat_number2 = '' # y.find(class_= 'T8vBE').get_text(strip=True)

                    print(
                        f"{developer}, {project2}, {url2}, дата: {date2}, комнаты: {room_count2}, площадь: {area2}, цена: {price2}, старая цена: {old_price2}, корпус: {korpus2}, этаж: {floor2}")
                    result2 = [date2, project2, english2, promzona2, mestopolozhenie2, subway2, distance_to_subway2, time_to_subway2,
                              mck2,
                              distance_to_mck2, time_to_mck2, distance_to_bkl2,
                              time_to_bkl2, bkl2, status2, start2, comment2, developer2, okrug2, district2, adress2, eskrou2, korpus2,
                              konstruktiv2, klass2, srok_sdachi2, srok_sdachi_old2,
                              stadia2, dogovor2, type2, finish_type2, room_count2, area2, price_per_metr2, old_price2, discount2,
                              price_per_metr_new2, price2, section2, floor2, flat_number2]
                    flats.append(result2)

                try:
                    # Получаем все кнопки с нужным классом
                    buttons = driver.find_elements(By.CLASS_NAME, "pgnt-control-eeb-4-1-2")
                    next_button = None

                    for btn in buttons:
                        try:
                            # Проверяем, есть ли у кнопки div с нужным вложенным классом
                            btn.find_element(By.CLASS_NAME, "pgnt-next-c9c-4-1-2")
                            next_button = btn
                            break  # нашли нужную кнопку — дальше не ищем
                        except NoSuchElementException:
                            continue

                    if not next_button:
                        print("Кнопка 'вперёд' не найдена")
                        break

                    # Проверяем, не отключена ли она
                    if "pgnt-disabled-835-4-1-2" in next_button.get_attribute("class"):
                        print("Кнопка 'вперёд' неактивна, выходим из цикла")
                        break

                    ActionChains(driver).move_to_element(next_button).perform()
                    next_button.click()
                    print("Переход на следующую страницу")
                    time.sleep(2)

                except Exception as e:
                    print(f"Ошибка при переходе на следующую страницу: {e}")
                    break

        try:
            finish_type = finish_type2
        except:
            finish_type = ''

        print(
            f"{developer}, {project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)








    params["offset"] = str(int(params["offset"]) + 20)
    sleep_time = random.uniform(5, 10)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        driver.quit()
        break



save_flats_to_excel(flats, project, developer)
