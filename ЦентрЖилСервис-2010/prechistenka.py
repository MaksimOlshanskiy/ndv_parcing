import requests
from bs4 import BeautifulSoup
import datetime
from save_to_excel import save_flats_to_excel_old_new

url = 'https://hamovnyki.ru/prechistenka-8?filters=price_rub%2Fint_band_filter%7C31+000+000%3A3+766+700+000%3Barea%2Fint_band_filter%7C28%3A584&sort_type=expert_choice%3Adesc%2Cprice_rub%3Aasc&sort_direction=asc&viewType=list'

# Делаем запрос
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)

flats_data=[]

# Проверка статуса
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    flats = soup.find_all('div', class_='f-object__info')

    for flat in flats:
        # Название
        name_tag = flat.find('a', class_='f-object__heading')
        name = name_tag.get_text(strip=True) if name_tag else ''

        # Ссылка
        link = name_tag['href'] if name_tag and name_tag.has_attr('href') else ''

        # ЖК
        complex_tag = flat.find('div', class_='f-object__complex')
        project = complex_tag.get_text(strip=True) if complex_tag else ''

        # Метро
        metro_tag = flat.find('div', class_='f-object__metro')
        metro = metro_tag.get_text(strip=True) if metro_tag else ''

        # Площадь
        area_tag = flat.find('div', class_='f-object__spec-text', string='Площадь:')
        area_value_tag = area_tag.find_next('div', class_='f-object__spec-number') if area_tag else None
        area = area_value_tag.get_text(strip=True) if area_value_tag else ''

        # Этаж
        floor_tag = flat.find('div', class_='f-object__spec-text', string='Этаж:')
        floor_value_tag = floor_tag.find_next('div', class_='f-object__spec-number') if floor_tag else None
        floor = floor_value_tag.get_text(strip=True) if floor_tag else ''

        # Спальни
        bedrooms_tag = flat.find('div', class_='f-object__spec-text', string='Спален:')
        bedrooms_value_tag = bedrooms_tag.find_next('div', class_='f-object__spec-number') if bedrooms_tag else None
        bedrooms = bedrooms_value_tag.get_text(strip=True) if bedrooms_value_tag else ''

        # Цена (рубли)
        price_tag = flat.find('div', class_='f-object__price price-rub')
        price_number_tag = price_tag.find('div', class_='f-object__price-number') if price_tag else None
        price_rub = price_number_tag.get_text(strip=True) if price_number_tag else ''

        type_ = name.split()[0]
        project = project.split()[0].replace(',', '')
        area = area.replace(' м2', '')
        floor = floor
        rooms = bedrooms
        price = int(price_rub.replace('₽', '').replace(' ', ''))
        developer = 'ЦентрЖилСервис-2010'


        flats_data.append(
            [datetime.date.today(), project, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
             developer, "", "", "", "", '', "", "", "", "", "", "", type_, "С отделкой", rooms,
             area, "", price, "", '', '', "", floor, ""]
        )

    save_flats_to_excel(flats_data, project, developer)
else:
    print(f"Ошибка загрузки страницы: {response.status_code}")
