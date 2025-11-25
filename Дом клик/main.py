import json
from functions import classify_renovation, clean_filename, merge_and_clean, haversine, domclick_skip
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
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

with open("coordinates.json", "r", encoding="utf-8") as f:
    city_centers = json.load(f)

developer = ''
project = ''
area = ''
region = 'Самара'

coords = city_centers.get(region)

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

cookies = {
    'ns_session': 'a9b0527d-1831-4051-9691-f2a4ff9f2eb1',
    '_ym_uid': '1754049701221173595',
    '_ym_d': '1754049701',
    'is-green-day-banner-hidden': 'true',
    'is-ddf-banner-hidden': 'true',
    'RETENTION_COOKIES_NAME': 'cf097f92a360491a94d2b23ea308902f:ztXlYHeFUoQ4EW8CGN8-8HaKM5o',
    'sessionId': 'b53dde4d6b3e41048c50269ef9a9a640:087ckq3ae0HFXc7RfxSMR6JZ4eE',
    'UNIQ_SESSION_ID': 'e3b5b2661819410dab5179919a9a5dbf:4X3jH9cQ0_NIooq_KXzwDcVRQfQ',
    'logoSuffix': '',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}',
    'adrcid': 'ATq4NGAhUq_h0PN1rcX56vw',
    'adtech_uid': '2529e064-13de-46d3-b559-557905b2c7ab%3Adomclick.ru',
    'top100_id': 't1.7711713.1875136519.1754049702923',
    'tmr_lvid': '591f79504a966df059c5d4755ee24cfd',
    'tmr_lvidTS': '1754049703045',
    'regionAlert': '1',
    'iosAppAvailable': 'true',
    'cookieAlert': '1',
    'iosAppLink': '',
    'auto-definition-region': 'false',
    'currentSubDomain': 'samara',
    '_sv': 'SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664',
    'adrdel': '1759388033851',
    'qrator_jsr': 'v2.0.1759473042.011.59bc78366yAvg5Tp|drNsNYFMREeM3S5n|8tUhfFgWFJytULpM+oU+VkWXV+ZSyHyMxIm/+16QZOOp+1m1VhWWGFuI1MQzIQ/UT+kxYSNKCUoipp6CerClVQ==-F4M7/56Oeu5hBcQuu7f7MWbiDYI=-00',
    'qrator_jsid2': 'v2.0.1759473042.011.59bc78366yAvg5Tp|vaDq5x3IZFR8ySzc|uHxI/dcmbno3EK1MNh2Szg464g5qKhtTnKPdxujLxLUqkROV2/3tAQ/5iKHCj123a8CQ1UNiGRY5A2KoCTwssc28Jwi7VDoUJw5RQzv2fSfbavhpIlLfG134Hsh6cig0pj+Gu2xpzYI3KUnX1iCB3w==-7CkWf0POLc7RrUq+Ji5aqFezVbI=',
    '_ym_isad': '2',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664.1759473042',
    '_visitId': '6eb33d4f-caf5-4022-a04c-cb1cb64c9057-f4f0dcc432ac8ba6',
    '_sas': 'SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664.1759473048',
    'currentRegionGuid': '321b0daa-da95-4ce5-81b3-a7ab62d89d19',
    'currentLocalityGuid': '6369cbfc-1f06-4574-adba-82f4dc42c0f7',
    'regionName': '6369cbfc-1f06-4574-adba-82f4dc42c0f7:%D0%A1%D0%B0%D0%BC%D0%B0%D1%80%D0%B0',
    'tmr_reqNum': '361',
    't3_sid_7711713': 's1.350417262.1759473043176.1759473112563.6.11.2.1..',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://samara.domclick.ru',
    'Referer': 'https://samara.domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=a9b0527d-1831-4051-9691-f2a4ff9f2eb1; _ym_uid=1754049701221173595; _ym_d=1754049701; is-green-day-banner-hidden=true; is-ddf-banner-hidden=true; RETENTION_COOKIES_NAME=cf097f92a360491a94d2b23ea308902f:ztXlYHeFUoQ4EW8CGN8-8HaKM5o; sessionId=b53dde4d6b3e41048c50269ef9a9a640:087ckq3ae0HFXc7RfxSMR6JZ4eE; UNIQ_SESSION_ID=e3b5b2661819410dab5179919a9a5dbf:4X3jH9cQ0_NIooq_KXzwDcVRQfQ; logoSuffix=; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; adrcid=ATq4NGAhUq_h0PN1rcX56vw; adtech_uid=2529e064-13de-46d3-b559-557905b2c7ab%3Adomclick.ru; top100_id=t1.7711713.1875136519.1754049702923; tmr_lvid=591f79504a966df059c5d4755ee24cfd; tmr_lvidTS=1754049703045; regionAlert=1; iosAppAvailable=true; cookieAlert=1; iosAppLink=; auto-definition-region=false; currentSubDomain=samara; _sv=SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664; adrdel=1759388033851; qrator_jsr=v2.0.1759473042.011.59bc78366yAvg5Tp|drNsNYFMREeM3S5n|8tUhfFgWFJytULpM+oU+VkWXV+ZSyHyMxIm/+16QZOOp+1m1VhWWGFuI1MQzIQ/UT+kxYSNKCUoipp6CerClVQ==-F4M7/56Oeu5hBcQuu7f7MWbiDYI=-00; qrator_jsid2=v2.0.1759473042.011.59bc78366yAvg5Tp|vaDq5x3IZFR8ySzc|uHxI/dcmbno3EK1MNh2Szg464g5qKhtTnKPdxujLxLUqkROV2/3tAQ/5iKHCj123a8CQ1UNiGRY5A2KoCTwssc28Jwi7VDoUJw5RQzv2fSfbavhpIlLfG134Hsh6cig0pj+Gu2xpzYI3KUnX1iCB3w==-7CkWf0POLc7RrUq+Ji5aqFezVbI=; _ym_isad=2; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664.1759473042; _visitId=6eb33d4f-caf5-4022-a04c-cb1cb64c9057-f4f0dcc432ac8ba6; _sas=SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664.1759473048; currentRegionGuid=321b0daa-da95-4ce5-81b3-a7ab62d89d19; currentLocalityGuid=6369cbfc-1f06-4574-adba-82f4dc42c0f7; regionName=6369cbfc-1f06-4574-adba-82f4dc42c0f7:%D0%A1%D0%B0%D0%BC%D0%B0%D1%80%D0%B0; tmr_reqNum=361; t3_sid_7711713=s1.350417262.1759473043176.1759473112563.6.11.2.1..',
}


ids = [118718, 116835, 113022, 120392, 115133, 117042, 118424, 114760, 113200, 118674, 119885, 118577, 115573, 118358, 119095, 114828, 116648, 119631, 121722, 116110, 112606, 118639, 123320, 123400, 123957, 124413, 111097, 61486, 116406, 118993, 123711, 2589, 116736, 114032, 119223, 117214, 121640, 119597, 115258, 120486, 116630, 116439, 6990, 9506, 80566, 86457, 110256, 115976, 116112, 118411, 118710, 118783, 118814, 118856, 119365, 121023, 121481, 121706, 122100, 111079, 111611, 112049, 124047]



def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


# Основной цикл по ID комплексов
for complex_id in ids:
    flats = []
    params = {
        'address': '25a8b02a-a308-4cb2-bbba-b31592b66046',
        'offset': '0',
        'limit': '20',
        'sort': 'qi',
        'sort_dir': 'desc',
        'deal_type': 'sale',
        'category': 'living',
        'offer_type': 'layout',
        'complex_ids': [complex_id],  # Используем текущий ID из списка
        'complex_name': 'ЖК Солнечный город',
        'from_developer': '1',
        'sort_by_tariff_date': '1',
    }

    print(f"\nНачинаем обработку комплекса с ID: {complex_id}")

    while True:
        response = requests.get('https://bff-search-web.domclick.ru/api/offers/v1', params=params, cookies=cookies,
                                headers=headers)
        print(f"Статус код: {response.status_code}, offset: {params['offset']}")

        try:
            items = response.json()['result']['items']
        except (KeyError, ValueError) as e:
            print(f"Ошибка при обработке ответа: {e}")
            break

        if not items:
            print("Нет данных, завершаем обработку этого комплекса")
            break

        for i in items:
            url = ""
            date = datetime.date.today()
            project = i['complex']['name'].replace('"', '').replace('ЖК ', '')
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
            eskrou = ''
            korpus = ''
            konstruktiv = ''
            klass = ''
            try:
                quarter = i['complex']['building']['endBuildQuarter']
                year = i['complex']['building']['endBuildYear']
                srok_sdachi = f"{quarter} квартал {year} года"
            except:
                quarter = ''
                year = ''
                srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = 'Квартира' if not i['generalInfo']['isApartment'] else "Апартаменты"
            room_count = i['generalInfo']['rooms']
            area = i['generalInfo']['area']
            price_per_metr = ''
            discount = ''
            price_per_metr_new = ''
            price = int(i["price"])
            old_price = ''
            section = ''
            floor = int(i['generalInfo']['maxFloor'])
            flat_number = ''
            finish_type = ''
            added = ''
            try:
                lat_jk = i['location']['lat']
                lon_jk = i['location']['lon']
                lat_center = coords["lat_center"]
                lon_center = coords["lon_center"]
                distance = round(haversine(lat_jk, lon_jk, lat_center, lon_center), 2)
            except:
                distance = ''
            try:
                geo1 = i['address']['displayName'].split(',')[1].strip()
            except:
                geo1 = ''
            try:
                geo2 = i['address']['displayName'].split(',')[2].strip()
            except:
                geo2 = ''
            try:
                geo3 = i['address']['displayName'].split(',')[3].strip()
            except:
                geo3 = ''
            try:
                geo4 = i['address']['displayName'].split(',')[4].strip()
            except:
                geo4 = ''

            kitchenArea = ''
            livingArea = ''
            parking = ''
            balconies_and_loggias_count = ''

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

                    for item in range(1, len(items2)):

                        y = items2[item]

                        url2 = web_url
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
                        eskrou2 = ''
                        korpus2 = ''
                        konstruktiv2 = ''
                        klass2 = ''
                        quarter2 = ''
                        year2 = ''
                        srok_sdachi_old2 = ''
                        stadia2 = ''
                        dogovor2 = ''
                        finish_type2 = y.find_all('div', class_='yzjlv')[2].get_text().strip()


                        area2 = area
                        price_per_metr2 = ''
                        discount2 = ''
                        price_per_metr_new2 = ''
                        try:
                            price2 = int(y.find(class_='VkJXv').get_text(strip=True).replace(' ₽', '').replace(' ', ''))
                        except:
                            price2 = y.find(class_='VkJXv').get_text(strip=True).replace(' ₽', '').replace(' ', '')
                        old_price2 = ''
                        section2 = ''
                        floor2 = int(y.get_text(separator='!').split('!')[1])
                        flat_number2 = ''
                        added2 = ''

                        print(
                            f"Вложенные лоты || {project2}, комнаты: {room_count}, площадь: {area2}, цена: {price2}, этаж: {floor2}, отделка: {finish_type2}")

                        result2 = [project, developer, geo1, geo2, geo3, geo4, korpus, distance, srok_sdachi, type,
                                   finish_type2, room_count, area, '', '', price2, floor2, '', '', url2]
                        flats.append(result2)

                    try:
                        buttons = driver.find_elements(By.CLASS_NAME, "pgnt-control-eeb-4-0-1")
                        next_button = None

                        for btn in buttons:
                            try:
                                btn.find_element(By.CLASS_NAME, "pgnt-next-c9c-4-0-1")
                                next_button = btn
                                break
                            except NoSuchElementException:
                                continue

                        if not next_button:
                            print("Кнопка 'вперёд' не найдена")
                            break

                        if "pgnt-disabled-835-4-0-1" in next_button.get_attribute("class"):
                            print("Кнопка 'вперёд' неактивна, выходим из цикла")
                            break

                        # Попробуем закрыть всплывающее окно cookies, если оно есть
                        try:
                            cookie_alert = driver.find_element(By.CLASS_NAME, "tpln-CookieAlert-spoilerIntro--11-5-1")
                            close_button = cookie_alert.find_element(By.TAG_NAME,
                                                                     "button")  # Или уточни CSS селектор, если другой
                            close_button.click()
                            print("Всплывающее окно закрыто")
                            time.sleep(1)
                        except NoSuchElementException:
                            pass
                        except Exception as ce:
                            print(f"Не удалось закрыть всплывающее окно: {ce}")

                        try:
                            ActionChains(driver).move_to_element(next_button).perform()
                            next_button.click()
                        except ElementClickInterceptedException:
                            # Вдруг не получилось — пробуем через JS
                            print("Перекрыт элемент, пробуем кликнуть через JS")
                            driver.execute_script("arguments[0].click();", next_button)

                        print("Переход на следующую страницу")
                        time.sleep(2)

                    except Exception as e:
                        print(f"Ошибка при переходе на следующую страницу: {e}")
                        break
            try:
                finish_type = finish_type2
            except:
                finish_type = ''
            try:
                url = url2
            except:
                url = ''

            print(
                f"{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}, отделка: {finish_type}")
            result = [project, developer, geo1, geo2, geo3, geo4, korpus, distance, srok_sdachi, type,
                      finish_type, room_count, area, '', '', price, floor, '', '', url]
            flats.append(result)

        params["offset"] = str(int(params["offset"]) + 20)
        sleep_time = random.uniform(5, 10)
        time.sleep(sleep_time)

        # Сохраняем результаты в Excel
    df = pd.DataFrame(flats, columns=['Название проекта',
                                      'Девелопер',
                                      'Гео1',
                                      'Гео2',
                                      'Гео3',
                                      'Гео4',
                                      'Корпус',
                                      'Расстояние до центра, км',
                                      'Срок сдачи',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Площадь кухни, кв.м',
                                      'Жилая площадь, кв.м',
                                      'Цена лота, руб.',
                                      'Этаж',
                                      'Балконы/лоджии',
                                      'Паркинг',
                                      'Ссылка'])

    current_date = datetime.date.today()
    base_path = r""
    folder_path = os.path.join(base_path, str(current_date))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{region}_{complex_id}_{current_date}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)

    print(f"\nВсе данные успешно сохранены в файл: {file_path}")

# Закрываем драйвер после обработки всех комплексов
driver.quit()
