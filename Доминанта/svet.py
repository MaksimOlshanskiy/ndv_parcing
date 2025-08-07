import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

'''
Проверять base_url
'''

# Базовый URL API без номера страницы
base_url = "https://d-a.ru/ajax/flats/?filter[price][0]=14067500.00&filter[price][1]=37324350.00&filter[sq][0]=0&filter[sq][1]=0&filter[profile]=%D0%96%D0%B8%D0%BB%D0%B0%D1%8F&filter[project_code]=svet&filter[type]=%D0%9C%D0%B0%D1%88%D0%B8%D0%BD%D0%BE%D0%BC%D0%B5%D1%81%D1%82%D0%BE&filter[price_mlnusd][0]=0&filter[price_mlnusd][1]=0&filter[price_mlneur][0]=0&filter[price_mlneur][1]=0&filter[price_sqm][0]=0&filter[price_sqm][1]=0&filter[price_sqmusd][0]=0&filter[price_sqmusd][1]=0&filter[price_sqmeur][0]=0&filter[price_sqmeur][1]=0&filter[hide_reserved][0]=Y&filter[flat]=&sort[sq]=1&page={page}&cnt=30"

page = 1
flats = []
count=0
max_pages = 6  # Максимальное количество страниц для парсинга

while page <= max_pages:
    # Формируем URL с текущим номером страницы
    url = base_url.format(page=page)
    print(f"Загружаем страницу {page}: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем на ошибки HTTP

        data = response.json()
        items = data.get("data", [])

        if not items:
            print(f"На странице {page} нет данных, завершаем сбор.")
            break

        print(f"Найдено {len(items)} квартир на странице {page}")

        for item in items:
            count+=1
            date = datetime.date.today()
            project = "Свет"
            developer = "Доминанта"
            korpus = item["building"]
            finish_type = item.get("finishing", "")
            room_count = item.get("bedroomscount", "")
            area = item.get("sq", "")
            price = int(str(item.get("price", "")).replace(' ', ''))
            old_price = int(str(item.get("priceold", "")))
            section = item.get("section", "")
            floor = item.get("floor", "")

            if old_price==0:
                old_price=price
                price=None

            print(f"{count} | {project}, корпус: {korpus}, этаж: {floor}, комнаты: {room_count}, площадь: {area}, цена: {price}")

            flats.append([
                date, project, "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                "", developer, "", "", "", "", int(korpus), "", "", "", "", "", "", "Квартира",
                finish_type, int(room_count), float(area), "", old_price, "", '',
                price, int(section), int(floor), ""
            ])

        page += 1
        time.sleep(0.3)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе страницы {page}: {e}")
        break

if flats:
    save_flats_to_excel(flats,project,developer)
else:
    print("Не удалось собрать данные. Проверьте URL и параметры запроса.")