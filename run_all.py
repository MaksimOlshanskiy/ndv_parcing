import subprocess
import logging
from pathlib import Path

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










]

# логирование
LOG_DIR = Path("All/logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "run_all.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)



for script in SCRIPTS:
    if not script.exists():
        raise FileNotFoundError(f"Скрипт не найден: {script}")
    logging.info(f"===== Запуск {script.name} =====")

    process = subprocess.Popen(
        ["python", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1  # построчно
    )

    # stdout в реальном времени
    for line in process.stdout:
        logging.info(f"{script.name} | {line.rstrip()}")

    # stderr в реальном времени
    for line in process.stderr:
        logging.error(f"{script.name} | {line.rstrip()}")

    return_code = process.wait()

    if return_code != 0:
        logging.error(f"{script.name} завершился с кодом {return_code}")
    else:
        logging.info(f"{script.name} выполнен успешно")

logging.info("Все скрипты обработаны")