import requests
from bs4 import BeautifulSoup
import datetime

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

# URL страницы, с которой будем парсить данные
url = "https://www.dom-cult.ru/apartments"

# Отправляем GET запрос на сайт
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    apartments = soup.find_all('div', class_='flat__card')

    flats = []

    for apartment in apartments:
        link = apartment.find('a', class_='flat__card_link')['href']

        type_ = apartment.find('p', class_='flat__card_title').get_text(strip=True).split()[0]

        specs = apartment.find('ul', class_='flat__card_tags')
        if specs:
            for li in specs.find_all('li'):
                text = li.get_text(strip=True)
                if 'м' in text and any(char.isdigit() for char in text):
                    area = text.replace('м2', '').replace('м²', '').strip()


        floor_element = apartment.find('li', string=lambda text: 'этаж' in text)
        floor = int(floor_element.get_text(strip=True).replace(' этаж', '')) if floor_element else None

        rooms_element = apartment.find('li', string=lambda text: text and (
                    'спальня' in text or 'спальни' in text or 'Студия' in text or 'спален' in text))
        if rooms_element:
            rooms_text = rooms_element.get_text(strip=True)
            if 'Студия' in rooms_text:
                rooms = 'Студия'
            else:
                rooms = int(''.join(filter(str.isdigit, rooms_text))) or None
        else:
            rooms = None

        price_element = apartment.find('div', class_='flat__card_price')
        price = int(price_element.get_text(strip=True).replace('₽', '').replace(' ','')) if price_element else None

        if type_=='Резиденция':
            type_='Таунхаус'
        elif type_=='Пентхаус':
            type_ = 'Квартира'

        flats.append([datetime.date.today(), 'CULT', "", "", "", "",
                      "", "", "",
                      "", "", "",
                      "", "", "", "",
                      "", "Гравион", "", "", "", "",
                      '1', "", "", "", "",
                      "", "", type_, "Без отделки",
                      rooms, float(area), '', price, "", '',
                      '', "", floor, ""])

save_flats_to_excel(flats,'CULT','Гравион')

