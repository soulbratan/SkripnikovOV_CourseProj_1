# Модуль с основной логикой функции для отчётов веб-страниц:
# (Траты по категории, Траты по дням недели, Траты в рабочий/выходной день).
# Собирает вспомогательные функции из utils.py в одну.
from src.utils import report_to_file, date_convert, read_excel_transactions
import pandas as pd
from typing import Optional
import datetime
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования
console_handler = logging.StreamHandler()  # Создание обработчика с выводом в консоль
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter(
    fmt="%(asctime)s %(filename)s, %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)  # Настраиваем форматер
console_handler.setFormatter(console_formatter)  # Устанавливаем форматер
logger.addHandler(console_handler)  # Добавляем хэндлер в логгер


@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    Аргументы:
    - transactions: дфрейм с транзакциями
    - category: название категории
    - date: опциональная дата (если не передана, берется текущая дата), если невалидный ввод, то (2021-02-12 13:00:00)
    Возвращает:
    - Датафрейм с тратами по указанной категории за последние 3 месяца
    """
    logger.info(f"Func <{spending_by_category.__name__}> started.")
    if date is None:
        end_date = datetime.datetime.now()
    else:
        end_date = date_convert(date)
    logger.info(f"End_date data is <{end_date}>.")
    start_date = end_date - datetime.timedelta(days=90)
    logger.info(f"Start_date data is <{start_date}>.")
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S",
                                                   errors="coerce")
    filtered = transactions[
        transactions["Категория"].str.lower().str.contains(category.lower(), na=False) &
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date)
        ].reset_index(drop=True)
    logger.info(f"Func <{spending_by_category.__name__}> completed.")
    return filtered

