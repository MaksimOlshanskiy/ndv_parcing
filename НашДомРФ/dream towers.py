import os
import requests
from bs4 import BeautifulSoup
import re
from openpyxl import Workbook
import datetime
import time

current_date = datetime.date.today()


def get_section_number(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем конкретную структуру с номером секции
        section_li = soup.find('li', string='Секция').find_parent('li') if soup.find('li', string='Секция') else None

        if section_li:
            section_div = section_li.find('div', class_='t2')
            if section_div:
                return section_div.get_text(strip=True)

        # Альтернативный поиск, если первый не сработал
        for li in soup.find_all('li'):
            t1_div = li.find('div', class_='t1')
            if t1_div and t1_div.get_text(strip=True) == 'Секция':
                t2_div = li.find('div', class_='t2')
                if t2_div:
                    return t2_div.get_text(strip=True)

        return None

    except Exception as e:
        print(f"Ошибка при парсинге страницы объекта {url}: {e}")
        return None


def parse_dream_towers_objects():
    base_url = "https://dream-towers.ru"
    url = f"{base_url}/genplan/params/"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('table tr:has(td)')
        objects_data = []

        for row in rows:
            cols = row.find_all('td')

            if len(cols) >= 9:
                try:
                    building_text = cols[4].get_text(strip=True)
                    building_number = int(re.search(r'\d+', building_text).group()) if re.search(r'\d+',
                                                                                                 building_text) else None
                    detail_url = f"{base_url}{cols[0].find('a')['href']}" if cols[0].find('a') else None

                    # Получаем номер секции
                    section_number = None
                    if detail_url:
                        section_number = get_section_number(detail_url)
                        time.sleep(0.5)  # Уменьшенная пауза между запросами

                    # Основные данные из таблицы
                    obj = {
                        'Тип помещения': 'Квартира',
                        'Отделка': 'Без отделки',
                        'Девелопер': 'Регионы',
                        'Площадь, кв.м': float(cols[1].get_text(strip=True)) if cols[1].get_text(strip=True).replace(
                            '.', '').isdigit() else None,
                        'Кол-во комнат': int(cols[2].get_text(strip=True)) if cols[2].get_text(
                            strip=True).isdigit() else None,
                        'этаж': int(cols[3].get_text(strip=True)) if cols[3].get_text(strip=True).isdigit() else None,
                        'Корпус': building_number,
                        'Цена лота, руб.': float(cols[5].get_text(strip=True).replace('р.', '').replace(' ', '')) if
                        cols[5].get_text(strip=True) else None,
                        'Скидка,%': float(cols[6].get_text(strip=True).replace('%', '')) if cols[6].get_text(
                            strip=True) else None,
                        'Цена лота со ск, руб.': float(
                            cols[7].get_text(strip=True).replace('р.', '').replace(' ', '')) if cols[7].get_text(
                            strip=True) else None,
                        'Цена кв.м со ск, руб.': float(
                            cols[8].get_text(strip=True).replace('р.', '').replace(' ', '')) if
                        cols[8].get_text(strip=True) else None,
                        'Ссылка': detail_url,
                        'секция': section_number
                    }

                    objects_data.append(obj)

                except Exception as e:
                    print(f"Ошибка обработки строки: {e}")
                    continue

        return objects_data

    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return None


def save_to_excel(data):
    if not data:
        print("Нет данных для сохранения")
        return

    # Определяем путь для сохранения
    base_path = r"C:\Users\m.lugovskiy\PycharmProjects\Parcer"
    folder_path = os.path.join(base_path, str(current_date))

    # Создаем папку, если она не существует
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Полный путь к файлу
    filename = f'Dream Towers_{current_date}.xlsx'
    full_path = os.path.join(folder_path, filename)

    wb = Workbook()
    ws = wb.active


    all_fields = [
        'Дата обновления',
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
        'номер'
    ]

    # Добавляем заголовки
    ws.append(all_fields)

    # Заполняем данные
    for obj in data:
        row = []
        for field in all_fields:
            if field in obj:
                row.append(obj[field])
            elif field == 'Дата обновления':
                row.append(current_date)
            elif field == 'Название проекта':
                row.append('Dream Towers')
            else:
                row.append(None)
        ws.append(row)

    # Сохраняем файл
    wb.save(full_path)
    print(f"Файл успешно сохранён: {full_path}")


if __name__ == "__main__":
    print("Парсинг данных с сайта Dream Towers...")
    objects = parse_dream_towers_objects()

    if objects:
        print(f"Найдено {len(objects)} объектов")
        save_to_excel(objects)
    else:
        print("Не удалось получить данные")
