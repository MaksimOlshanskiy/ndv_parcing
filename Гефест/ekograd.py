import datetime

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode, urlparse, parse_qs

BASE_URL = "https://gefestholding.ru"
BASE_PATH = "/obekty/ekograd-novyj-katuar/kvartiry-v-prodazhe-novii-katuar/"
PARAMS = {
    "flat[0]": "s",
    "flat[1]": "a",
    "flat[2]": "1",
    "flat[3]": "2",
    "flat[4]": "3",
    "pricelower": "100000.00",
    "priceupper": "1204000099.00",
    "sqlower": "10.00",
    "squpper": "999.00"
}
HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_html(url, params=None):
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.text


def get_total_pages(html):
    soup = BeautifulSoup(html, "html.parser")
    pages = soup.select("a[href*='list_page']")
    max_page = 1
    for a in pages:
        href = a.get("href")
        parsed = parse_qs(urlparse(href).query)
        page_num = int(parsed.get("list_page", [1])[0])
        max_page = max(max_page, page_num)
    return max_page


def parse_flats(html):
    soup = BeautifulSoup(html, "html.parser")
    flats = []

    for flat_div in soup.find_all("div", id=lambda x: x and x.startswith("printcontent")):
        try:
            flat_id = flat_div["id"].replace("printcontent", "")
            popup = flat_div.find("div", id=f"popup{flat_id}")
            raw_text = popup.find("div", class_="print").get_text(" ", strip=True)

            def extract(label):
                if label not in raw_text:
                    return ''
                part = raw_text.split(label)[1].split(" /")[0]
                return part.strip()

            complex_name = extract("ЖК:")
            korpus_sect_flat = extract("Корпус")
            floor = extract("Этаж:")
            area = extract("Общая площадь:")
            price = extract("Цена:")

            finish = ''
            rows = popup.find("table").find_all("tr")
            for row in rows:
                tds = row.find_all("td")
                if len(tds) == 2 and "отделк" in tds[0].text.lower():
                    finish = tds[1].text.strip()
                    break

            book_link_tag = popup.find("a", href=lambda x: x and x.startswith("forma-obratnoj-svyazi"))

            flats.append({
                'Дата обновления': datetime.date.today(),
                'Название проекта': complex_name.replace('ЖК «', '').replace('» Адрес', ''),
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
                'Девелопер': "Гефест",
                'Округ': None,
                'Район': None,
                'Адрес': None,
                'Эскроу': None,
                'Корпус': korpus_sect_flat,
                'Конструктив': None,
                'Класс': None,
                'Срок сдачи': None,
                'Старый срок сдачи': None,
                'Стадия строительной готовности': None,
                'Договор': None,
                'Тип помещения': 'Квартира',
                'Отделка': 'без отделки',
                'Кол-во комнат': None,
                'Площадь, кв.м': float(area.replace(",", ".")) if area else None,
                'Цена кв.м, руб.': None,
                'Цена лота, руб.': int(
                    price.replace(" ", "").replace("руб.", "").replace("р.", "")) if price else None,
                'Скидка,%': None,
                'Цена кв.м со ск, руб.': None,
                'Цена лота со ск, руб.': None,
                'секция': None,
                'этаж': int(floor) if floor else None,
                'номер': None,
            })

        except Exception as e:
            print(f"Ошибка при парсинге квартиры: {e}")

    return flats


def main():
    print("Загружаем первую страницу...")
    first_url = urljoin(BASE_URL, BASE_PATH)
    html = get_html(first_url, PARAMS)
    total_pages = get_total_pages(html)

    print(f"Всего страниц: {total_pages}")
    all_flats = []

    for page in range(1, total_pages + 1):
        print(f"Парсинг страницы {page} из {total_pages}")
        params = PARAMS.copy()
        if page > 1:
            params["list_page"] = page
        page_html = get_html(first_url, params)
        flats = parse_flats(page_html)
        all_flats.extend(flats)

    save_flats_to_excel(all_flats, 'Экоград','Гефест')


if __name__ == "__main__":
    main()
