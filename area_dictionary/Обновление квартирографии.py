import pandas as pd
import json

# Загружаем данные из Excel файла
df = pd.read_excel(r"\\192.168.252.25\аналитики\ОТЧЕТЫ\Квартирография_new.xlsx")  # укажите путь к вашему файлу

# Предполагаем, что колонки называются:
# 'Название проекта', 'Площадь', 'кол-во комнат'
# Если названия другие - замените их

# Приводим названия проектов к нижнему регистру
df['Название проекта'] = df['Название проекта'].str.lower()

# Сортируем внутри каждого проекта по площади (если 'Площадь, кв.м' — числовая)
df = df.sort_values(by=['Название проекта', 'Площадь, кв.м'])

# Группируем данные по названию проекта
result = {}
for project in df['Название проекта'].unique():
    # Фильтруем данные для текущего проекта
    project_data = df[df['Название проекта'] == project]

    # Создаем словарь площадь: тип_комнаты
    area_rooms = {}
    for _, row in project_data.iterrows():
        area = str(row['Площадь, кв.м'])  # преобразуем в строку для ключа
        room_type = row['Кол-во комнат']
        area_rooms[area] = room_type

    result[project] = area_rooms

# Сохраняем в JSON файл
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Данные успешно сохранены в output.json")