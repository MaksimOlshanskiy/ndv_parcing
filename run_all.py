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
    Path(r"C:\PycharmProjects\ndv_parcing\ПИК\Pik.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\3С Групп\3S_Group.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\А101\A101.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Абсолют\Absolute.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Аверус\novograd monino.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Авиаспецресурс\vesna.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Агрострой\Novo-Nikolsk.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Аеон\aeon_kutuz.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Айкон\Новый Зеленоград.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Айкон\Сколково.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Аквилонинвест\AkvilonInvest_all.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\АМ Девелопмент\dom v malahovke.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Апсис Глоуб\CITIMIX Novokosino.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Ар Ди Ай\Ново-Молоково.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Ар Ди Ай\Южная долина.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Вектор\Vector_all.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Атлантис Скай\Odinchovo.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Афи\Afi.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Берендей\Троицкая слобода.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Бесткон\Bestcon.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Брусника\Brusnika.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\БТР Групп\kit.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Веспер\Vesper.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ВиХолдинг\Алиа.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ГАЛС\HALS.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Гефест\ekograd2.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Абсолют\luzhniki.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ГК Мега-мечта\Мечта.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ГК Монолит\elyon.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ГК Развитие\malahovsky.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ГК Развитие\onegin.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Глоракс\Аура Белорусская.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Глоракс\Олимп.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Горакс\Смарт Гарден.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Гравион\Cult.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Град\ICE TOWERS.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Гранд\klukveny.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Гранд\sobolevka.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Гранд\volkovskaya 67.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Гранд\Кашинцево.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Гранель\Granel.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Дар\Dar.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Дар\Dom.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Дело\pushkinograd.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Ди Эм Холдинг\preobrazhensky.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Догма\Догма new.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Доминанта\Dominanta_all.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Донстрой\Donstroy.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ФСК_1ДСК\main_1DSK.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Замитино\zamitino.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ИММО ДЕВЕЛОПМЕНТ\zeleny gorod.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Ин-Групп\Ценности.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Инвест траст\Новые ватутинки.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Инвестстрой\Отрадный.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Инград\Ingrad.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Каскад\kaskad park.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Квартал Инвестстрой\Новая Щербинка.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ГК Монолит\Киноквартал.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Колди\Найс лофт.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Корпорация ВИТ\Триумф.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Крост\krost.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Level\Level.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Легион\ametist.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Ломоносов Девелопмент\mitischi city.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\М1 Девелопмент\М1 Сколково.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Мангазея\mangazeya.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Массиер-Девелопмент\ул. Советская 18 new.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\MR\MR.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Некрасовка Девелопмент\Nekrasovka.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Неострой\Тургенев.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Новая эра\Код Сокольники.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Новое время\Vostok 2.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ОМ\Новые островцы.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ОМ\Станиславский.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Основа\Osnova.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Плюс Девелопмент\detali.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Премьера\Оптима.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Проксима-1\Москворецкий (Тучково).py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Профи Инвест\Профи Инвест.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\РГ Девелопмент\rg-dev.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\РК-Газсетьсервис\podlipki.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\РКП\frunzensky.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Родина доделать все\peredelkino_2.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Родина доделать все\Rodina_park.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\РосЕвроСити\pushkino.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\РосЕвроСити\sholohovo.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Рост\Новое Летово.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Русич\Русич весь.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Сан Майкл\st.michael.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Сбер Капитал\1864.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\СЗ Риверхаус\river house.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\СЗ Рублево-Архангельское\Сберсити.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\СЗ Сантерра\sunterra.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\СЗ Северный квартал\Северный квартал.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Сибпромстрой\moscow.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Сити 21\8klenov.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Сити 21\Rafinad.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Сити 21\Аристов берег.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Sminex\Sminex.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Upside Development\smu6.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Спсити\moscowsky.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Стадион Спартак\Примавера.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Стоун\Stone.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Строй мир\Dius.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\СтройИнновация\andreevka.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Талан\Инджой.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Ташир\Deco Residence.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Ташир\Legacy.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Ташир\stellarcity.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Ташир\west tower.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Текта\tekta.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Точно\Юту.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Тренд Групп\duna.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Третий Рим\Patricks.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Тройка плюс\Все проекты.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Тройка РЭД\3-RED.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\УНР 494\Marshall.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\УНР 494\renessans.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Форма\forma.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ФСК_1ДСК\main_FSK.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ЮР-Инвест\Бакеево Парк.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Юнион\Riga Hills New.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Энергостройинвест\energoinvest.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Центр-инвест\Городские истории.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Центр-инвест\Centr-invest_willtower.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Центр-инвест\Centr-invest_festival.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Хаттон\Лунар.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Хаттон\Дом Дуо.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Флагман\scrylia_1.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Флагман\scrylia_2.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\СЗ Глобалмытищи\barhat.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\СЗ Т-ОТЕЛЬ\adres.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\СтартСК\Времена года.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Пионер\high life2.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Пионер\opus.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Пионер\pride.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Пионер\shift.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Пионер\varshavskaya.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Upside Development\enigmia (upside).py"),
    Path(r"C:\PycharmProjects\ndv_parcing\РКС Девелопмент\Коллекция.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\РКС Девелопмент\Insider.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Карандаш\Октябрьский.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Остов\Остов.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\ВЭМЗ-Эстейт\Бруно.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Атлантис Одинцово\Вяземы Парк.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\СЗ Спортивная 2Б\Сердце Лыткарино.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Веста\Кратовоград.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Палладио Групп\Аннабельс.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Гранард\Гранд фили.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Березовец\atlantis.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Джи3\Джи3.py"),
    Path(r"C:\PycharmProjects\ndv_parcing\Первоград\Горки Марусино.py"),
    Path(r'C:\PycharmProjects\ndv_parcing\Сезар-Груп\Сезар Будущее.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\СЗ Сосновый парк\Новое Павлово.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\СЗ Энергостройинвест\Отлично.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\Юник девелопмент\Springs.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\Primacom\Внуково Кантри клаб.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\AVA\Городской бор.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\НДВ\Берег.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\НДВ\Восточный.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\НДВ\Гармония Парк.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\НДВ\Космос.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\НДВ\Красная горка.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\НДВ\Мишино.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\НДВ\Серебро.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\НДВ\Школьный.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\ГК Развитие\voroncovskiy.py'),
    Path(r'C:\PycharmProjects\ndv_parcing\Элемент\Тессинский 5.py')







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