import pandas as pd
from scipy.optimize import newton


pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)

# === 1. Загрузка ===
df = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\Cash flow2.xlsx")

# === 2. Дата ===
df['Дата'] = pd.to_datetime(df['Дата'], dayfirst=True)


# === 3. CF ===
def calc_cf(row):
    t = row['Тип операции']
    details = str(row['Подробнее'])

    if 'Пополнение' in t:
        return -row['Приход']

    else:
        return 0


df['CF'] = df.apply(calc_cf, axis=1)

# === 4. Убираем нули ===
cf = df[df['CF'] != 0].copy()

# === 5. ДОБАВЛЯЕМ старт портфеля (ВАЖНО) ===
start_value = 41128  # ← стоимость на 01.03.2025
start_date = pd.Timestamp("2025-03-01")

cf = pd.concat([
    pd.DataFrame({'Дата': [start_date], 'CF': [-start_value]}),
    cf
])

# === 6. ДОБАВЛЯЕМ текущую стоимость ===
end_value = 125161  # ← текущая стоимость
end_date = pd.Timestamp.today()

cf = pd.concat([
    cf,
    pd.DataFrame({'Дата': [end_date], 'CF': [end_value]})
])

cf['Накопленный CF'] = cf['CF'].cumsum()


# === 7. XIRR ===
def xnpv(rate, values, dates):
    t0 = dates.iloc[0]
    return sum(v / (1 + rate) ** ((d - t0).days / 365) for v, d in zip(values, dates))


def xirr(values, dates):
    return newton(lambda r: xnpv(r, values, dates), 0.1)

cf_check = df.copy()

# Добавим CF в исходную таблицу
cf_check['CF'] = df['CF']

# Отсортируем по дате (важно для анализа)
cf_check = cf_check.sort_values('Дата')
cf_check['Накопленный CF'] = cf_check['CF'].cumsum()

# Сохраним
cf_check.to_excel("cf_check.xlsx", index=False)

print("Сумма CF:", cf['CF'].sum())
print("Мин CF:", cf['CF'].min())
print("Макс CF:", cf['CF'].max())

print(df.sort_values('Дата').head(10))


irr = xirr(cf['CF'], cf['Дата'])

print(f"Годовая доходность: {irr:.2%}")