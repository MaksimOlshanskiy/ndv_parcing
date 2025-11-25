import requests
from bs4 import BeautifulSoup
import datetime
import re
from urllib.parse import urljoin

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new


def parse_citi_mix_flats():
    base_url = "https://citi-mix.ru"
    start_url = "/flats/catalog?corp=all&floor=all&korpus=5%2C4&pmin=7&pmax=9.6&fmin=6&fmax=18&tags=&sort=default&sortType=ASC"
    developer = "Apsis Globe"
    project = "Citi-Mix"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    flats = []
    current_url = start_url
    page_num = 1

    while current_url:
        print(f"Обрабатываю страницу {page_num}...")
        full_url = urljoin(base_url, current_url)
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        flat_cards = soup.find_all('div', class_='c-flat-row')

        for card in flat_cards:
            title = card.find('div', class_='c-flat-row__title')
            title = title.get_text(strip=True) if title else ''
            description = card.find('div', class_='c-flat-row__description')
            description = description.get_text(strip=True) if description else ''
            price_element = card.find('div', class_='c-flat-row__price')
            price = re.search(r'[\d\s]+', price_element.get_text(strip=True)).group().replace(' ',
                                                                                              '') if price_element else ''

            area_match = re.search(r'(\d+\.?\d*)\s*м', title)
            area = area_match.group(1) if area_match else ''

            corp_match = re.search(r'(\d+)\s*корпус', description)
            floor_match = re.search(r'этаж\s*(\d+)', description)
            corp_number = corp_match.group(1) if corp_match else ''
            floor_number = floor_match.group(1) if floor_match else ''

            flats.append([
                datetime.date.today(), project, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                developer, "", "", "", "", corp_number, "", "", "", "", "", "", 'Апартаменты', "С отделкой", "",
                float(area), "",int(price), "", "", '', "", int(floor_number), ""
            ])

        next_button = soup.find('a', class_='c-grid__pagers-button c-grid__pagers-button--next')
        current_url = next_button['href'] if next_button and 'href' in next_button.attrs else None
        page_num += 1

    save_flats_to_excel(flats,project,developer)

    print(f"Данные успешно сохранены")


if __name__ == "__main__":
    parse_citi_mix_flats()
