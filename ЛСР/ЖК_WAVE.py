import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests

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
    'smFpId_old_values': '%5B%22b0d44eece823d71c253568fc397e79de%22%2C%22f0a18207107a745e280d9357abcbd51d%22%2C%22d3b2a7a62667c988953915d7d3b4139e%22%5D',
    'SCBnotShow': '-1',
    'domain_sid': '_s31UW6Md684Fha7bJKQS%3A1750859974028',
    '_ym_isad': '2',
    'spsc': '1750920512959_058f3f1f436e5d501185fc28167fdcb1_i4iKRQbkMcJUe7njxsBLkDrfvhP3GPrcK1jxC-12Rn0Z',
    'PHPSESSID': 'HUSDpN0GJCSQzrq4WbBP8fadlQKpVXmh',
    'DOMAIN': 'msk',
    'sma_session_id': '2339730387',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBporogAct': '5000',
    '_ym_visorc': 'b',
    'SCBstart': '1750920517531',
    '_cmg_csstA05bX': '1750920518',
    '_comagic_idA05bX': '11112445599.15317297684.1750920517',
    'number_phone_site': '74951510664',
    'backLink': '%2Fmsk%2Fkvartiry-v-novostroikah%2F%3Fprice%255Bmin%255D%3D9.2%26price%255Bmax%255D%3D41.1%26price_range%255Bmin%255D%3D9.2%26price_range%255Bmax%255D%3D41.1%26last_delivery%3D32%26obj%255B%255D%3D152%26obj%255B%255D%3D152%26area%255Bmin%255D%3D20%26area%255Bmax%255D%3D89%26area_range%255Bmin%255D%3D20.0%26area_range%255Bmax%255D%3D89.0%26floor%255Bmin%255D%3D2%26floor%255Bmax%255D%3D23%26floor_range%255Bmin%255D%3D2%26floor_range%255Bmax%255D%3D23',
    'number_phone_site_arr': '%5B%2274951510664%22%5D',
    'tmr_detect': '0%7C1750920523768',
    '_ga_FNTNBKC2H2': 'GS2.1.s1750920516$o31$g1$t1750920528$j48$l0$h0',
    'sma_index_activity': '1831',
    'SCBindexAct': '1631',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.lsr.ru',
    'Referer': 'https://www.lsr.ru/msk/kvartiry-v-novostroikah/?price%5Bmin%5D=8.7&price%5Bmax%5D=75.1&price_range%5Bmin%5D=8.7&price_range%5Bmax%5D=75.1&last_delivery=32&obj%5B%5D=202&obj%5B%5D=202&area%5Bmin%5D=19&area%5Bmax%5D=108&area_range%5Bmin%5D=19.0&area_range%5Bmax%5D=108.0&floor%5Bmin%5D=2&floor%5Bmax%5D=52&floor_range%5Bmin%5D=2&floor_range%5Bmax%5D=52',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'tmr_lvid=b846073c297ab0f227a0beeff859cbb0; tmr_lvidTS=1742911907765; _ym_uid=1742911908725726256; _ym_d=1742911908; _ga_09LLC3Q7HR=GS1.2.1742978855.1.0.1742978855.0.0.0; _ga=GA1.1.2011517384.1742911908; _cmg_csst7Pddw=1745507826; _comagic_id7Pddw=10313394311.14534335851.1745507826; scbsid_old=2746015342; cookie_consent=accepted; spid=1750341260887_e8966188f22fa893f1c6b051cebd99a2_141i7jfp6fqw39e6; smFpId_old_values=%5B%22b0d44eece823d71c253568fc397e79de%22%2C%22f0a18207107a745e280d9357abcbd51d%22%2C%22d3b2a7a62667c988953915d7d3b4139e%22%5D; SCBnotShow=-1; spsc=1750859969032_bcc6ec2bdf2c89c10a3684de2f597d77_i4iKRQbkMcJUe7njxsBLkDrfvhP3GPrcK1jxC-12Rn0Z; PHPSESSID=2eyjdo0CoLtGpyzOk5W4KBJRvVA1hbLf; DOMAIN=msk; sma_session_id=2339169691; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBstart=1750859973682; domain_sid=_s31UW6Md684Fha7bJKQS%3A1750859974028; SCBporogAct=5000; _ym_isad=2; _ym_visorc=b; backLink=%2Fmsk%2Fkvartiry-v-novostroikah%2F%3Fprice%255Bmin%255D%3D8.7%26price%255Bmax%255D%3D75.1%26price_range%255Bmin%255D%3D8.7%26price_range%255Bmax%255D%3D75.1%26last_delivery%3D32%26obj%255B%255D%3D202%26obj%255B%255D%3D202%26area%255Bmin%255D%3D19%26area%255Bmax%255D%3D108%26area_range%255Bmin%255D%3D19.0%26area_range%255Bmax%255D%3D108.0%26floor%255Bmin%255D%3D2%26floor%255Bmax%255D%3D52%26floor_range%255Bmin%255D%3D2%26floor_range%255Bmax%255D%3D52; _ga_FNTNBKC2H2=GS2.1.s1750859973$o29$g1$t1750859975$j58$l0$h0; _cmg_csstA05bX=1750859976; _comagic_idA05bX=11112445599.15312519079.1750859975; number_phone_site=74950195932; number_phone_site_arr=%5B%2274950195932%22%5D; tmr_detect=0%7C1750859977889; sma_index_activity=1298; SCBindexAct=798',
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
  'ok': 'HUSDpN0GJCSQzrq4WbBP8fadlQKpVXmh'
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
            old_price = ''
            discount = ''
            price_per_metr_new = ''
            price = extract_digits_or_original(i.find('span', class_= 'h4 isHiddenInGrid').text)
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