from selenium import webdriver
import json
from datetime import datetime
import time
import openpyxl
import os
import random
import requests
import json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from openpyxl.utils.datetime import to_excel
from playwright.sync_api import sync_playwright

def making_list_of_urls(project_id):


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


        # Выполняем fetch внутри браузера
        result = page.evaluate(
            """
            async (projectId) => {
                const r = await fetch(
                    `/сервисы/api/object/${projectId}/document/rpd`,
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



        time.sleep(1)

    url_list = []

    for i in result["data"]:

        date = i['rpdIssueDttm']
        link = i['rpdPdfLink']
        pd_number = i['rpdNum']
        print([date, link, pd_number])
        url_list.append([date, link, pd_number])

    return url_list


