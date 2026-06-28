from selenium import webdriver
import json
import time
from playwright.sync_api import sync_playwright

ids = ['70095', '70357']

list_of_results = []

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


def making_list_of_urls(object_id, page):
    url_list = []
    project_id = str(object_id)
    # Выполняем fetch внутри браузера
    result = page.evaluate(
        """
        async (projectId) => {
            const r = await fetch(
                `/сервисы/api/object/construction/progress/photo/${projectId}`,
                {
                    headers: {
                        authorization: 'Basic MTpxd2U='
                    }
                }
            );

            return await r.json();
        }
        """,
        project_id
    )

    max_date_found = None

    for i in result:
        obj_id = i['objId']
        date = i['objPeriodDt']
        link = i['objPhotoUrl']

        url_list.append([date, link])
    return url_list

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    # Открываем страницу объекта
    page.goto(
        "https://наш.дом.рф/сервисы/каталог-новостроек/объект/35121"
    )

    # Ждем полной загрузки

    time.sleep(8)





