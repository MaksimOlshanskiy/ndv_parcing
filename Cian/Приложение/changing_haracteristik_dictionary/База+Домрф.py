import pandas as pd
import numpy as np


def six_months_passed(date_value):
    if pd.isna(date_value):
        return False
    return date_value + pd.DateOffset(months=6) <= pd.Timestamp.today()

# Загружаем файлы
df1 = pd.read_excel(r"\\192.168.252.25\аналитики\ОТЧЕТЫ\База изменяемые данные.xlsx")
df1 = df1.drop(columns=[
    "Распроданность квартир",
    "Количество квартир",
    "Жилая площадь, м²",
    "Дата публикации проекта",])
df2 = pd.read_excel(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\НашДомРФ\2026-01-14\НашДомРФ_глубже_МО.xlsx")

print(df1.info())


df1["ID дом.рф"] = df1["ID дом.рф"].apply(
    lambda x: str(x).replace(".0", "") if pd.notna(x) else pd.NA
)

df2["ID дом.рф"] = df2["ID дом.рф"].apply(
    lambda x: str(x).replace(".0", "") if pd.notna(x) else pd.NA
)

print(df1.info())

# Перечень колонок из второго файла, которые нужно добавить
needed_cols = [
    "Ввод в эксплуатацию",
    "Распроданность квартир",
    "Количество квартир",
    "Жилая площадь, м²",
    "Дата публикации проекта",
]

# Делаем merge по ID
# Выполняем merge по 'ID дом.рф'
merged = df1.merge(
    df2[["ID дом.рф"] + needed_cols],
    on="ID дом.рф",
    how="left"
)

print(merged.columns.tolist())

# === 0. Подставляем "Срок сдачи" из "Срок сдачи старый", если пусто ===
merged['Ввод в эксплуатацию'] = merged['Ввод в эксплуатацию'].fillna(merged['Срок сдачи'])

# === 1. Проставляем 'Стадия строительной готовности' ===
merged['Стадия строительной готовности'] = merged['Стадия строительной готовности'].copy()

merged.loc[
    merged['Дата публикации проекта'] == 'Сдан',
    'Стадия строительной готовности'
] = 'введен'

# === 2. Проставляем 'Договор' ===
merged['Договор'] = merged['Стадия строительной готовности'].apply(
    lambda x: 'ДКП' if x == 'введен' else 'ДДУ')

merged['Жилая площадь, м²'] = merged['Жилая площадь, м²'].str.replace('ш', '')

merged["Количество квартир"] = (
    merged["Количество квартир"]
    .astype(str)
    .str.replace(r"\D", "", regex=True)   # удаляем всё, что не цифра
    .replace("", None)                    # пустые строки → NaN
    .astype("Int64")                      # безопасный int с поддержкой NaN
)

# очищаем столбец "Жилая площадь, м²"
merged["Жилая площадь, м²"] = (
    merged["Жилая площадь, м²"]
    .astype(str)
    .str.replace(r"\D", "", regex=True)   # удаляем всё, что не цифра (включая ш)
    .replace("", None)
    .astype("Int64")
)

merged["Распроданность квартир"] = (((merged["Распроданность квартир"].astype(str).
                                    str.replace(r"\D", "", regex=True))
                                    .replace("", None))
                                    .astype("Int64"))

merged["Распроданность квартир"] = merged["Распроданность квартир"]/100

merged["Дата публикации проекта"] = pd.to_datetime(
    merged["Дата публикации проекта"],
    dayfirst=True,
    errors="coerce"   # 'Сдан' → NaT
)

base_url = "https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82/"
merged["Ссылка"] = merged["ID дом.рф"].apply(
    lambda x: base_url + str(x) if pd.notna(x) and str(x).strip() != "" else ""
)

# Сопоставление кварталов и последних дней
quarter_map = {
    "1": "03-31",
    "2": "06-30",
    "3": "09-30",
    "4": "12-31"
}

today = pd.Timestamp.today() # + pd.Timedelta(days=85)

def days_until_quarter(q):
    # Проверка на пустое значение или нестроковое
    if pd.isna(q) or not isinstance(q, str) or q.strip() == "":
        return np.nan
    parts = q.strip().lower().split()
    if len(parts) < 3:  # если формат неправильный
        return np.nan
    q_num, _, year = parts
    if q_num not in quarter_map:  # если квартал не 1-4
        return np.nan
    due_date = pd.to_datetime(f"{year}-{quarter_map[q_num]}")
    return (due_date - today).days

mask_changed = merged['Срок сдачи'].ne(merged['Ввод в эксплуатацию'])

if mask_changed.any():
    print(f"Меняем значение для {mask_changed.sum()} проектов")

# Создаём столбец с количеством дней до срока
merged.loc[mask_changed, "Дней_до_сдачи"] = (
    merged.loc[mask_changed, "Ввод в эксплуатацию"].apply(days_until_quarter)
)


mask_stage1 = (
    mask_changed
    & (merged['Стадия строительной готовности'] == 'начальный цикл')
    & (merged['Дней_до_сдачи'].notna())
)

mask_stage3 = (
    mask_changed
    & (merged['Стадия строительной готовности'] == 'монтажные работы')
    & (merged['Дней_до_сдачи'].notna())
)


merged.loc[mask_stage1, 'stage_2_date'] = (
    today + pd.to_timedelta(merged.loc[mask_stage1, 'Дней_до_сдачи'] / 3, unit='D')
)
merged.loc[mask_stage1, 'stage_3_date'] = (
    today + pd.to_timedelta(merged.loc[mask_stage1, 'Дней_до_сдачи'] * 2 / 3, unit='D')
)

merged.loc[mask_stage3, 'stage_3_date'] = (
    today + pd.to_timedelta((merged.loc[mask_stage3, 'Дней_до_сдачи'] / 2), unit='D')
)

# Удаляем ненужные столбцы
merged = merged.drop(
    columns=['Срок сдачи', 'Дней_до_сдачи'],
    errors='ignore'
)

# Переименовываем столбец
merged = merged.rename(
    columns={'Ввод в эксплуатацию': 'Срок сдачи'}
)

# замена стадии по сегодняшней дате

today = pd.Timestamp.today().normalize()

# 1. Завершающий цикл — самый приоритетный
mask_stage3 = merged['stage_3_date'].notna() & (today > merged['stage_3_date'])
merged.loc[mask_stage3, 'Стадия строительной готовности'] = 'завершающий цикл'

# 2. Монтажные работы
mask_stage2 = (
    merged['stage_2_date'].notna()
    & (today > merged['stage_2_date'])
    & ~mask_stage3
)
merged.loc[mask_stage2, 'Стадия строительной готовности'] = 'монтажные работы'

# Сохраняем результат
merged.to_excel(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\!changing_haracteristik_dictionary\file2_с_новым_сроком.xlsx", index=False)

print("Готово! Новый файл сохранён.")

