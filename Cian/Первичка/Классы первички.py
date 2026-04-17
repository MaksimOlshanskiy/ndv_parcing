import pandas as pd

# Загружаем файлы
df1 = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\Города млн\Апрель 2026\Первичка\Первичка_Млн_Апрель.xlsx")
df2 = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\Города млн\Апрель 2026\Города-миллионники_классы.xlsx")

for df in [df1, df2]:
    df['Название проекта'] = df['Название проекта'].str.replace(r"[\"'«»]", "", regex=True)

# создаём "очищенные" колонки (НЕ заменяя оригинальные)
for col in ['Название проекта', 'Локация']:
    df1[col + '_clean'] = df1[col].str.strip().str.lower()
    df2[col + '_clean'] = df2[col].str.strip().str.lower()

# merge по очищенным колонкам
result = df1.merge(
    df2[['Название проекта_clean', 'Локация_clean', 'Класс']],
    left_on=['Название проекта_clean', 'Локация_clean'],
    right_on=['Название проекта_clean', 'Локация_clean'],
    how='left',
    suffixes=('', '_new')
)

# если нужно заменить Класс
result['Класс'] = result['Класс_new']

# удаляем технические колонки
result = result.drop(columns=[
    'Название проекта_clean',
    'Локация_clean',
    'Класс_new'
])

result = pd.concat([
    result[~result['Локация'].isin(['Самарская область', 'Республика Башкортостан'])].drop_duplicates(),
    result[result['Локация'].isin(['Самарская область', 'Республика Башкортостан'])]
]).reset_index(drop=True)

# сохраняем
result.to_excel('result.xlsx', index=False)