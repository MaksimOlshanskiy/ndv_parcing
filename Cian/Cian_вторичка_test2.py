import os
import json
import time
import datetime
import requests
import pandas as pd

class CianParser:
    def __init__(self, cities, base_path=None):
        self.cities = cities
        self.base_path = base_path or os.getcwd()
        self.session = self._create_session()
        self.current_date = datetime.date.today()

    def _create_session(self):
        session = requests.Session()
        session.headers.update({
            'authority': 'api.cian.ru',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.cian.ru',
            'referer': 'https://www.cian.ru/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        })
        session.cookies.update({
            'session_region_id': '1'
        })
        return session

    def parse(self):
        for user_input, city_name in self.cities.items():
            user_id = int(user_input)
            all_flats = []
            for page in range(1, 31):
                try:
                    json_data = self._build_query(user_id, page)
                    response = self.session.post('https://api.cian.ru/search-offers/v2/search-offers-desktop/', json=json_data)
                    if response.status_code != 200:
                        print(f"❌ Ошибка запроса для города {city_name}, страница {page}: {response.status_code}")
                        break

                    data = response.json()
                    items = data['data']['offers']
                    if not items:
                        break

                    for item in items:
                        flat_data = self._extract_flat_data(item)
                        if flat_data:
                            all_flats.append(flat_data)

                    time.sleep(1)

                except Exception as e:
                    print(f"Ошибка на странице {page} для города {city_name}: {e}")
                    break

            if all_flats:
                self._save_to_excel(all_flats, city_name)

    def _build_query(self, user_id, page):
        with open('cian_query_template.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        json_data['jsonQuery']['region']['value'] = [user_id]
        json_data['jsonQuery']['_type'] = "flatsale"
        json_data['jsonQuery']['page'] = page
        return json_data

    def _extract_flat_data(self, item):
        try:
            address = item.get('geo', {}).get('userInput', '')
            price = item.get('bargainTerms', {}).get('priceRur', '')
            area = item.get('payload', {}).get('totalArea', '')
            floor = item.get('payload', {}).get('floorNumber', '')
            floors_count = item.get('payload', {}).get('building', {}).get('floorsCount', '')
            decoration = item.get('payload', {}).get('decoration', '')
            sale_discount = item.get('bargainTerms', {}).get('saleDiscount', '')
            return [address, price, area, floor, floors_count, decoration, sale_discount]
        except Exception as e:
            print(f"Ошибка при извлечении данных: {e}")
            return None

    def _save_to_excel(self, flats, city_name):
        df = pd.DataFrame(flats, columns=['Address', 'Price', 'Area', 'Floor', 'FloorsCount', 'Decoration', 'Discount'])
        df = df[df['Price'] != '']
        df = df[df['Area'] != '']

        filename = f"{city_name}_{self.current_date}.xlsx"
        filepath = os.path.join(self.base_path, filename)
        df.to_excel(filepath, index=False)
        print(f"✅ Сохранено: {filepath}")


if __name__ == "__main__":
    cities = cities = {
        "1": "Москва",
        "2": "Санкт-Петербург",
        "25": "Казань"
    }

    parser = CianParser(cities)
    parser.parse()
