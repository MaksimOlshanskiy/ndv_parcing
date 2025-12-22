import requests
from bs4 import BeautifulSoup
import re
import datetime

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near


def parse_flats():
    cookies = {
        'PHPSESSID': 'NrofqkSGMtkzfdIxkURfkT4BdTYMTtl9',
        '_ct_ids': 'iprwcp8a%3A55732%3A548063993',
        '_ct_session_id': '548063993',
        '_ct_site_id': '55732',
        '_ct': '2300000000363267925',
        '_ym_uid': '1744296311369635550',
        '_ym_d': '1764581728',
        '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
        '_ym_isad': '2',
        '_ym_visorc': 'w',
        'cted': 'modId%3Diprwcp8a%3Bya_client_id%3D1744296311369635550',
        'call_s': '___iprwcp8a.1764583556.548063993.350748:1427108|2___',
    }

    headers = {
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
        'priority': 'u=1, i',
        'referer': 'https://rzv.ru/choice-flat/?arFilterFlat_134=&arFilterFlat_135=1610553442&arFilterFlat_571=&arFilterFlat_122=&arFilterFlat_123=&arFilterFlat_124_MIN=14.9&arFilterFlat_124_MAX=148.7&arFilterFlat_570_MIN=2&arFilterFlat_570_MAX=47.8&set_filter=%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'PHPSESSID=NrofqkSGMtkzfdIxkURfkT4BdTYMTtl9; _ct_ids=iprwcp8a%3A55732%3A548063993; _ct_session_id=548063993; _ct_site_id=55732; _ct=2300000000363267925; _ym_uid=1744296311369635550; _ym_d=1764581728; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_isad=2; _ym_visorc=w; cted=modId%3Diprwcp8a%3Bya_client_id%3D1744296311369635550; call_s=___iprwcp8a.1764583556.548063993.350748:1427108|2___',
    }

    base_params = {
        'arFilterFlat_134': '',
        'arFilterFlat_135': '1610553442',
        'arFilterFlat_571': '',
        'arFilterFlat_122': '',
        'arFilterFlat_123': '',
        'arFilterFlat_124_MIN': '14.9',
        'arFilterFlat_124_MAX': '148.7',
        'arFilterFlat_570_MIN': '2',
        'arFilterFlat_570_MAX': '47.8',
        'set_filter': 'Y',
        'PAGEN_1': '1',
    }

    try:
        base_url = 'https://rzv.ru/choice-flat/'
        flats_data = []
        page = 1
        skipped_flats = 0

        while True:
            params = base_params.copy()
            if page > 1:
                params['PAGEN_1'] = str(page)

            response = requests.get(
                base_url,
                params=params,
                cookies=cookies,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            current_page_flats = soup.select('a.one-favorites-list.load_more_element')

            if not current_page_flats and page > 1:
                break

            for card in current_page_flats:
                try:
                    section_element = card.select_one('.floor-favorites-list.mob-none')
                    section_text = section_element.get_text(strip=True) if section_element else None
                    section = section_text.split('(')[
                        0].strip() if section_text and '(' in section_text else section_text
                    section = section.split()[-1] if section else None

                    if not section:
                        skipped_flats += 1
                        continue

                    price_element = card.select_one('.price-favorites-list')
                    price = int(re.sub(r'[^\d]', '', price_element.get_text(strip=True))) if price_element else None

                    labels = card.select('.line-label-favorites-list .label-favorites-list')
                    rooms = labels[0].get_text(strip=True) if len(labels) > 0 else None

                    area_text = labels[1].get_text(strip=True) if len(labels) > 1 else None
                    area_value = float(re.search(r'[\d.]+', area_text).group()) if area_text else None
                    price_per_sqm = int(int(int(price) / float(area_value))) if price and area_value else None

                    floor_element = card.select_one('.floor-favorites-list.floor_at_flat_list').get_text(
                        strip=True) if card.select_one('.floor-favorites-list.floor_at_flat_list') else None
                    floor = int(floor_element.split()[0])

                    flat_data = {
                        'Дата обновления': datetime.date.today(),
                        'Название проекта': 'Малаховский',
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
                        'Девелопер': 'ГК Развитие',
                        'Округ': '',
                        'Район': '',
                        'Адрес': '',
                        'Эскроу': '',
                        'Корпус': section,
                        'Конструктив': '',
                        'Класс': '',
                        'Срок сдачи': '',
                        'Старый срок сдачи': '',
                        'Стадия строительной готовности': '',
                        'Договор': '',
                        'Тип помещения': 'Квартира',
                        'Отделка': 'Без отделки',
                        'Кол-во комнат': rooms.replace('‑комнатная', ''),
                        'Площадь, кв.м': area_value,
                        'Цена кв.м, руб.': '',
                        'Цена лота, руб.': price,
                        'Скидка,%': '',
                        'Цена кв.м со ск, руб.': '',
                        'Цена лота со ск, руб.': '',
                        'секция': '',
                        'этаж': floor,
                        'номер': None
                    }
                    flats_data.append(flat_data)

                except Exception as e:
                    print(f"Ошибка при парсинге карточки: {e}")
                    continue

            print(f"Обработано страниц: {page}, квартир: {len(flats_data)}, пропущено: {skipped_flats}")

            # Проверяем наличие кнопки "Показать еще"
            load_more = soup.select_one('.container.load_more_btn_container .ajax_load')
            if not load_more:
                break

            page += 1

        save_flats_to_excel(flats_data, 'Малаховский', 'ГК Развитие')

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return None


if __name__ == '__main__':
    flats_data = parse_flats()
    if flats_data is not None:
        print(f"\nИтого найдено {len(flats_data)} квартир")
