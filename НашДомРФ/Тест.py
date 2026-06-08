import time
from datetime import datetime

import pandas as pd
from openpyxl.utils.datetime import to_excel
from playwright.sync_api import sync_playwright


def get_dates(result):
    construction_dates = []
    commissioning_dates = []

    for doc in result.get("data", []):

        date_str = doc.get("docObjRnsIssueDt")

        if not date_str:
            continue

        dt = datetime.strptime(date_str, "%d-%m-%Y %H:%M")

        if doc.get("description") == "Разрешение на строительство":
            construction_dates.append(dt)

        elif doc.get("description") == "Разрешение на ввод":
            commissioning_dates.append(dt)

    return (
        min(construction_dates).date() if construction_dates else None,
        min(commissioning_dates).date() if commissioning_dates else None,
    )

ids = ['68831', '71592', '58854', '71392', '66807', '71445', '71031', '71505', '71440', '57752', '71032', '50764', '66931', '62677', '71525', '63966', '50516', '71828', '51572', '47112', '50517', '70084']

list_of_results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    # Открываем страницу объекта
    page.goto(
        "https://наш.дом.рф/сервисы/каталог-новостроек/объект/35121"
    )

    # Ждем полной загрузки
    page.wait_for_load_state("networkidle")
    time.sleep(8)

    for project_id in ids:
        # Выполняем fetch внутри браузера
        result = page.evaluate(
            """
            async (projectId) => {
                const r = await fetch(
                    `/сервисы/api/object/${projectId}/document/permits`,
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

        print(result)

        construction_date, commissioning_date = get_dates(result)
        print(construction_date)
        print(commissioning_date)
        temp = [project_id, construction_date, commissioning_date]
        list_of_results.append(temp)


        time.sleep(1)

df = pd.DataFrame(list_of_results, columns=["project_id", "construction_date", "commissioning_date"])
df.to_excel("Хар-ки_080626.xlsx", index=False)


browser.close()