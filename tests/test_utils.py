# Модуль тестирования программных функций
import datetime
import logging
from unittest.mock import patch, MagicMock
import pandas as pd
import pytest
from _pytest.logging import LogCaptureFixture

from src import utils


# 1) Тест нормальной работы функции "date_convert" и вывода логов
@pytest.mark.parametrize(
    "date_str, expected",
    [
        ("2021-12-15 13:00:00", datetime.datetime(2021, 12, 15, 13, 0)),
        ("2000-01-01 00:00:00", datetime.datetime(2000, 1, 1, 0, 0)),
        ("2020-10-10 10:00:00", datetime.datetime(2020, 10, 10, 10, 0)),
    ],
)
def test_date_convert(date_str: str, expected: datetime.datetime, caplog: LogCaptureFixture) -> None:
    """Тест нормальной работы функции date_convert"""
    caplog.set_level(logging.DEBUG, logger="views")
    assert utils.date_convert(date_str) == expected
    assert "Func <date_convert> started" in caplog.text
    assert "Func <date_convert> successfully completed." in caplog.text


# 2) Тест ошибки входного значения функции "date_convert"
def test_date_convert_error(caplog: LogCaptureFixture) -> None:
    """Тест ошибки формата входного значения функции date_convert"""
    assert utils.date_convert("2021-12-15 24:00:00") == datetime.datetime(2021, 2, 13, 13, 0)
    assert "time data '2021-12-15 24:00:00' does not match format '%Y-%m-%d %H:%M:%S'." in caplog.text
    assert "The date '2021-02-13 13:00:00' will be used" in caplog.text


def test_greeting(
    caplog: LogCaptureFixture,
    x_1: datetime.datetime,
    x_2: datetime.datetime,
    x_3: datetime.datetime,
    x_4: datetime.datetime,
) -> None:
    """Тест нормальной работы функции greeting"""
    caplog.set_level(logging.DEBUG, logger="views")
    assert utils.greeting(x_1) == "Доброе утро"
    assert utils.greeting(x_2) == "Добрый день"
    assert utils.greeting(x_3) == "Добрый вечер"
    assert utils.greeting(x_4) == "Доброй ночи"
    assert "Func <greeting> started" in caplog.text
    assert "Func <greeting> successfully completed." in caplog.text


def test_read_excel_monthly_success() -> None:
    # Создаем тестовые данные
    test_data = {
        "Дата операции": [
            "01.01.2023 00:00:00",
            "15.01.2023 12:30:00",
            "31.01.2023 23:59:59",
            "01.02.2023 00:00:00"
        ],
        "Сумма операции": [100, 200, 300, 400]
    }
    test_df = pd.DataFrame(test_data)
    # Мокируем pd.read_excel, чтобы он возвращал тестовые данные
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = test_df
        # Вызываем тестируемую функцию
        date_obj = datetime.datetime(2023, 1, 16)
        result = utils.read_excel_monthly("dummy_path.xlsx", date_obj)
        # Проверяем, что pd.read_excel был вызван с правильными аргументами
        mock_read_excel.assert_called_once_with("dummy_path.xlsx", engine="openpyxl")
        # Проверяем, что возвращается DataFrame
        assert isinstance(result, pd.DataFrame)
        # Проверяем фильтрацию (должны остаться только 2 записи <= 15.01.2023)
        assert len(result) == 2
        assert all(result["Дата операции"].dt.month == 1)
        assert all(result["Дата операции"].dt.day <= 15)


def test_read_excel_monthly_missing_date_column(x_1: datetime.datetime, caplog: LogCaptureFixture) -> None:
    # Создаем DataFrame без колонки "Дата операции"
    test_df = pd.DataFrame({"Неправильная колонка": [1, 2, 3]})
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = test_df
        result = utils.read_excel_monthly("dummy_path.xlsx", x_1)
        # Проверяем, что возвращается пустой DataFrame с правильными колонками
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert "Дата операции" in result.columns  # Проверяем наличие нужных колонок
        assert "Column 'Дата операции' not found." in caplog.text


def test_read_excel_monthly_file_not_found(x_1: datetime.datetime, caplog: LogCaptureFixture) -> None:
    # Мокируем pd.read_excel, чтобы он вызывал FileNotFoundError
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.side_effect = FileNotFoundError("Файл не найден")
        result = utils.read_excel_monthly("nonexistent_file.xlsx", x_1)
        # Проверяем, что возвращается пустой DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert "Дата операции" in result.columns
        assert "Returned empty DF" in caplog.text


def test_read_excel_monthly_logging(x_1: datetime.datetime) -> None:
    test_data = {
        "Дата операции": ["01.01.2023 00:00:00"],
        "Сумма операции": [100]
    }
    test_df = pd.DataFrame(test_data)
    with patch("pandas.read_excel") as mock_read_excel, \
         patch("src.utils.logger") as mock_logger: # Мокируем pd.read_excel и logger
        mock_read_excel.return_value = test_df
        result = utils.read_excel_monthly("dummy_path.xlsx", x_1)
        # Проверяем, что logger.info вызывался с нужными сообщениями
        mock_logger.info.assert_any_call("Func <read_excel_monthly> started.")
        mock_logger.info.assert_any_call("Func <read_excel_monthly> successfully completed. Returned OK DF")


def test_cards_statistic_basic(data_frame, cards_stats_expected) -> None:
    with patch("src.utils.logger") as mock_logger:
        # Вызываем функцию с тестовыми данными
        result = utils.cards_statistic(data_frame)
        # Проверяем корректность результата
        assert result == cards_stats_expected
        # Проверяем, что вызывались методы логгера
        mock_logger.info.assert_any_call("Func <cards_statistic> started.")
        mock_logger.info.assert_any_call("Func <cards_statistic> completed.")

def test_cards_statistic_empty_df() -> None:
    # Тест с пустым DataFrame
    empty_df = pd.DataFrame(columns=['Номер карты', 'Сумма операции'])
    result = utils.cards_statistic(empty_df)
    assert result == [{}]