import subprocess
import sys
import codecs
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import colorlog

handler = colorlog.StreamHandler(sys.stdout)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s | %(levelname)s | %(message)s",
    log_colors={
        'DEBUG': 'white',
        'INFO': 'white',
        'WARNING': 'white',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
    reset=True
)

handler.setFormatter(formatter)

logger = logging.getLogger("runner")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer)

# папка со скриптами
SCRIPTS = [
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\3С Групп\3S_Group.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\А101\A101.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Абсолют\Absolute.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Абсолют\luzhniki.py"),
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
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Афи\Afi Tower.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Афи\odinburg.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Афи\sirenevy park.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Берендей\Троицкая слобода.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Бесткон\Bestcon.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Брусника\Brusnika.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\БТР Групп\kit.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Веспер\Vesper.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ВиХолдинг\Алиа.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ГАЛС\HALS.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Гефест\ekograd.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ГК Мега-мечта\Мечта.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ГК Монолит\elyon.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ГК Развитие\malahovsky.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ГК Развитие\onegin.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Глоракс\Аура Белорусская.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Глоракс\Олимп.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Горакс\Смарт Гарден.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Гравион\Cult.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Град\ICE TOWERS.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Град\Лесная коллекция.py"),
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
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Империал\iliyn.py"),
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
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Массиер-Девелопмент\ул. Советская 18.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\MR\MR.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Некрасовка Девелопмент\Nekrasovka.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Неострой\Тургенев.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Новая эра\Код Сокольники.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Новое время\Vostok 2.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ОМ\Новые островцы.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ОМ\Станиславский.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Основа\Osnova.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ПИК\Pik.py"),
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
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Sminex\Sminex.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\СМУ 6\smu6.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Спсити\moscowsky.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Стадион Спартак\Примавера.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Стоун\Сокольники.py"),
    Path(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Стоун\Стоун Rise.py"),
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




]

LOG_DIR = Path("All/logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("runner")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# 🔹 Консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 🔹 Файл с ротацией
file_handler = RotatingFileHandler(
    LOG_DIR / "run_all.log",
    maxBytes=5_000_000,  # 5 MB
    backupCount=5,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



for script in SCRIPTS:
    if not script.exists():
        raise FileNotFoundError(f"Скрипт не найден: {script}")
    logging.info(f"===== Запуск {script.name} =====")

    process = subprocess.Popen(
        ["python", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1
    )

    for line in process.stdout:
        logger.info(f"{script.name} | {line.rstrip()}")

    return_code = process.wait()

    if return_code != 0:
        logging.error(f"{script.name} завершился с кодом {return_code}")
    else:
        logging.info(f"{script.name} выполнен успешно")

logging.info("Все скрипты обработаны")