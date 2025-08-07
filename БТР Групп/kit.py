import requests
from bs4 import BeautifulSoup
import datetime
import re
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near


def parse_apartment(html_element):
    soup = BeautifulSoup(html_element, 'html.parser')
    apt = {
        'Дата обновления': datetime.date.today().isoformat(),
        'Название проекта': 'КИТ',
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
        'Девелопер': 'БТР Групп',
        'Округ': '',
        'Район': '',
        'Адрес': '',
        'Эскроу': '',
        'Корпус': '',
        'Конструктив': '',
        'Класс': '',
        'Срок сдачи': '',
        'Старый срок сдачи': '',
        'Стадия строительной готовности': '',
        'Договор': '',
        'Тип помещения': '',
        'Отделка': '',
        'Кол-во комнат': '',
        'Площадь, кв.м': '',
        'Цена кв.м, руб.': '',
        'Цена лота, руб.': '',
        'Скидка,% ': '',
        'Цена кв.м со ск, руб.': '',
        'Цена лота со ск, руб.': '',
        'секция': '',
        'этаж': '',
        'номер': ''
    }

    footnote = soup.find('div', class_='object__footnote')
    if footnote:
        spans = footnote.find_all('span')
        if len(spans) > 1:
            apt['Отделка'] = spans[1].get_text(strip=True)

        if spans:
            text = spans[0].get_text(strip=True)

            # Используем регулярное выражение для поиска числа между "Этаж" и "из"
            match = re.search(r'Этаж (\d+)', text)

            if match:
                apt['этаж'] = int(match.group(1))
            else:
                apt['этаж'] = None

    params = soup.find('div', class_='object__params')
    if params:
        title_div = params.find('div', class_='object__params-title')
        if title_div:
            div = title_div.find('div')
            if div:
                apt['Тип помещения'] = div.get_text(strip=True)
                if ' ' in apt['Тип помещения']:
                    apt['Кол-во комнат'] = apt['Тип помещения'].split()[0]

                    if title_div:
                        raw_type = title_div.find('div').get_text(strip=True) if title_div.find('div') else None
                        apt['Тип помещения'] = raw_type

                        if 'Студия' in raw_type:
                            apt['Кол-во комнат'] = 'Студия'
                        else:
                            match_rooms = re.match(r'(\d+)-к', raw_type)
                            apt['Кол-во комнат'] = int(match_rooms.group(1)) if match_rooms else None

                apt['Тип помещения'] = 'Квартира'

        param_divs = params.find_all('div')
        if len(param_divs) > 3:
            area_str = param_divs[3].get_text(strip=True)
            # Убираем все возможные символы, которые могут присутствовать, например, пробелы, "м²", и т.д.
            area_str = re.sub(r'[^\d.,]', '', area_str)

            try:
                apt['Площадь, кв.м'] = float(area_str.replace(',', '.'))
            except ValueError:
                apt['Площадь, кв.м'] = None
        if len(param_divs) > 5:
            apt['Отделка'] = param_divs[5].get_text(strip=True)
            if apt['Отделка'] == 'Чистовая':
                apt['Отделка'] = 'С отделкой'
            elif apt['Отделка'] == 'White Box':
                apt['Отделка'] = 'Предчистовая'

        price_div = params.find('div', class_='object__params-price')
        if price_div:
            old_price = price_div.find('span', class_='object__params-strike')
            discount = price_div.find('span', class_='object__params-discount')
            new_price = price_div.find('div')

            apt['Цена лота, руб.'] = None
            apt['Цена лота со ск, руб.'] = None

            if old_price:
                old_price_str = old_price.get_text(strip=True)
                old_price_str = re.sub(r'[^\d]', '', old_price_str)
                if old_price_str.isdigit():
                    apt['Цена лота, руб.'] = int(old_price_str)


            if new_price:
                new_price_str = new_price.get_text(strip=True)
                new_price_str = re.sub(r'[^\d]', '', new_price_str)
                if new_price_str.isdigit():
                    apt['Цена лота со ск, руб.'] = int(new_price_str)

            # Подставим цену со скидкой, если старая цена не указана
            if apt['Цена лота, руб.'] is None and apt['Цена лота со ск, руб.'] is not None:
                apt['Цена лота, руб.'] = apt['Цена лота со ск, руб.']
                apt['Цена лота со ск, руб.']=None

    aside = soup.find('div', class_='object__aside')
    if aside:
        spans = aside.find_all('span')
        if len(spans) > 2:
            korpus = spans[2].get_text(strip=True) if len(spans) > 2 else None
            apt['Корпус'] = korpus.replace(' корпус', '')

    apt_link = soup.find('a', class_='object object_room')
    if apt_link:
        href = apt_link.get('href')
        if href:
            match = re.search(r'/turn2/apartments/house-(\d+)/section-(\d+)/floor-\d+/flat-(\d+)/', href)
            if match:
                apt['секция'] = match.group(2)

    return apt


def get_all_apartments(cookies, headers, max_pages=45):
    all_apartments = []
    seen = set()

    for page in range(1, max_pages + 1):
        params = {
            'sort': 'price',
            'sortBy': 'asc',
            'turn': 'all',
            'page': page
        }

        url = 'https://dom-kit.ru/apartments/parametrical/'
        print(f"Загружаем страницу {page}...")
        r = requests.get(url, params=params, cookies=cookies, headers=headers)  # ⬅️ Добавлено params=params
        if r.status_code != 200:
            print(f"Ошибка {r.status_code} при загрузке страницы {page}")
            break

        soup = BeautifulSoup(r.text, 'html.parser')
        for apt_tag in soup.find_all('a', class_='object object_room'):
            apt = parse_apartment(str(apt_tag))
            key = f"{apt['Тип помещения']}_{apt['Площадь, кв.м']}_{apt['этаж']}_{apt['Цена лота со ск, руб.']}_{apt['Цена лота, руб.']}"
            if key not in seen:
                seen.add(key)
                all_apartments.append(apt)

        if not soup.find('div', class_='search__result-more'):
            print("Больше страниц нет.")
            break

        time.sleep(0.05)

    return all_apartments



if __name__ == '__main__':
    cookies = {'SCBnotShow': '-1'}
    headers = {
        'user-agent': 'Mozilla/5.0',
        'x-requested-with': 'XMLHttpRequest'
    }

    apartments = get_all_apartments(cookies, headers)
    save_flats_to_excel(apartments, 'Кит', 'БТР Групп')
