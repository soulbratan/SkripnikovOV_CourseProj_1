# Модуль вспомогательных функций проекта.
import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

# Создаём логгер для вспомогательных функций модуля views
logger = logging.getLogger(__name__)  # Создание объекта логгера
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


# Функция обработки DF для выдачи статистики по карте
def cards_statistic(df_transactions: pd.DataFrame) -> list[dict]:
    """
    Функция принимает DataFrame с транзакциями и возвращает статистику по каждой карте.
    Возвращает список словарей с номером карты, суммой трат и кэшбэк.
    """
    logger.info(f"Func <{cards_statistic.__name__}> started.")
    expenses = df_transactions[df_transactions["Сумма операции"] < 0].copy()  # Фильтруем траты (отриц. знач.)
    spending_by_card = expenses.groupby("Номер карты")["Сумма операции"].sum().reset_index()  # Групп карту и сумма
    spending_by_card["Сумма трат"] = spending_by_card["Сумма операции"] * -1  # Делаем положительное знач.
    spending_by_card["Кэшбэк"] = round(spending_by_card["Сумма трат"] / 100, 2)  # Считаем кэшбэк и округляем
    data_list = list()
    for i in range(len(spending_by_card)):  # Проходимся по DF и создаём словари для записи в список
        cards_data = {
            "last_digits": spending_by_card.iloc[i]["Номер карты"],
            "total_spent": round(spending_by_card.iloc[i]["Сумма трат"].item(), 2),
            "cashback": spending_by_card.iloc[i]["Кэшбэк"].item()
        }
        data_list.append(cards_data)
    logger.info(f"Func <{cards_statistic.__name__}> completed.")
    if data_list == []:
        data_list = [{}]
    return data_list


def top5_transactions(df_transactions: pd.DataFrame) -> list[dict]:
    """
    Функция принимает DataFrame с транзакциями и возвращает топ 5 транзакций по сумме.
    Возвращает список словарей: дата, сумма, категория, описание
    """
    logger.info(f"Func <{top5_transactions.__name__}> started.")
    success_tr = df_transactions[df_transactions["Статус"] == "OK"]  # Фильтруем успешные транзакции
    top5_tr = success_tr.iloc[success_tr["Сумма операции"].abs().argsort()[::-1]].head(5)  # Выбираем топ5 по сумме
    top5_list = list()
    for i in range(len(top5_tr)):  # Проходимся по строкам и перекладываем словари в новый список
        tr_data = {
            "date": top5_tr.iloc[i]["Дата операции"].strftime("%d.%m.%Y"),
            "amount": top5_tr.iloc[i]["Сумма операции с округлением"].item(),
            "category": top5_tr.iloc[i]["Категория"],
            "description": top5_tr.iloc[i]["Описание"]
        }
        top5_list.append(tr_data)
    logger.info(f"Func <{top5_transactions.__name__}> completed.")
    return top5_list