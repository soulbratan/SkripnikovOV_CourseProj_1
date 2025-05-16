# Модуль тестирования программных функций
from src import utils
import datetime
import pytest
import logging

# 1) Тест нормальной работы функции и вывода логов
def test_date_convert_1(caplog) -> None:
    """Тест нормальной работы функции date_convert"""
    caplog.set_level(logging.DEBUG, logger="views")
    assert utils.date_convert("2021-12-15 13:00:00") == datetime.datetime(2021, 12, 15, 13, 0)
    assert "Func <date_convert> started" in caplog.text
    assert "Func <date_convert> successfully completed." in caplog.text


# 2) Тест ошибки входного значения
def test_date_convert_error(caplog) -> None:
    """Тест ошибки формата входного значения функции date_convert"""
    assert utils.date_convert("2021-12-15 24:00:00") == datetime.datetime(2021, 2, 13, 13, 0)
    assert "time data '2021-12-15 24:00:00' does not match format '%Y-%m-%d %H:%M:%S'." in caplog.text
    assert "The date '2021-02-13 13:00:00' will be used" in caplog.text