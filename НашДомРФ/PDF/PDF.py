import json
import random
import re
import time
from datetime import datetime
from io import BytesIO

import pandas as pd
import pdfplumber
import requests

from НашДомРФ.PDF.Find_project_by_id import find_project_and_building
from НашДомРФ.PDF.Get_urls import making_list_of_urls

with open(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\!changing_haracteristik_dictionary\projects.json", "r",
          encoding="utf-8") as f:
    changing_hars = json.load(f)



def extract_number(text):
    # 1. убрать zero-width и переносы строк
    text = re.sub(r'[\u200b\n]', '', text)

    # 2. найти число (включая однозначные)
    match = re.search(r'(\d+(?:[\s,.]\d+)*)', text)
    if not match:
        return None

    value = match.group()
    value = re.sub(r'\s+', '', value)
    value = value.replace(',', '.')
    value = re.sub(r'[^0-9.]', '', value)

    # если несколько точек — оставить первую
    if value.count('.') > 1:
        first = value.find('.')
        value = value[:first+1] + value[first+1:].replace('.', '')

    # -------- X2 ПРОВЕРКА (игнорируя точку) --------
    raw_digits = value.replace('.', '')

    if len(raw_digits) >= 4 and len(raw_digits) % 2 == 0:
        pairs_ok = True
        for i in range(0, len(raw_digits), 2):
            if raw_digits[i] != raw_digits[i+1]:
                pairs_ok = False
                break

        if pairs_ok:
            fixed = raw_digits[::2]

            if '.' in value:
                decimals = len(value.split('.')[-1]) // 2
                fixed = fixed[:-decimals] + '.' + fixed[-decimals:]

            value = fixed

    try:
        return float(value)
    except:
        return None

def extract_points_from_pdf_url(url, target_points):
    # 📌 Теперь храним список значений
    results = {point: [] for point in target_points}

    response = requests.get(url)
    response.raise_for_status()

    with pdfplumber.open(BytesIO(response.content)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                for row in table:
                    if not row:
                        continue

                    row = [cell if cell else "" for cell in row]

                    for point in target_points:
                        if any(point in cell for cell in row):

                            # right_column_text = row[-1]
                            # print("POINT:", point)
                            # print("RAW:", repr(right_column_text))
                            # print("-" * 50)

                            value = extract_number(row[-1])
                            if value is not None:
                                results[point].append(value)

                    summed_results = {
                        k: sum(v) if v else None
                        for k, v in results.items()
                    }

    return summed_results


corpus_ids = [64564, 44953]
finish_result_list = []

for corpus_id in corpus_ids:

    seen_months = set()
    print(corpus_id)

    list_of_urls = making_list_of_urls(corpus_id)

    print(list_of_urls)

    project_and_building = find_project_and_building(changing_hars, corpus_id)
    print(project_and_building)
    project = project_and_building['project_name']
    building = project_and_building['building_number']

    for project_declaration in list_of_urls:

        date_of_pd = project_declaration[0]
        date_of_pd = datetime.strptime(date_of_pd, "%d-%m-%Y %H:%M")
        print(date_of_pd)
        month_key = (date_of_pd.year, date_of_pd.month)

        if month_key in seen_months:
            continue  # 🔥 пропускаем, PDF даже не скачиваем

        seen_months.add(month_key)

        url = project_declaration[1]
        pd_number = project_declaration[2]

        target_points = [
            "19.7.1.1.1.1",
            "19.7.2.1.1.1",
            "19.7.3.1.1.1",
            '19.7.1.1.2.1',
            '19.7.2.1.2.1',
            '19.7.3.1.2.1',
            '19.7.1.1.3.1',
            '19.7.2.1.3.1',
            '19.7.3.1.3.1',
        ]

        data = extract_points_from_pdf_url(url, target_points)

        result = [project, building, corpus_id, date_of_pd, pd_number, data['19.7.1.1.1.1'], data['19.7.2.1.1.1'],
                  data['19.7.3.1.1.1'], data['19.7.1.1.2.1'], data['19.7.2.1.2.1'], data['19.7.3.1.2.1'],
                  data['19.7.1.1.3.1'], data['19.7.2.1.3.1'], data['19.7.3.1.3.1']]
        print(result)
        finish_result_list.append(result)
        if all(value == 0 for value in data.values()):
            break

        if date_of_pd.year < 2024:
            break

        sleep_time = random.uniform(3, 10)
        time.sleep(sleep_time)

df = pd.DataFrame(finish_result_list, columns=[
    'Название проекта',
    'Корпус',
    'ID дом.рф',
    'Дата декларации',
    'Жилые помещения, количество договоров',
    'Жилые помещения, площадь объектов',
    'Жилые помещения, суммарная цена договоров',
    'Нежилые помещения, количество договоров',
    'Нежилые помещения, площадь объектов',
    'Нежилые помещения, суммарная цена договоров',
    'Машино-места, количество договоров',
    'Машино-места, площадь объектов',
    'Машино-места, суммарная цена договоров',
])
print(df)

# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\НашДомРФ\Посейдония.xlsx"

# Сохранение файла в папку
df.to_excel(base_path, index=False)
