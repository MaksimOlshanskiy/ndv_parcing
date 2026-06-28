import datetime
import pdfplumber
import pandas as pd
import requests
from io import BytesIO
import re
from functions import save_flats_to_excel

'''
Заходим на сайт https://stonebrokers.ru/documents/price_lists
Там ищем ссылки на жилые проекты стоун. Грэйн, Райз, Сокольники. Скоро добавится ещё Блик
Эти ссылки подставляем ниже в url
Также вручную указываем названия проектов
'''



url = 'https://stone-s3.storage.yandexcloud.net/STOUN_Sokolniki_Ritejl_553383_Prajs_list_4308f65bac.pdf'

response = requests.get(url)
pdf_file = BytesIO(response.content)

all_rows = []

with pdfplumber.open(pdf_file) as pdf:

    for page in pdf.pages:

        # Получаем текст страницы
        page_text = page.extract_text() or ""

        # Ищем номер корпуса
        match = re.search(r'Корпус\s+([^\s\n]+)', page_text)

        if match:
            corpus = match.group(1)
        else:
            corpus = None

        # Получаем таблицы страницы
        tables = page.extract_tables()

        for table in tables:

            if not table or len(table) < 2:
                continue

            headers = [str(x).strip() if x else '' for x in table[0]]

            if 'Лот' not in headers:
                continue

            for row in table[1:]:

                if not row or not row[0]:
                    continue

                row = [datetime.date.today(), 'СТОУН Сокольники', '', '', '', '', '', '', '', '', '', '',
                          '', '', '', '', '', 'Стоун', '', '', '', '', corpus, '', '', '', '',
                          '', '', type, 'с отделкой', '', row[1], '', row[3].replace(' ', '').strip(), '', '', row[3].replace(' ', '').strip(),
                          '', '1', row[0]]
                all_rows.append(row)



df = pd.DataFrame(all_rows)

save_flats_to_excel(all_rows, 'СТОУН Сокольники', 'Стоун')