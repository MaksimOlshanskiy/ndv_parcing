import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# --- Входные данные ---
target = 1_500_000   # цель накоплений (руб.)
initial = 100_000    # стартовый капитал (руб.)
annual_rate = 0.14   # 14% годовых
years = 9            # срок накоплений в годах
months = years * 12  # срок в месяцах

# --- Расчёт месячной доходности ---
monthly_rate = (1 + annual_rate) ** (1/12) - 1

# --- Рассчёт будущей стоимости стартового капитала ---
future_initial = initial * (1 + monthly_rate) ** months

# --- Сколько нужно накопить за счет ежемесячных взносов ---
needed_from_contributions = target - future_initial

# --- Ежемесячный взнос ---
monthly_contribution = needed_from_contributions * monthly_rate / ((1 + monthly_rate) ** months - 1)

print(f"Необходимо ежемесячно откладывать: {monthly_contribution:,.2f} руб.")

# --- Построение таблицы накоплений ---
balance = []
amount = initial
start_date = datetime(2025, 9, 1)  # Сентябрь 2025

for m in range(1, months + 1):
    # начисляем доход
    amount *= (1 + monthly_rate)
    # пополняем
    amount += monthly_contribution
    # вычисляем дату
    current_date = start_date + relativedelta(months=m-1)
    balance.append((m, current_date.month, current_date.year, amount))

df = pd.DataFrame(balance, columns=["Номер месяца", "Месяц", "Год", "Сумма на счёте"])

# --- Сохраняем в Excel ---
df.to_excel("накопления.xlsx", index=False)

print("Таблица сохранена в файл 'накопления.xlsx'")
