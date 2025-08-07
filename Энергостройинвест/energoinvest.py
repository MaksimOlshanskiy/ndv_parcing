import re
import datetime
import requests
from bs4 import BeautifulSoup

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all


def parse_apartments(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Ошибка при запросе: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    apartments_rows = soup.find_all('div', class_='apartments-table__row')[1:]
    apartments = []

    for row in apartments_rows:
        columns = row.find_all('div')
        if len(columns) >= 7:
            try:
                price_text = columns[6].find('span').text
                price = float(re.sub(r'[^\d]', '', price_text))

                area_text = columns[2].text.strip().replace(',', '.')
                area = float(re.sub(r'[^\d.]', '', area_text))

                rooms_text = columns[3].text.strip()
                if 'С' in rooms_text:
                    rooms = "Студия"
                else:
                    rooms = rooms_text

                apartment = {
                    'Дата обновления': datetime.date.today(),
                    'Название проекта': 'Self',
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
                    'Девелопер': 'Энергостройинвест',
                    'Округ': '',
                    'Район': '',
                    'Адрес': '',
                    'Эскроу': '',
                    'Корпус': columns[5].text.strip(),
                    'Конструктив': '',
                    'Класс': '',
                    'Срок сдачи': '',
                    'Старый срок сдачи': '',
                    'Стадия строительной готовности': '',
                    'Договор': '',
                    'Тип помещения': 'Квартира',
                    'Отделка': 'Без отделки',
                    'Кол-во комнат': rooms,
                    'Площадь, кв.м': area,
                    'Цена кв.м, руб.': '',
                    'Цена лота, руб.': price,
                    'Скидка,%': '',
                    'Цена кв.м со ск, руб.': '',
                    'Цена лота со ск, руб.': '',
                    'секция': '',
                    'этаж': int(columns[4].text.strip()),
                    'номер': ''
                }

                apartments.append(apartment)

            except Exception as e:
                print(f"Ошибка при обработке строки: {e}")

    return apartments





if __name__ == "__main__":
    url = "https://self-kvartal.ru/apartments/list"
    apartments = parse_apartments(url)

    if apartments:
        save_flats_to_excel(apartments, 'all', 'Энергостройинвест')
    else:
        print("Не удалось получить данные о квартирах")
