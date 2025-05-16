# Модуль вспомогательных функций проекта.
import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

# Создаём логгер для вспомогательных функций модуля views
logger = logging.getLogger("views")  # Создание объекта логгера для модуля views
logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования
console_handler = logging.StreamHandler()  # Создание обработчика с выводом в консоль
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter(
    fmt="%(asctime)s %(filename)s, %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)  # Настраиваем форматер
console_handler.setFormatter(console_formatter)  # Устанавливаем форматер
logger.addHandler(console_handler)  # Добавляем хэндлер в логгер


# Создаём вспомогательные функции модуля views
# Функция преобразования пользовательской строки с датой
def date_convert(user_date: str) -> datetime.datetime:
    """Функция принимает строку даты в формате 'YYYY-MM-DD HH:MM:SS' и преобразовывает в datetime"""
    logger.info(f"Func <{date_convert.__name__}> started.")
    try:
        date_obj = datetime.datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")  # Переводим str в datetime
        logger.info(f"Func <{date_convert.__name__}> successfully completed. Return: >{date_obj}<")
    except ValueError as e_1:  # Если строка с датой некорректна используем стандартную строку
        logger.error(f"{e_1}. The date '2021-02-13 13:00:00' will be used.")
        date_obj = datetime.datetime.strptime("2021-02-13 13:00:00", "%Y-%m-%d %H:%M:%S")
    return date_obj


# Функция приветствия
def greeting(date_obj: datetime.datetime) -> str:
    """
    Функция принимает дату и время в формате 'datetime' и возвращает строку приветствия с учётом времени суток.
    """
    logger.info(f"Func <{greeting.__name__}> started.")
    greet_str = ""
    if date_obj.hour >= 6 and date_obj.hour < 12:
        greet_str = "Доброе утро"
    elif date_obj.hour >= 12 and date_obj.hour < 18:
        greet_str = "Добрый день"
    elif date_obj.hour >= 18 and date_obj.hour < 24:
        greet_str = "Добрый вечер"
    elif date_obj.hour >= 0 and date_obj.hour < 6:
        greet_str = "Доброй ночи"
    logger.info(f"Func <{greeting.__name__}> successfully completed. Returned: >{greet_str}<")
    return greet_str


# Функция считывания и фильтрации excel файла по дате
def read_excel_monthly(path_to_data: str, date_obj: datetime.datetime) -> pd.DataFrame:
    """
    Функция считывания операции из Excel файла и фильтрации по дате (с 1го числа месяца по заданное).
    Аргументы функции: путь до файла, дата в формате YYYY-MM-DD HH:MM:SS
    """
    logger.info(f"Func <{read_excel_monthly.__name__}> started.")
    try:
        df = pd.read_excel(path_to_data, engine="openpyxl")  # Обращаемся к файлу .xlsx
        if "Дата операции" in df.columns:  # Если колонка существует, то фильтруем даты за текущий месяц
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
            filtered_df = df[
                (df["Дата операции"] >= datetime.datetime(date_obj.year, date_obj.month, 1))
                & (df["Дата операции"] <= datetime.datetime(date_obj.year, date_obj.month, date_obj.day))
            ]
            logger.info(f"Func <{read_excel_monthly.__name__}> successfully completed. Returned OK DF")
            return filtered_df
        else:
            columns = [
                "Дата операции",
                "Дата платежа",
                "Номер карты",
                "Статус",
                "Сумма операции",
                "Валюта платежа",
                "Кэшбэк",
                "Категория",
                "МСС",
                "Описание",
                "Бонусы (включая кэшбэк)",
                "Округление на инвесткопилку",
                "Сумма операции с округлением",
            ]
            empty_df = pd.DataFrame(columns=columns)  # Если колонки нет, то возвращаем пустой df
            logger.error("Column 'Дата операции' not found.")
            return empty_df
    except FileNotFoundError as e_2:  # Если файл не найден, то возвращаем пустой df
        columns = [
            "Дата операции",
            "Дата платежа",
            "Номер карты",
            "Статус",
            "Сумма операции",
            "Валюта платежа",
            "Кэшбэк",
            "Категория",
            "МСС",
            "Описание",
            "Бонусы (включая кэшбэк)",
            "Округление на инвесткопилку",
            "Сумма операции с округлением",
        ]
        empty_df = pd.DataFrame(columns=columns)
        logger.error(f"{e_2}. Returned empty DF")
        return empty_df
