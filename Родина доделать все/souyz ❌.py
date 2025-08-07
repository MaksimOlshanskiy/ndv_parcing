import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


def parse_flats():
    base_url = "https://xn--g1ani7c.xn--80adxhks/flats"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        flats_list = soup.find('div', class_='flat-list')

        if not flats_list:
            print("Не найдено списка квартир")
            return


        for flat_item in flats_list.find_all('a', class_='flat-list__item'):
            # Извлекаем этаж и корпус
            title_text = flat_item.find('div', class_='flat-list__title').find('div').get_text(strip=True)

            # Этаж
            floor_match = re.search(r'(\d+)\s*этаж', title_text)
            floor = floor_match.group(1) if floor_match else "N/A"

            # Корпус
            building_match = re.search(r'(\d+)\s*корпус', title_text)
            building = building_match.group(1) if building_match else "N/A"

            # Тип и площадь
            square_div = flat_item.find('div', class_='flat-list__square')
            if square_div:
                square_text = square_div.get_text(strip=True)
                # Разделяем тип и площадь
                if "Студия" in square_text:
                    flat_type = "Студия"
                    area_text = square_text.replace("Студия", "").strip()
                else:
                    flat_type = "Другой"
                    area_text = square_text

                # Извлекаем только число (с точкой) до "м"
                area_match = re.search(r'(\d+\.?\d*)', area_text.split('м')[0])
                area = area_match.group(1) if area_match else "N/A"
            else:
                flat_type = "N/A"
                area = "N/A"

            # Цена
            price_div = flat_item.find('div', class_='flat-list__price')
            price = price_div.get_text(" ", strip=True).replace("₽", "").strip() if price_div else "N/A"

            # Скидка
            discount = flat_item.find('div', class_='flat-list__discount').get_text(strip=True) if flat_item.find('div',
                                                                                                                  class_='flat-list__discount') else ""


            # Выводим в одну строку
            print(f"{floor}, {building}, {flat_type}, {area}, {price}")

        print(f"Всего квартир: {len(flats_list.find_all('a', class_='flat-list__item'))}")

    except Exception as e:
        print(f"\nОшибка при парсинге: {e}\n")


if __name__ == "__main__":
    parse_flats()