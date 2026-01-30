from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from selenium import webdriver
import requests
import json
from bs4 import BeautifulSoup


def convert_quarter(text: str) -> str:
    roman_to_int = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4
    }

    for roman, arabic in roman_to_int.items():
        if text.startswith(roman):
            # удаляем " кв." или " кв. "
            rest = text.replace(f"{roman} кв.", "").replace(f"{roman} кв. ", "")
            return f"{arabic} кв {rest.strip()}"

    return text  # если формат не совпал

buildings_id = ['3025', '3395', '3882', '8637', '22344', '33295', '33296', '38074', '42436', '42437', '44480', '45019', '53850', '55727', '55728', '56378', '57464', '57765', '57833', '57911', '57912', '58179', '58180', '58912', '59950', '60694', '61154', '62048', '62967', '62968', '63664', '63874', '64171', '64236', '65027', '65042', '65271', '65567', '66029', '66184', '66384', '66614', '66615', '66795', '66796', '66817', '67259', '67322', '67372', '67403', '67823', '67824', '67872', '67873', '68028', '68054', '68055', '68056', '68404', '68406', '68407', '68408', '68409', '68410', '68859', '68944', '69169', '69171', '69392', '69662']

rows = []

current_date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
offset_counter = 0

driver = webdriver.Chrome()

for building_id in buildings_id:

    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{building_id}/sale_graph?type=apartments'
    print(url)

    driver.get(url=url)
    page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
    json_text = driver.find_element("tag name", "body").text  # Читаем текст из <body>
    salesGraphs = json.loads(json_text)['data']

    salesGraph = pd.DataFrame(salesGraphs)

    sales_list = salesGraphs["salesGraphDtos"]

    # 1. DataFrame из списка
    df = pd.DataFrame(sales_list)

    # 2. Месяц в формат MM.YY
    df["month"] = (
        pd.to_datetime(df["reportMonthDt"], dayfirst=True)
        .dt.strftime("%m.%y")
    )

    df = df.drop(columns="reportMonthDt")

    # 3. Длинный формат
    df_long = df.melt(
        id_vars="month",
        var_name="metric",
        value_name="value"
    )

    # 4. Формируем имена колонок
    df_long["column"] = df_long["month"] + "-" + df_long["metric"]

    # 5. Собираем всё в одну строку
    result = (
        df_long
        .set_index("column")["value"]
        .to_frame()
        .T
    )

    result.insert(0, "building_id", building_id)

    print(result)
    rows.append(result)

final_df = pd.concat(rows, ignore_index=True)

final_df.to_excel(
    "sales_all_buildings.xlsx",
    index=False
)