# Модуль вспомогательных функций проекта.
import pandas as pd
import datetime
import logging
import os
import requests
from dotenv import load_dotenv
import json


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
def date_conversion(user_date: str) -> datetime.datetime:
    """Функция принимает строку даты в формате 'YYYY-MM-DD HH:MM:SS' и преобразовывает в datetime"""
    logger.info(f"Func <{date_conversion.__name__}> started.")
    try:
        date_obj = datetime.datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")  # Переводим str в datetime
        logger.info(f"Func <{date_conversion.__name__}> successfully completed. Return: >{date_obj}<")
    except ValueError as e_1:  # Если строка с датой некорректна используем стандартную строку
        logger.error(f"{e_1}. The date '2021-02-13 13:00:00' will be used.")
        date_obj = datetime.datetime.strptime("2021-02-13 13:00:00", "%Y-%m-%d %H:%M:%S")
    return date_obj
# Функция приветствия
