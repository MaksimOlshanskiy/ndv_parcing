import requests
from bs4 import BeautifulSoup
import re
import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

current_date = datetime.date.today()


def get_section_number(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        section_li = soup.find('li', string='Секция').find_parent('li') if soup.find('li', string='Секция') else None

        if section_li:
            section_div = section_li.find('div', class_='t2')
            if section_div:
                return section_div.get_text(strip=True)

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
        rows = soup.select('table tr:has(td)')[1:]
        objects_data = []

        for row in rows:
            cols = row.find_all('td')

            if len(cols) >= 9:
                try:
                    building_text = cols[4].get_text(strip=True)
                    building_number = int(re.search(r'\d+', building_text).group()) if re.search(r'\d+', building_text) else None
                    detail_url = f"{base_url}{cols[0].find('a')['href']}" if cols[0].find('a') else None

                    section_number = None
                    if detail_url:
                        section_number = get_section_number(detail_url)
                        time.sleep(0.5)

                    price_text = cols[5].get_text(strip=True).replace('р.', '').replace(' ', '')
                    discount_text = cols[6].get_text(strip=True).replace('%', '')
                    final_price_text = cols[7].get_text(strip=True).replace('р.', '').replace(' ', '')
                    sqm_price_text = cols[8].get_text(strip=True).replace('р.', '').replace(' ', '')

                    obj = {
                        'Дата обновления': datetime.date.today(),
                        'Название проекта': 'Dream Towers',
                        'Тип помещения': 'Квартира',
                        'Отделка': 'Без отделки',
                        'Девелопер': 'Регионы',
                        'Площадь, кв.м': float(cols[1].get_text(strip=True)) if cols[1].get_text(strip=True).replace(
                            '.', '').isdigit() else None,
                        'Кол-во комнат': int(cols[2].get_text(strip=True)) if cols[2].get_text(
                            strip=True).isdigit() else None,
                        'этаж': int(cols[3].get_text(strip=True)) if cols[3].get_text(strip=True).isdigit() else None,
                        'Корпус': building_number,
                        'Цена лота, руб.': float(price_text) if price_text.replace('.', '').isdigit() else None,
                        'Скидка,%': float(discount_text) if discount_text.replace('.', '').isdigit() else None,
                        'Цена лота со ск, руб.': float(final_price_text) if final_price_text.replace('.',
                                                                                                     '').isdigit() else None,
                        'Цена кв.м со ск, руб.': float(sqm_price_text) if sqm_price_text.replace('.',
                                                                                                 '').isdigit() else None,
                        'секция': section_number
                    }

                    print(f"корпус: {building_number}, цена:{final_price_text}")

                    objects_data.append(obj)

                except Exception as e:
                    print(f"Ошибка обработки строки: {e}")
                    continue

        return objects_data

    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return None

if __name__ == "__main__":
    print("Парсинг данных с сайта Dream Towers...")
    objects = parse_dream_towers_objects()

    if objects:
        print(f"Найдено {len(objects)} объектов")
        save_flats_to_excel(objects, "Dream Towers", "Регионы")
    else:
        print("Не удалось получить данные")
