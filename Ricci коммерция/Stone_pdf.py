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

import pdfplumber

print(pdfplumber.__version__)

import pdfminer
print(pdfminer.__version__)

pdf_path = r"C:\Users\Mi\Downloads\СТОУН_Грэйн___Ритейл.pdf"

import pypdfium2 as pdfium

pdf = pdfium.PdfDocument(pdf_path)

page = pdf[0]
textpage = page.get_textpage()

text = textpage.get_text_range()
print('pypdfium2')
print(text[:1000])


all_rows = []

with pdfplumber.open(pdf_path) as pdf:

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
        print(f'Страница {page.page_number}: найдено {len(tables)} таблиц')

        for table in tables:

            for i, table in enumerate(tables):
                print(f'\nТаблица {i + 1}')
                print(table)

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