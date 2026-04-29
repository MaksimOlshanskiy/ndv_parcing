import json

# Загрузка исходного JSON
with open('typology_all_updated.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Словари и множества как в твоем коде
suffixes = [
    '(терр.)', '(терр.+бассейн)', '(терр)', ' терр', ' терр.', ' (антресоль)', ' (патио)', ' city house',
    ' (ситихаус)', '(терр.)', '(терр.)'
]

taun_variants = ['(таун)', 'таун', 'таунхаус', '(таунхаус)', 'таунхаусы', '(вилла)']

level_replacements = {
    'к2L': '2 ур',
    'л': '2 ур',
    'L': '2 ур',
    '2-ур': '2 ур',
    '2 ур.': '2 ур',
    '2 р.': '2 ур',
    '2ур.': '2 ур',
    '2ур': '2 ур'
}

def normalize(value):
    original = value
    if isinstance(value, str):
        val = value.strip()

        if val == '6еL (терр.)':
            val = '6еL'

        # Если есть любой из таунхаус-вариантов — заменяем всё значение
        if any(variant in val for variant in taun_variants):
            val = 'таунхаус'
        else:
            # Удаляем суффиксы
            for suffix in suffixes:
                if val.endswith(suffix):
                    val = val[:-len(suffix)].strip()
                    break

        # Заменяем 'ph' на 'пент.'
        if 'ph' in val:
            return 'пентхаус'
        if 'пент.' in val:
            return 'пентхаус'

        # Спец. случай для 'к2L'
        if 'к2L' in val:
            parts = val.split('к2L')
            if parts[0] and parts[0][-1].isdigit():
                val = f"{parts[0]} 2 ур{' '.join(parts[1:])}"
            else:
                val = ' '.join(parts) + ' 2 ур'

        # Остальные замены уровня
        for variant, replacement in level_replacements.items():
            if variant != 'к2L' and variant in val:
                val = val.replace(variant, replacement)

        # Перенос "2 ур" в конец
        if '2 ур' in val:
            parts = [p.strip() for p in val.split('2 ур') if p.strip()]
            count = val.count('2 ур')
            val = ' '.join(parts) + ' 2 ур' * count

        val = val.replace('4е2 2 ур', '4е 2 ур')
        val = val.replace('2 4e 2 ур', '4e 2 ур')
        val = val.replace('6е (терр.) 2 ур', '6е 2 ур')
        val = val.replace('пентхаусы', 'пентхаус')
        val = val.replace('e', 'е')  # латинскую 'e' на кириллическую
        val = val.strip()

        try:
            return int(val)
        except ValueError:
            return val
    else:
        return value  # уже int

# Создание нового словаря с нормализованными значениями
normalized_data = {}

for project, flats in data.items():
    normalized_data[project] = {}
    for area, val in flats.items():
        normalized_value = normalize(val)
        normalized_data[project][area] = normalized_value

# Сохраняем результат
with open('normalized_output.json', 'w', encoding='utf-8') as f:
    json.dump(normalized_data, f, ensure_ascii=False, indent=2)
