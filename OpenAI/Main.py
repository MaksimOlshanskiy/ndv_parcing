# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from openai import OpenAI
import base64
import os
from PIL import Image
import io

client = OpenAI(
    api_key="sk-4sG_gD4oYJ46qXzRY6IHH0ripNIcj4z82k4pjCSZbGw",
    base_url="https://api.zveno.ai/v1",
)


def compress_image(image_path, max_size=1200, quality=85):
    """
    Уменьшает изображение по максимальной стороне
    и возвращает base64 строку.

    max_size — максимальный размер большей стороны (px)
    quality — качество JPEG (1-95)
    """

    img = Image.open(image_path)

    # уменьшаем пропорционально
    img.thumbnail((max_size, max_size))

    # сохраняем в буфер
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)

    # получаем base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return image_base64


def analyze_construction_stage(image_base64, prompt_text):

    response = client.chat.completions.create(
        model="openai/gpt-4o",
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

def analyze_construction_stage_multi(image_base64_list, prompt_text):

    content = [{"type": "text", "text": prompt_text}]

    # добавляем все изображения
    for image_base64 in image_base64_list:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
            },
        })

    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        max_tokens=300,
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    prompt = """Тебе передано несколько фотографий одного и того же объекта
    с разных ракурсов. Проанализируй ВСЕ изображения и определи
    единую стадию строительной готовности.
    Если стадии на фото различаются, выбери наиболее продвинутую.
    Ответь только названием стадии.
    Если строительство не началось, вырыт только котлован или возведены максимум три этажа, то это начальная стадия.
    Если возвели более трёх этажей, и крыша ещё не закончена, окна ещё не начали вставлять то это монтажные работы.
    Всё остальное это финальная стадия.
    """


    images = [
        compress_image(r"C:\Users\m.olshanskiy\Desktop\7D6375EBA2754CF894666C8675D5989B.jpeg"),
        compress_image(r"C:\Users\m.olshanskiy\Desktop\0185006A74C64272B461133A6100977D.jpeg"),
        compress_image(r"C:\Users\m.olshanskiy\Desktop\EC2938E034FF4FC8A0B6827F44B44B59.jpeg"),
    ]

    stage = analyze_construction_stage_multi(images, prompt)
    print("Стадия строительства:", stage)