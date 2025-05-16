# Модуль тестирования программных функций
from src import utils
import datetime
import pytest
import logging

# 1) Тест нормальной работы функции "date_convert" и вывода логов
def test_date_convert(caplog) -> None:
    """Тест нормальной работы функции date_convert"""
    caplog.set_level(logging.DEBUG, logger="views")
    assert utils.date_convert("2021-12-15 13:00:00") == datetime.datetime(2021, 12, 15, 13, 0)
    assert "Func <date_convert> started" in caplog.text
    assert "Func <date_convert> successfully completed." in caplog.text


# 2) Тест ошибки входного значения функции "date_convert"
def test_date_convert_error(caplog) -> None:
    """Тест ошибки формата входного значения функции date_convert"""
    assert utils.date_convert("2021-12-15 24:00:00") == datetime.datetime(2021, 2, 13, 13, 0)
    assert "time data '2021-12-15 24:00:00' does not match format '%Y-%m-%d %H:%M:%S'." in caplog.text
    assert "The date '2021-02-13 13:00:00' will be used" in caplog.text


# 3) Тест нормальной работы функции "greeting" и вывода логов
def test_greeting(caplog) -> None:
    """Тест нормальной работы функции greeting"""
    caplog.set_level(logging.DEBUG, logger="views")
    x_1 = datetime.datetime(2021, 12, 15, 6, 0)
    x_2 = datetime.datetime(2021, 12, 15, 12, 0)
    x_3 = datetime.datetime(2021, 12, 15, 18, 0)
    x_4 = datetime.datetime(2021, 12, 15, 0, 0)
    assert utils.greeting(x_1) == "Доброе утро"
    assert utils.greeting(x_2) == "Добрый день"
    assert utils.greeting(x_3) == "Добрый вечер"
    assert utils.greeting(x_4) == "Доброй ночи"
    assert "Func <greeting> started" in caplog.text
    assert "Func <greeting> successfully completed." in caplog.text