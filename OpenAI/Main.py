# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI
import base64
import os
from PIL import Image
import io
import requests
from datetime import datetime
from io import BytesIO
from OpenAI.Json import making_list_of_urls
import pandas as pd
import time

client = OpenAI(
    api_key="sk-4sG_gD4oYJ46qXzRY6IHH0ripNIcj4z82k4pjCSZbGw",
    base_url="https://api.zveno.ai/v1",
)

def load_image_from_url(url: str) -> bytes:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.content




def compress_image(image_bytes, max_size=1200, quality=85):

    img = Image.open(BytesIO(image_bytes))

    img.thumbnail((max_size, max_size))

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=quality)

    return buffer.getvalue()


def analyze_construction_stage(image_base64, prompt_text):

        try:
            for i in range(3):
                try:
                    response = client.chat.completions.create(
                    model="google/gemma-3-12b-it",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt_text},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}"
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=300,
                )

                    return response.choices[0].message.content
                except Exception as e:
                    print("Ошибка:", e)

                time.sleep(2)
        except:
            return 'Не удалось распознать'


def analyze_construction_stage_multi(images, prompt_text):

    content = [{"type": "text", "text": prompt_text}]

    for image in images:

        if isinstance(image, bytes):
            image_base64 = base64.b64encode(image).decode("utf-8")

        elif isinstance(image, str):
            image_base64 = image

        else:
            raise ValueError(f"Неподдерживаемый тип изображения: {type(image)}")

        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
            },
        })

    try:

        response = client.chat.completions.create(
            model="google/gemma-3-12b-it",
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
            max_tokens=300,
        )

        if not response.choices:
            print("API вернул пустой ответ:", response)
            return "Нет ответа модели"

        return response.choices[0].message.content

    except Exception as e:
        print("Ошибка OpenAI:", e)
        return "Ошибка анализа"


if __name__ == "__main__":

    prompt = """Тебе передано несколько фотографий одного и того же объекта
    с разных ракурсов. Проанализируй ВСЕ изображения и определи
    единую стадию строительной готовности.
    Если стадии на фото различаются, выбери наименее продвинутую.
    Ответь только названием стадии.
    Если строительство не началось, вырыт только котлован или возведено менее 5 этажей, то это начальная стадия.
    Если возвели более 5 этажей, ведётся монтаж стен и перекрытий, и не закончена полностью коробка здания, то это монтажные работы.
    Если здание достроено до крыши, ведётся остекление или ведутся фасадно-отделочные работы, или другие финальные работы, или фото сделано внутри здания, то это финальная стадия.
    """


    # images = [
    #     compress_image(r"C:\Users\m.olshanskiy\Desktop\Тест распознования стадий\1.jpeg"),
    #     compress_image(r"C:\Users\m.olshanskiy\Desktop\Тест распознования стадий\2.jpeg"),
    #     compress_image(r"C:\Users\m.olshanskiy\Desktop\Тест распознования стадий\3.jpeg"),
    #
    # ]
    #
    # stage = analyze_construction_stage_multi(images, prompt)


def process_corpus_id(corpus_id, prompt, year, month):

    photo_list = making_list_of_urls(corpus_id)
    target_prefix = f"{year}-{month:02d}"

    # 🔹 отбираем только фото за нужный месяц
    month_photos = [
        url for date_str, url in photo_list
        if date_str.startswith(target_prefix)
    ]

    if not month_photos:
        print(f"Нет фото за {month:02d}.{year} для {corpus_id}")
        return None

    # 🔹 берём максимум 3
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

    stage = analyze_construction_stage_multi(images, prompt)
    return stage

final_result = []
id_list = ['45969']

prompt = """Тебе передано несколько фотографий одного и того же объекта
    с разных ракурсов. Проанализируй ВСЕ изображения и определи
    единую стадию строительной готовности.
    Если стадии на фото различаются, выбери наименее продвинутую.
    Ответь только названием стадии.
    Если строительство не началось, вырыт только котлован или возведено менее 5 этажей, то это начальная стадия.
    Если возвели более 5 этажей, ведётся монтаж стен и перекрытий, и не закончена полностью коробка здания, то это монтажные работы.
    Если здание достроено до крыши, ведётся остекление или ведутся фасадно-отделочные работы, или другие финальные работы, или фото сделано внутри здания, то это финальная стадия.
    """

for corpus_id in id_list:
    stage = process_corpus_id(
        corpus_id,
        prompt,
        year=2026,
        month=2
    )
    print(f"{corpus_id} → Стадия строительства: {stage}")
    result = [corpus_id, stage]
    final_result.append(result)

df = pd.DataFrame(final_result, columns=[
    'ID дом.рф',
    'Стадия',
])

# Базовый путь для сохранения
base_path = rf"\\192.168.252.25\аналитики\ОТЧЕТЫ\Стадии.xlsx"

# Сохранение файла в папку
df.to_excel(base_path, index=False)

