import datetime
import requests
from bs4 import BeautifulSoup

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle


def parse_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    flats = []

    for article in soup.select("article.flat"):
        try:
            project = article.select_one(".flat--addr--project-name")
            building = article.select_one(".flat--addr--building")
            section = article.select_one(".flat--addr--section")
            rooms = article.select_one(".flat--stats--rooms")
            area = article.select_one(".flat--stats--area")
            floor = article.select_one(".flat--stats--floor")
            finish = article.select_one(".flat--stats--facing")
            price = article.select_one(".flat--prices--full-price")

            project = project.text.strip() if project else None
            building = building.text.strip() if building else None
            building = building.replace('Корпус ', '')
            section = section.text.strip() if section else None
            rooms = int(str(rooms.text.strip())[0]) if rooms else None
            area = float(area.text.strip().replace(" м²", "").replace(",", ".")) if area else None
            floor = int(floor.text.strip().replace(" этаж", "")) if floor else None
            finish = finish.text.strip().replace("Отделка: ", "") if finish else 'Без отделки'
            price = int(price.text.strip().replace("₽", "").replace(" ", "")) if price else None

            if 'к' in building:
                building = building.strip()[-1]

            flats.append({
                'Дата обновления': datetime.date.today(),
                'Название проекта': project.replace('ЖК «', '').replace('»', ''),
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
                'Девелопер': 'СК Зеленоградский',
                'Округ': None,
                'Район': None,
                'Адрес': None,
                'Эскроу': None,
                'Корпус': building,
                'Конструктив': None,
                'Класс': None,
                'Срок сдачи': None,
                'Старый срок сдачи': None,
                'Стадия строительной готовности': None,
                'Договор': None,
                'Тип помещения': 'Квартира',
                'Отделка': finish,
                'Кол-во комнат': rooms,
                'Площадь, кв.м': area,
                'Цена кв.м, руб.': None,
                'Цена лота, руб.': price,
                'Скидка,%': None,
                'Цена кв.м со ск, руб.': None,
                'Цена лота со ск, руб.': None,
                'секция': section.replace('секция ', ''),
                'этаж': floor,
                'номер': None,
            })
        except Exception as e:
            print(f"Ошибка при обработке квартиры: {e}")
            continue

    return flats


base_url = "https://www.sibpromstroy.ru/flat-search/?set_filter=%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C&arrFilter_175=3801791676&arrFilter_213=&arrFilter_196_MIN=&arrFilter_196_MAX=&f%5B0%5D=city_region%3A32&f%5B1%5D=price%3A%28min%3A4360000%2Cmax%3A26290000%29&f%5B2%5D=status%3AAVAILABLE"
flats_all = []

for page_num in range(0, 28):
    print(f"Парсинг страницы {page_num}...")
    url = f"{base_url}&page={page_num}"
    flats = parse_page(url)

    if not flats:
        print(f"На странице {page_num} нет квартир или произошла ошибка.")
        continue  # Если на странице нет квартир, переходим к следующей

    flats_all.extend(flats)

developer = 'СК Зеленоградский'
project = 'Москва и МО'
save_flats_to_excel(flats_all, project, developer)
