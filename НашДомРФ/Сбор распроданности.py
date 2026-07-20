import datetime
import pandas as pd
from selenium import webdriver
import json
import os
import time
from playwright.sync_api import sync_playwright

ids = [50874, 42767, 42025, 29765, 42026, 43061, 43062, 42443, 53778, 53780, 53769, 53776, 53779, 53770, 53771, 53772, 53773, 53774, 53775, 53777, 51054, 27645, 51187, 36568, 35909, 58891, 35613, 43489, 33907, 33908, 21336, 16732, 16735, 16734, 16733, 27569, 27563, 27561, 27567, 27562]

results_list = []
city = 'Самара'
date = datetime.date.today()
counter = 1

# def making_list_of_urls(corpus_id):
#     driver = webdriver.Chrome()
#     try:
#         url_list = []
#
#         url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/construction/progress/photo/{corpus_id}'
#         driver.get(url=url)
#
#         json_text = driver.find_element("tag name", "body").text
#         data = json.loads(json_text)
#
#         for i in data:
#             date = i['objPeriodDt']
#             link = i['objPhotoUrl']
#             url_list.append([date, link])
#
#         return url_list
#
#     finally:
#         driver.quit()  # закрываем браузер, даже если будет исключение




with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    # Открываем страницу объекта
    page.goto(
        "https://наш.дом.рф/сервисы/каталог-новостроек/объект/70357"
    )

    # Ждем полной загрузки

    time.sleep(8)


    for project_id in ids:


        offset = 0
        while True:
            project_id = str(project_id)
            # Выполняем fetch внутри браузера
            result = page.evaluate(
    """
    async ({ projectId, offset }) => {
        const r = await fetch(
            `https://xn--80az8a.xn--d1aqf.xn--p1ai/portal-kn/api/kn/objects/${projectId}/flats?flatGroupType=premises&limit=5&offset=${offset}`,
            {
                headers: {
                    authorization: 'Basic MTpxd2U='
                }
            }
        );
    
        return await r.json();
    }
    """,
    {"projectId": project_id, "offset": offset}
    )

            total_count = result["total"]
            for i in result['data']:
                type = i['type']
                floorNumber = i['floorNumber']
                price = i['price']
                status = i['status']
                totalArea = i['totalArea']
                print(f'{counter} из {len(ids)}', project_id, type, floorNumber, price, status, totalArea)
                res = [city, project_id, type, floorNumber, price, status, totalArea]
                results_list.append(res)
            offset +=5
            if offset > total_count:
                break
            time.sleep(1)
        counter += 1

df = pd.DataFrame(results_list, columns=['city','project_id', 'type', 'floorNumber', 'price', 'status', 'totalArea'])

# Базовый путь для сохранения
base_path = r"C:\PycharmProjects\ndv_parcing\НашДомРФ"

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f'{city}_Лоты.xlsx'

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)






