import json
from functions import classify_renovation, clean_filename, merge_and_clean, haversine
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

with open(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Cian\coordinates.json", "r", encoding="utf-8") as f:
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
    'ns_session': '5210b38b-2a77-4df9-a428-6405b3065d3d',
    'is-green-day-banner-hidden': 'true',
    'is-ddf-banner-hidden': 'true',
    'logoSuffix': '',
    'RETENTION_COOKIES_NAME': 'd7cf7088ab814dde8d8f546c98c6f8c4:nBa67XQBjdIGZ8ctm6VUWFBZvuI',
    'sessionId': 'be29cf2aa31349c5b9526a8908556af9:qLh2pQi0C902c_qNAP6M4MB1TKE',
    'UNIQ_SESSION_ID': '01e8c70898c34d438fc9eefa59f4b03e:1_zXQ6IYGeCp9PiCY8T9XGEuXgs',
    'adtech_uid': '5b955382-d038-40cf-a271-c67f8cd94af8%3Adomclick.ru',
    'top100_id': 't1.7711713.1405137252.1743518288740',
    '_ym_uid': '1743518289666663600',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'tmr_lvid': '6b6b440680155a4ac17ccaf6a462f603',
    'tmr_lvidTS': '1743518291170',
    'regionAlert': '1',
    'COOKIE_IS_HIDDEN_EASY_SEARCH_ONBOARDING': 'true',
    'cookieAlert': '1',
    'COOKIE_IS_HIDDEN_EASY_SEARCH_COUNTRY_ONBOARDING': 'true',
    '_ym_d': '1759300554',
    'adrdel': '1759300555210',
    '_sv': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000',
    'currentRegionGuid': '1d1463ae-c80f-4d19-9331-a1b68a85b553',
    'currentLocalityGuid': '1d1463ae-c80f-4d19-9331-a1b68a85b553',
    'regionName': '1d1463ae-c80f-4d19-9331-a1b68a85b553:%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    'favoriteHintShowed': 'true',
    'qrator_jsr': 'v2.0.1765175668.335.5b6ce31f82wfMzAJ|FGQ4eHaiSeVn2MYZ|wdHcIMSmbbdOV62Sb2cn0EV1ZksWBZcaRiYlalOk0s75R4GxR9JCIozy5FtjjMKqFVT7eUcb1ZgecgVWsK4GWQ==-hYWzzG/NDc+IzFDWYdR4tFOQGlM=-00',
    'qrator_ssid2': 'v2.0.1765175669.020.5b6ce31fuj39Qjst|ZKjOKXpnYfh2ZsFq|Ao2Wt2ogG2912gqlPQU9e8VzshPYJxhhaISNbkjtu+sd7kUo54eOjDqKAMtwtS05T6GBX6rwvKkno1GU4rNRGQ==-6vdA/6/yUz457q77rft+iw8pwxw=',
    'qrator_jsid2': 'v2.0.1765175668.335.5b6ce31f82wfMzAJ|hDmC8XEOs2qhZLh2|vAeSD78iq9bVVWVgbpv7T8XZ8P4tGGybI9ThcvN35t1aM9a79dAFXRT67Dl7ZLEA02xwqgx0glS/dxwvlMonT+isq6HGkiYeHsIresYtMbVUjt5C0C+zFz0Ai2pERQBAuwrxRVXRjKlBtEoO9hwHVxV8taEOuvWvJsGhriUpoDc=-DnEgu67TDaII/bjYuo4Z3GkBe/8=',
    'iosAppLink': '',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1765175674',
    '_ym_isad': '2',
    '_visitId': '9ec75f4a-da8b-4e97-a6b1-226f4918f4bf-f4f0dcc432ac8ba6',
    '_sas': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1765175676',
    't3_sid_7711713': 's1.1313865512.1765175675052.1765175690493.32.4.1.1..',
    'tmr_reqNum': '286',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://domclick.ru',
    'Referer': 'https://domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=5210b38b-2a77-4df9-a428-6405b3065d3d; is-green-day-banner-hidden=true; is-ddf-banner-hidden=true; logoSuffix=; RETENTION_COOKIES_NAME=d7cf7088ab814dde8d8f546c98c6f8c4:nBa67XQBjdIGZ8ctm6VUWFBZvuI; sessionId=be29cf2aa31349c5b9526a8908556af9:qLh2pQi0C902c_qNAP6M4MB1TKE; UNIQ_SESSION_ID=01e8c70898c34d438fc9eefa59f4b03e:1_zXQ6IYGeCp9PiCY8T9XGEuXgs; adtech_uid=5b955382-d038-40cf-a271-c67f8cd94af8%3Adomclick.ru; top100_id=t1.7711713.1405137252.1743518288740; _ym_uid=1743518289666663600; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; tmr_lvid=6b6b440680155a4ac17ccaf6a462f603; tmr_lvidTS=1743518291170; regionAlert=1; COOKIE_IS_HIDDEN_EASY_SEARCH_ONBOARDING=true; cookieAlert=1; COOKIE_IS_HIDDEN_EASY_SEARCH_COUNTRY_ONBOARDING=true; _ym_d=1759300554; adrdel=1759300555210; _sv=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000; currentRegionGuid=1d1463ae-c80f-4d19-9331-a1b68a85b553; currentLocalityGuid=1d1463ae-c80f-4d19-9331-a1b68a85b553; regionName=1d1463ae-c80f-4d19-9331-a1b68a85b553:%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; favoriteHintShowed=true; qrator_jsr=v2.0.1765175668.335.5b6ce31f82wfMzAJ|FGQ4eHaiSeVn2MYZ|wdHcIMSmbbdOV62Sb2cn0EV1ZksWBZcaRiYlalOk0s75R4GxR9JCIozy5FtjjMKqFVT7eUcb1ZgecgVWsK4GWQ==-hYWzzG/NDc+IzFDWYdR4tFOQGlM=-00; qrator_ssid2=v2.0.1765175669.020.5b6ce31fuj39Qjst|ZKjOKXpnYfh2ZsFq|Ao2Wt2ogG2912gqlPQU9e8VzshPYJxhhaISNbkjtu+sd7kUo54eOjDqKAMtwtS05T6GBX6rwvKkno1GU4rNRGQ==-6vdA/6/yUz457q77rft+iw8pwxw=; qrator_jsid2=v2.0.1765175668.335.5b6ce31f82wfMzAJ|hDmC8XEOs2qhZLh2|vAeSD78iq9bVVWVgbpv7T8XZ8P4tGGybI9ThcvN35t1aM9a79dAFXRT67Dl7ZLEA02xwqgx0glS/dxwvlMonT+isq6HGkiYeHsIresYtMbVUjt5C0C+zFz0Ai2pERQBAuwrxRVXRjKlBtEoO9hwHVxV8taEOuvWvJsGhriUpoDc=-DnEgu67TDaII/bjYuo4Z3GkBe/8=; iosAppLink=; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1765175674; _ym_isad=2; _visitId=9ec75f4a-da8b-4e97-a6b1-226f4918f4bf-f4f0dcc432ac8ba6; _sas=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1765175676; t3_sid_7711713=s1.1313865512.1765175675052.1765175690493.32.4.1.1..; tmr_reqNum=286',
}


ids = [116609, 119533, 113535, 110415, 121668, 111198, 109691, 120454, 120453, 61531, 3702, 112327, 119522, 119515, 117826, 120313, 122640, 119889, 115129, 121581, 120923, 116791, 109982, 118406, 121246, 118694, 117530, 109806, 124462, 121112, 114675, 119519, 109690, 114274, 122402, 123038, 122092, 118275, 112780, 114920, 116349, 118384, 119295, 120223, 120595, 120705, 121064, 122496, 122811, 123690, 124512, 62219, 110934, 111255, 125015, 121911, 117434, 117731, 113798, 115156, 119185, 113184, 97075, 73525, 113273, 119564, 112757, 118396, 109856, 122895, 119740, 120046, 121663, 116468, 120602, 124815, 115444, 1604, 3707, 4707, 60878, 73680, 111562, 113899, 113936, 115910, 115919, 116212, 116542, 117360, 118090, 120802, 122094, 122203, 122498, 124651, 124879]




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
