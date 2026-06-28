# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI
import base64
import os
from PIL import Image
from PIL import ImageOps
import io
import requests
from datetime import datetime
from io import BytesIO
from OpenAI.Json import making_list_of_urls
import pandas as pd
import time
from playwright.sync_api import sync_playwright
import json

["google/gemini-2.5-flash-lite", "openai/gpt-4.1-nano"]

model = "google/gemini-2.5-flash"

with open(r'C:\PycharmProjects\ndv_parcing\!changing_haracteristik_dictionary\projects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    rows = []

    for buildings in data.values():
        for info in buildings.values():
            stage = (info.get("Стадия строительной готовности") or "").strip().lower()

            if stage in {"", "завершающий цикл", "введен", "nan"}:
                continue

            rows.append({
                "ID дом.рф": info.get("ID дом.рф"),
                "Стадия строительной готовности": info.get("Стадия строительной готовности")
            })

    df = pd.DataFrame(rows)
    id_list = df['ID дом.рф'].dropna().unique().tolist()
    print(id_list)
    print(f'Количество id: {len(id_list)}')
    df = df.drop_duplicates(subset="ID дом.рф")

    df2 = pd.read_excel(r'C:\PycharmProjects\ndv_parcing\НашДомРФ\2026-06-23\НашДомРФ_глубже_23062026.xlsx')

    df['ID дом.рф'] = df['ID дом.рф'].astype(str)
    df2['ID дом.рф'] = df2['ID дом.рф'].astype(str)
    df = df.merge(
        df2[["ID дом.рф", 'Количество этажей']],
        on="ID дом.рф",
        how='left'
    )
    df['Количество этажей'] = df['Количество этажей'].astype('Int64')

    # df = pd.DataFrame({
    #     'ID дом.рф': ['62039', '64985', '57447', '60548', '70357', '70585'],
    #     'Стадия строительной готовности': [
    #         'монтажные работы',
    #         'монтажные работы',
    #         'монтажные работы',
    #         'монтажные работы',
    #         'монтажные работы',
    #         'начальный цикл'
    #     ],
    #     'Количество этажей': [23, 70, 31, 44, 14, 52]
    # })

    print(df.head())





max_tokens = 50

client = OpenAI(
    api_key="sk-4sG_gD4oYJ46qXzRY6IHH0ripNIcj4z82k4pjCSZbGw",
    base_url="https://api.zveno.ai/v1",
)

def load_image_from_url(url: str) -> bytes:
    response = requests.get(url, timeout=30)
    print(url)
    response.raise_for_status()
    return response.content




def compress_image(image_bytes, max_size=1024, quality=75):

    img = Image.open(BytesIO(image_bytes))

    # исправление поворота камеры
    img = ImageOps.exif_transpose(img)

    # конвертация для JPEG
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # уменьшение изображения
    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)

    return buffer.getvalue()

def analyze_construction_stage_multi(images, prompt_text, current_stage, floor):

    content = [{"type": "text", "text": prompt_text}]
    # for i, img in enumerate(images):
    #    print("image", i, "size:", len(img))

    for i, image in enumerate(images):

        if isinstance(image, bytes):
            image_base64 = base64.b64encode(image).decode("utf-8")

        elif isinstance(image, str):
            image_base64 = image

        else:
            raise ValueError(f"Неподдерживаемый тип изображения: {type(image)}")

        content.append({
            "type": "text",
            "text": f"Фотография {i + 1}"
        })

        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
            },
        })

    try:

        response = client.chat.completions.create(
            model=f"{model}",
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            max_tokens=int(f"{max_tokens}"),
        )

        if not response.choices:
            print("API вернул пустой ответ:", response)
            return "Нет ответа модели"

        return response.choices[0].message.content

    except Exception as e:
        print("Ошибка OpenAI:", e)
        return "Ошибка анализа"

 


def process_corpus_id(corpus_id, min_year, min_month, current_stage, floors):

    photo_list = making_list_of_urls(corpus_id, page=page)
    print(photo_list)
    min_date = datetime(min_year, min_month, 1)

    # преобразуем даты
    parsed_photos = []

    for date_str, url in photo_list:
        try:
            date_obj = datetime.strptime(date_str[:10], "%Y-%m-%d")
            if date_obj >= min_date:
                parsed_photos.append((date_obj, url))
        except:
            continue

    if not parsed_photos:
        print(f"Нет фото после {min_year}-{min_month:02d}")
        return None

    # 🔹 ищем самый новый месяц
    latest_date = max(d for d, _ in parsed_photos)

    latest_year = latest_date.year
    latest_month = latest_date.month

    # print("Последний месяц фото:", latest_year, latest_month)

    # 🔹 берём фото только этого месяца
    month_photos = [
        url for d, url in parsed_photos
        if d.year == latest_year and d.month == latest_month
    ]

    if not month_photos:
        return None

    selected_urls = month_photos[:5]

    images = []

    for url in selected_urls:
        try:
            image_bytes = load_image_from_url(url)
            compressed = compress_image(image_bytes)
            images.append(compressed)
        except Exception as e:
            print(f"Ошибка обработки {url}: {e}")

    if not images:
        return None


    prompt = f"""Передано {len(images)} фотографий одного строительного объекта с разных ракурсов.

Последняя достоверно определённая стадия: {current_stage}. Максимальная этажность будущего здания: {floors}.

Проанализируй все фотографии и определи текущую стадию строительной готовности объекта. Порядок стадий: Начальный цикл, Монтажные работы, Завершающий цикл.

ВАЖНЫЕ ОГРАНИЧЕНИЯ:

Если на фото несколько зданий, анализируй объект, находящийся в центре кадра.
Если часть фотографий неинформативна, игнорируй их.

ОПРЕДЕЛЕНИЕ СТАДИИ ВЫПОЛНЯЕТСЯ ТОЛЬКО ПО ЭТАЖНОСТИ.

Сначала найди максимальное количество видимых этажей среди всех фотографий.

Далее определи стадию строго по правилам:

если этажей < {round(floors*0.2)}:
    начальный цикл

если {round(floors*0.2)} <= этажей <= {round(floors*0.6)}:
    монтажные работы

если этажей > {round(floors*0.6)}:
    завершающий цикл

Запрещено использовать любые другие признаки для выбора стадии.

ОТВЕТ:

Верни одну из стадий без пояснений, через пробел, без лишних слов:
начальный цикл или монтажные работы или завершающий цикл
        """



    prompt_another = f"""Передано {len(images)} фотографий одного строительного объекта
            с разных ракурсов. Проанализируй каждую фотографию.

            Задача: определить стадию строительной готовности методом голосования.
            При определении высоты конструкции здания можно ориентироваться на другие объекты, например:    
            забор, деревья, строительную технику, бытовки. Если на фото несколько зданий - 
            ориентируйся по тому, что в центре фотографии, на переднем плане. 

            Алгоритм (выполняй мысленно, НЕ выводи промежуточные шаги):
            1. Для каждой фотографии определи стадию строительства.
            2. Подсчитай количество голосов за каждую стадию.
            3. Выбери стадию, получившую большинство голосов.
            4. Если голоса равны — выбери более продвинутую стадию.

            Возможные стадии и их визуальные признаки:

            Начальная стадия:
            - строительство не началось
            - Глубокий котлован (большая выемка грунта, видны откосы или вертикальные стенки, вокруг могут быть земляные насыпи)
            - Если строится цокольная часть дома или подвал, то это Начальная стадия
            - Отсутствие надземных этажей  (нет стен, перекрытий и каркаса здания выше уровня земли)
            - Фундаментные конструкции (На дне котлована могут быть: бетонная фундаментная плита, свайное поле, ростверки, армирование (сетка арматуры))
            - Строительная техника для земляных работ (Часто присутствуют: экскаваторы, самосвалы, буровые установки для свай)
            - Много открытого грунта (преобладает земля, песок, щебень, мало бетонных вертикальных конструкций)  
            - Любые бетонные конструкции, находящиеся внутри котлована или на уровне земли, относятся к фундаменту и считаются Начальной стадией.
            
            КРИТИЧЕСКОЕ ПРАВИЛО:

            Если на фотографии нет ни одного надземного этажа здания 
            (нет перекрытий или стен выше уровня земли),
            то стадия ВСЕГДА "Начальная стадия"       

            Монтажные работы начинаются ТОЛЬКО когда:
            - появляется хотя бы один этаж здания
            - есть перекрытие между этажами
            - стены или колонны поднимаются выше уровня земли        
            - есть надземные бетонные конструкции
            - появились вертикальные колонны
            - каркас открыт
            - нет фасада
            - много опалубки
            

            Финальная стадия:
            - каркас уже полностью построен или частично выполнен     
            ВАЖНО: если появилась часть фасада, утеплителя, то это финальная стадия       
            - частично или полностью установлены окна
            - могут быть: строительные люльки, фасадные панели, желтый утеплитель на фасаде
            - фасад может быть выполнен из стекла                         
            - если ВСЕ фотографии сделаны внутри здания
            - могут быть строительные леса или защитная ткань или защитное покрытие для обустройства фасада, но если каркас полностью не построен, то это не показатель 
            
            Перед определением стадии задай себе вопросы:
            Есть ли хотя бы один надземный этаж здания?
            Если нет — это Начальная стадия.
            Есть ли строительные леса или сетка или защитная ткань или защитное покрытие?
            Если да, то это Финальная стадия
            Начат ли монтаж фасада?
            Если да, то это Финальная стадия
            
            Отвечай ТОЛЬКО стадией строительной готовности, ничего больше не пиши
            
            
            """

    prompt2 = f"""Передано {len(images)} фотографий одного строительного объекта
            с разных ракурсов. Проанализируй каждую фотографию.

            Задача: определить стадию строительной готовности методом голосования.
            При определении высоты конструкции здания можно ориентироваться на другие объекты, например:    
            забор, деревья, строительную технику, бытовки. Если на фото несколько зданий - 
            ориентируйся по тому, что в центре фотографии, на переднем плане. 

            Алгоритм (выполняй мысленно, НЕ выводи промежуточные шаги):
            1. Для каждой фотографии определи стадию строительства.
            2. Подсчитай количество голосов за каждую стадию.
            3. Выбери стадию, получившую большинство голосов.
            4. Если голоса равны — выбери более продвинутую стадию.
    
    КЛЮЧЕВОЕ ПРАВИЛО ОТЛИЧИЯ СТАДИЙ:

    1. Если нет надземных этажей → Начальная стадия.

    2. Если есть надземные этажи, но здание ещё растёт
   и верхние этажи продолжают строиться → Монтажные работы.

    3. Финальная стадия возможна ТОЛЬКО если
   каркас здания полностью построен по высоте
   и новые этажи больше не возводятся.
   
   Отвечай ТОЛЬКО стадией строительной готовности
    
    
    """
    current_stage = current_stage
    stage = analyze_construction_stage_multi(images, prompt, current_stage, floors)
    return stage

final_result = []


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    # Открываем страницу объекта
    page.goto(
        'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82/61985'
    )

    # Ждем полной загрузки
    time.sleep(10)
    # id_list = ['62039', '64985', '57447', '60548', '70357', '70585']
    for corpus_id in id_list:
        print(df.columns.tolist())
        current_stage = df.loc[
            df['ID дом.рф'] == corpus_id,
            'Стадия строительной готовности'
        ].iloc[0]
        floors = df.loc[
            df['ID дом.рф'] == corpus_id,
            'Количество этажей'
        ].iloc[0]
        print(f"Предыдущая стадия: {current_stage}, этажность: {floors}")
        stage = process_corpus_id(
            corpus_id,
            min_year=2026,
            min_month=5,
            current_stage=current_stage,
            floors=floors
        )

        print(f"{corpus_id} → Стадия строительства: {stage}")
        result = [corpus_id, stage, current_stage, floors]
        final_result.append(result)

        time.sleep(1)




        df_res = pd.DataFrame(final_result, columns=[
            'ID дом.рф',
            'Стадия',
            'Предыдущая стадия',
            'Этажность'
        ])

        # Базовый путь для сохранения
        base_path = r"C:\PycharmProjects\ndv_parcing\OpenAI\СтадииLast2.xlsx"

        # Сохранение файла в папку
        df_res.to_excel(base_path, index=False)
        print('Файл сохранён')

