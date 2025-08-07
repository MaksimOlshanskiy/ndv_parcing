import requests
from bs4 import BeautifulSoup
import json
import datetime
import re

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

# URL страницы
url = "https://best-novostroy.ru/novostroyki_moskva/vao/zhk_renessans/buy_kvartira/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    flats = soup.find_all('tr', class_='ix-flat-open-popup')

    rows = []

    for flat in flats:
        data_plan = flat.get('data-plan')
        data_info = flat.get('data-info')

        plan_data = json.loads(data_plan) if data_plan else {}
        info_data = json.loads(data_info) if data_info else {}

        cells = flat.find_all('td')

        rooms = ""
        if len(cells) > 0:
            rooms_text = cells[0].text.strip()
            rooms_match = re.search(r'\d+', rooms_text)
            if rooms_match:
                rooms = rooms_match.group()

        building = cells[1].text.strip() if len(cells) > 1 else ""
        section = cells[2].text.strip() if len(cells) > 2 else ""

        floor = ""
        if len(cells) > 3:
            floor_text = cells[3].text.strip()
            floor = floor_text.replace(" эт.", "").strip()

        area = ""
        if len(cells) > 4:
            area_text = cells[4].text.strip()
            area = area_text.replace("кв.м", "").strip()

        price = ""
        if len(cells) > 5:
            price_text = cells[5].text.strip()
            price = int(price_text.replace("₽", "").replace(' ', '').strip())

        # Доп. данные
        complex_name = info_data.get('complex', '')
        old_price = info_data.get('old_price', '')
        flat_name = info_data.get('name', '')

        # Параметры для строки
        date = datetime.date.today()
        project = complex_name.replace('ЖК ', '')
        developer = "494 УНР"
        finish_type = "С отделкой"
        type = "Квартира"

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', building, '', '', '', '',
                  '', '', type, finish_type, int(rooms), float(area), '', price, '', '', "",
                  section, int(floor), '']

        rows.append(result)

    save_flats_to_excel(rows, project, developer)
else:
    print(f"Ошибка при загрузке страницы: {response.status_code}")
