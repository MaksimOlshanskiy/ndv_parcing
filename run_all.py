import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import requests
import time
from tqdm import tqdm


print(requests.get("https://ipinfo.io/json").json())
time.sleep(2)



MAX_PARALLEL = 10

# папка со скриптами

SCRIPTS = [
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ПИК\Pik.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\3С Групп\3S_Group.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\А101\A101.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Абсолют\Absolute.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Аверус\novograd monino.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Авиаспецресурс\vesna.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Агрострой\Novo-Nikolsk.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Аеон\aeon_kutuz.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Айкон\Новый Зеленоград.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Айкон\Сколково.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Аквилонинвест\AkvilonInvest_all.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\АМ Девелопмент\dom v malahovke.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Апсис Глоуб\CITIMIX.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Апсис Глоуб\CITIMIX Novokosino.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Ар Ди Ай\Ново-Молоково.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Ар Ди Ай\Южная долина.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Вектор\Vector_all.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Атлантис Скай\Odinchovo.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Афи\Afi.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Берендей\Троицкая слобода.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Бесткон\Bestcon.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Брусника\Brusnika.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\БТР Групп\kit.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Веспер\Vesper.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ВиХолдинг\Алиа.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ГАЛС\HALS.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Гефест\ekograd2.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Абсолют\luzhniki.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ГК Мега-мечта\Мечта.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ГК Монолит\elyon.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ГК Развитие\malahovsky.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ГК Развитие\onegin.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Глоракс\Аура Белорусская.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Глоракс\Олимп.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Горакс\Смарт Гарден.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Гравион\Cult.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Град\ICE TOWERS.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Гранд\klukveny.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Гранд\sobolevka.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Гранд\volkovskaya 67.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Гранд\Кашинцево.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Гранель\Granel.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Дар\Dar.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Дар\Dom.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Дело\pushkinograd.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Ди Эм Холдинг\preobrazhensky.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Догма\Догма new.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Доминанта\Dominanta_all.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Донстрой\Donstroy.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ФСК_1ДСК\main_1DSK.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Замитино\zamitino.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ИММО ДЕВЕЛОПМЕНТ\zeleny gorod.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Ин-Групп\Ценности.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Инвест траст\Новые ватутинки.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Инвестстрой\Отрадный.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Инград\Ingrad.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Каскад\kaskad park.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Квартал Инвестстрой\Новая Щербинка.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Киноквартал\Киноквартал.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Колди\Найс лофт.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Корпорация ВИТ\Триумф.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Крост\krost.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Level\Level.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Легион\ametist.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Ломоносов Девелопмент\mitischi city.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\М1 Девелопмент\М1 Сколково.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Мангазея\mangazeya.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Массиер-Девелопмент\ул. Советская 18 new.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\MR\MR.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Некрасовка Девелопмент\Nekrasovka.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Неострой\Тургенев.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Новая эра\Код Сокольники.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Новое время\Vostok 2.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ОМ\Новые островцы.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ОМ\Станиславский.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Основа\Osnova.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Плюс Девелопмент\detali.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Премьера\Оптима.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Проксима-1\Москворецкий (Тучково).py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Профи Инвест\Профи Инвест.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\РГ Девелопмент\rg-dev.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\РК-Газсетьсервис\podlipki.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\РКП\frunzensky.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Родина доделать все\peredelkino_2.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Родина доделать все\Rodina_park.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\РосЕвроСити\pushkino.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\РосЕвроСити\sholohovo.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Рост\Новое Летово.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Русич\Русич весь.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Сан Майкл\st.michael.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Сбер Капитал\1864.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\СЗ Риверхаус\river house.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\СЗ Рублево-Архангельское\Сберсити.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\СЗ Сантерра\sunterra.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\СЗ Северный квартал\Северный квартал.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Сибпромстрой\moscow.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Сити 21\8klenov.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Сити 21\Rafinad.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Сити 21\Аристов берег.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Sminex\Sminex.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Upside Development\smu6.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Спсити\moscowsky.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Стадион Спартак\Примавера.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Стоун\Stone.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Строй мир\Dius.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\СтройИнновация\andreevka.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Талан\Инджой.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Ташир\Deco Residence.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Ташир\Legacy.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Ташир\stellarcity.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Ташир\west tower.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Текта\tekta.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Точно\Юту.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Тренд Групп\duna.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Третий Рим\Patricks.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Тройка плюс\Все проекты.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Тройка РЭД\3-RED.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\УНР 494\Marshall.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\УНР 494\renessans.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Форма\forma.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ФСК_1ДСК\main_FSK.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\BAZA Development\bestseller.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ЮР-Инвест\Бакеево Парк.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Юнион\Riga Hills New.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Энергостройинвест\energoinvest.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Центр-инвест\Городские истории.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Центр-инвест\Centr-invest_willtower.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Центр-инвест\Centr-invest_festival.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Хаттон\Лунар.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Хаттон\Дом Дуо.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Флагман\scrylia_1.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Флагман\scrylia_2.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\СЗ Глобалмытищи\barhat.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\СЗ Т-ОТЕЛЬ\adres.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\СтартСК\Времена года.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Пионер\high life2.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Пионер\opus.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Пионер\pride.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Пионер\shift.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Пионер\varshavskaya.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Upside Development\enigmia (upside).py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\РКС Девелопмент\Коллекция.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\РКС Девелопмент\Insider.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Карандаш\Октябрьский.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Остов\Авиатор.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ВЭМЗ-Эстейт\Бруно.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Атлантис Одинцово\Вяземы Парк.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\СЗ Спортивная 2Б\Сердце Лыткарино.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Веста\Кратовоград.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Палладио Групп\Аннабельс.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Гранард\Гранд фили.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Березовец\atlantis.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Джи3\Джи3.py"),



]

print(len(SCRIPTS))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

active_scripts = set()


def run_script(script):

    active_scripts.add(script.name)

    start = time.time()

    process = subprocess.Popen(
        ["python", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    for line in process.stdout:
        logging.info(f"{script.name} | {line.rstrip()}")

    return_code = process.wait()

    duration = round(time.time() - start, 1)

    active_scripts.remove(script.name)

    if return_code != 0:
        return script.name, duration

    return None, duration


failed_scripts = []

start_all = time.time()

with ThreadPoolExecutor(MAX_PARALLEL) as executor:

    futures = [executor.submit(run_script, s) for s in SCRIPTS]

    with tqdm(total=len(SCRIPTS), desc="Парсеры", ncols=100) as pbar:

        for future in as_completed(futures):

            result, duration = future.result()

            if result:
                failed_scripts.append(result)

            pbar.update(1)

            pbar.set_postfix({
                "active": len(active_scripts),
                "running": list(active_scripts)[:3]
            })

total_time = round(time.time() - start_all, 1)

print("\n===== РЕЗУЛЬТАТ =====")
print(f"Всего скриптов: {len(SCRIPTS)}")
print(f"Время выполнения: {total_time} сек")

if failed_scripts:
    print(f"Упали: {failed_scripts}")
else:
    print("Все скрипты выполнены успешно")