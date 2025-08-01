from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_far
import requests
from bs4 import BeautifulSoup
import datetime

url = "https://gk-moskovsky.ru/vybor-kvartiry/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

cards = soup.find_all("div", class_="elementor-column-wrap")

flats = []

for card in cards:
    try:
        title = card.find("h2", string=lambda s: s and "ЖК" in s).text.strip().replace('ЖК "', '').replace('"', '')
        flat_type = card.find_all("h2")[1].text.strip()

        if 'Квартира-студия' in flat_type:
            rooms = 'студия'
        else:
            rooms = int(flat_type.split()[0].replace('-комнатная',''))

        type_ = 'Квартира'
        price_info = card.find_all("h2")[2].text.strip()
        area_info = card.find_all("h2")[3].text.strip()

        price_parts = price_info.replace('\xa0', ' ').split()
        price = ''.join(price_parts[2:5])
        price_per_m2 = int(price_parts[-2].replace('.', '')) if len(price_parts) > 2 else ""

        area = float(area_info.split()[-2])

        link_tag = card.find("a", href=True)
        detail_url = link_tag['href'] if link_tag else ""

        flats.append({
            "Ссылка": detail_url,
            'Дата обновления': datetime.date.today(),
            'Название проекта': title,
            'на англ': None,
            'промзона': None,
            'Местоположение': None,
            'Метро': None,
            'Расстояние до метро, км': None,
            'Время до метро, мин': None,
            'МЦК/МЦД/БКЛ': None,
            'Расстояние до МЦК/МЦД, км': None,
            'Время до МЦК/МЦД, мин': None,
            'БКЛ': None,
            'Расстояние до БКЛ, км': None,
            'Время до БКЛ, мин': None,
            'статус': None,
            'старт': None,
            'Комментарий': None,
            'Девелопер': "Спсити",
            'Округ': None,
            'Район': None,
            'Адрес': None,
            'Эскроу': None,
            'Корпус': '1',
            'Конструктив': None,
            'Класс': None,
            'Срок сдачи': None,
            'Старый срок сдачи': None,
            'Стадия строительной готовности': None,
            'Договор': None,
            'Тип помещения': type_,
            'Отделка': 'Без отделки',
            'Кол-во комнат': rooms,
            'Площадь, кв.м': area,
            'Цена кв.м, руб.': None,
            'Цена лота, руб.': price,
            'Скидка,%': None,
            'Цена кв.м со ск, руб.': None,
            'Цена лота со ск, руб.': None,
            'секция': None,
            'этаж': None,
            'номер': None
        })

    except Exception:
        continue

developer = 'Спсити'
project = 'Московский'
save_flats_to_excel(flats, project, developer)

