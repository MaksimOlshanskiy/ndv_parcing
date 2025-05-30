import re




def classify_renovation(description: str) -> str:

    description = description.lower()

    # Категории ремонтов
    has_renovation = [
        "с отделкой", "свежий ремонт", "качественный ремонт", "с ремонтом",
        "евроремонт", "под ключ", "дизайнерский ремонт", "новый ремонт",
        "капитальный ремонт", "современный ремонт", "полностью отремонтирована",
        "после ремонта", "отличный ремонт", "хороший ремонт", "недавно сделан ремонт",
        "люкс ремонт", "высококачественная отделка", "эксклюзивный ремонт",
        "стильный ремонт", "авторский дизайн", "ремонт класса люкс",
        "дорогой ремонт", "ремонт бизнес-класса", "реновация",
        "квартира в идеальном состоянии", "хорошем жилом состоянии",
        "хорошем состоянии", "отличном состоянии", "меблирован", "с мебелью", "с техникой", 'чистовой отделкой',
        'чистовая отделка', 'отделка апартаментов выполнена', 'отделка квартир выполнена', 'отделка осуществляется',
        'отделка выполнена'
    ]

    no_renovation = [
        "без отделки", "без ремонта", "требуется ремонт", "нужен ремонт",
        "под ремонт", "нежилое состояние", "убитая квартира", "старый ремонт",
        "состояние от застройщика", "плохой ремонт", "оригинальное состояние",
        "под замену", "надо делать ремонт", "под восстановление",
        "обветшалый ремонт", "ремонт отсутствует", "разрушенное состояние",
        "без отделочных работ", "голые стены", "стены без отделки"
    ]

    rough_finishing = [
        "черновая отделка", "предчистовая отделка", "white box", "предчистовой ремонт",
        "стройвариант", "под чистовую отделку", "без чистовой отделки", "без ремонта от застройщика",
        "в бетоне", "без финишной отделки", "предчистовая подготовка",
        "стены под покраску", "готово к отделке", "штукатурка стен",
        "без напольного покрытия", "стяжка и штукатурка", 'предчистовой отделкой', 'white-box', 'получистовая'
    ]

    # Проверяем ключевые слова
    for phrase in has_renovation:
        if re.search(rf"\b{phrase}\b", description):
            return "С отделкой"

    for phrase in no_renovation:
        if re.search(rf"\b{phrase}\b", description):
            return "Без отделки"

    for phrase in rough_finishing:
        if re.search(rf"\b{phrase}\b", description):
            return "Предчистовая"

    return "Не удалось определить"

def clean_filename(name: str, max_length: int = 255) -> str:
    # Удаляем запрещённые символы для Windows
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Зарезервированные имена (например, CON.xlsx)
    reserved = {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)), *(f'LPT{i}' for i in range(1, 10))}
    # Удаляем пробелы в начале и конце
    name = name.strip()
    # Удаляем расширение перед проверкой имени
    base = name.rsplit('.', 1)[0]
    # Переименовываем зарезервированные
    if base.upper() in reserved:
        base = f"{base}_safe"
    # Возвращаем с ограничением длины

    base = base.replace('ЖК ', '')  # Убираем 'ЖК '
    base = base.strip('«»"')  # Убираем кавычки «», ""

    return f"{base[:max_length - 5]}.xlsx"  # 5 символов под ".xlsx"