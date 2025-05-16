# Модуль тестирования программных функций
import datetime
import logging
from unittest.mock import patch, Mock
import pandas as pd
import pytest
from _pytest.logging import LogCaptureFixture

from src import utils
import requests

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
    """Тест нормальной работы read_excel_monthly"""
    test_data = {
        "Дата операции": [
            "01.01.2023 00:00:00",
            "15.01.2023 12:30:00",
            "31.01.2023 23:59:59",
            "01.02.2023 00:00:00"
        ],
        "Сумма операции": [100, 200, 300, 400]
    } # Создаем тестовые данные
    test_df = pd.DataFrame(test_data)
    with patch("pandas.read_excel") as mock_read_excel: # Мокируем pd.read_excel, чтобы он возвращал тестовые данные
        mock_read_excel.return_value = test_df
        date_obj = datetime.datetime(2023, 1, 16)
        result = utils.read_excel_monthly("dummy_path.xlsx", date_obj) # Вызываем тестируемую функцию
        mock_read_excel.assert_called_once_with("dummy_path.xlsx", engine="openpyxl") # Проверяем, что pd.read_excel был вызван с правильными аргументами
        assert isinstance(result, pd.DataFrame) # Проверяем, что возвращается DataFrame
        assert len(result) == 2 # Проверяем фильтрацию (должны остаться только 2 записи <= 15.01.2023)
        assert all(result["Дата операции"].dt.month == 1)
        assert all(result["Дата операции"].dt.day <= 15)


def test_read_excel_monthly_missing_date_column(x_1: datetime.datetime, caplog: LogCaptureFixture) -> None:
    """Тест отсутствия нужной колонки read_excel_monthly"""
    test_df = pd.DataFrame({"Неправильная колонка": [1, 2, 3]}) # Создаем DataFrame без колонки "Дата операции"
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = test_df
        result = utils.read_excel_monthly("dummy_path.xlsx", x_1)
        # Проверяем, что возвращается пустой DataFrame с правильными колонками
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert "Дата операции" in result.columns  # Проверяем наличие нужных колонок
        assert "Column 'Дата операции' not found." in caplog.text


def test_read_excel_monthly_file_not_found(x_1: datetime.datetime, caplog: LogCaptureFixture) -> None:
    """Тест отсутствия файла read_excel_monthly"""
    with patch("pandas.read_excel") as mock_read_excel:# Моккируем pd.read_excel, чтобы он вызывал FileNotFoundError
        mock_read_excel.side_effect = FileNotFoundError("Файл не найден")
        result = utils.read_excel_monthly("nonexistent_file.xlsx", x_1)
        # Проверяем, что возвращается пустой DataFrame
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0
        assert "Дата операции" in result.columns
        assert "Returned empty DF" in caplog.text


def test_read_excel_monthly_logging(x_1: datetime.datetime) -> None:
    """Тест логирования read_excel_monthly"""
    test_data = {
        "Дата операции": ["01.01.2023 00:00:00"],
        "Сумма операции": [100]
    }
    test_df = pd.DataFrame(test_data)
    with patch("pandas.read_excel") as mock_read_excel, \
         patch("src.utils.logger") as mock_logger: # Моккируем pd.read_excel и logger
        mock_read_excel.return_value = test_df
        result = utils.read_excel_monthly("dummy_path.xlsx", x_1) # Вызываем функцию с тестовыми данными
        mock_logger.info.assert_any_call("Func <read_excel_monthly> started.") # Проверяем логирование
        mock_logger.info.assert_any_call("Func <read_excel_monthly> successfully completed. Returned OK DF")


def test_cards_statistic_basic(data_frame: pd.DataFrame, cards_stats_expected: list[dict]) -> None:
    """Тест нормальной работы cards_statistic"""
    with patch("src.utils.logger") as mock_logger:
        result = utils.cards_statistic(data_frame) # Вызываем функцию с тестовыми данными
        assert result == cards_stats_expected # Проверяем корректность результата
        mock_logger.info.assert_any_call("Func <cards_statistic> started.") # Проверяем логирование
        mock_logger.info.assert_any_call("Func <cards_statistic> completed.")

def test_cards_statistic_empty_df() -> None:
    """Тест с пустым DataFrame"""
    empty_df = pd.DataFrame(columns=["Номер карты", "Сумма операции"])
    result = utils.cards_statistic(empty_df)
    assert result == [{}]


def test_top5_transactions_basic(data_frame_2: pd.DataFrame, top5_expected: list[dict]) -> None:
    """Тест нормальной работы top5_transactions"""
    with patch("src.utils.logger") as mock_logger: # патчим логгер
        result = utils.top5_transactions(data_frame_2) # Вызываем функцию с тестовыми данными
        assert top5_expected == result # Проверяем результат и ожидаемое значение
        assert len(result) == 5 # Проверяем что вернулось 5 элементов
        amounts = [t["amount"] for t in result]
        assert amounts == sorted(amounts, reverse=True) # Проверяем что транзакции отсортированы по убыванию суммы
        mock_logger.info.assert_any_call("Func <top5_transactions> started.") # Проверяем логирование
        mock_logger.info.assert_any_call("Func <top5_transactions> completed.")

def test_top5_transactions_empty_df() -> None:
    """Тест с пустым DataFrame"""
    empty_df = pd.DataFrame(columns=["Статус", "Сумма операции", "Дата операции",
                                         "Категория", "Описание"])
    result = utils.top5_transactions(empty_df)
    assert result == []


def test_top5_transactions_less_than_5(data_frame_2: pd.DataFrame) -> None:
    """Тест когда успешных транзакций меньше 5"""
    small_data = data_frame_2.iloc[:3]  # только 3 транзакции (2 успешные)
    result = utils.top5_transactions(small_data)
    assert len(result) == 2

@patch('os.getenv')
def test_exchange_rates_success(mock_getenv) -> None:
    """Тест на успешного запроса и обработки ответа"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_getenv.return_value = "mock_api_key"
    mock_response.json.return_value = {
        "rates": {
            "USD": 0.014,
            "EUR": 0.012
        }
    }
    with patch('requests.request', return_value=mock_response) as mock_request:
        result = utils.exchange_rates("USD, EUR")
        # Проверяем, что функция возвращает правильные данные
        assert len(result) == 2
        assert {"currency": "USD", "rate": round(1 / 0.014, 2)} in result
        assert {"currency": "EUR", "rate": round(1 / 0.012, 2)} in result
        # Проверяем, что запрос был сделан с правильными параметрами
        mock_request.assert_called_once_with("GET",
                                             "https://api.apilayer.com/exchangerates_data/latest",
                                             headers={"apikey": "mock_api_key"},
                                             params={"base": "RUB", "symbols": "USD, EUR"},
                                             data={}
                                             )


def test_exchange_rates_api_failure() -> None:
    """Тест на обработку ошибки API"""
    with patch('requests.request', side_effect=requests.exceptions.RequestException("API error")):
        result = utils.exchange_rates("USD")
        # Проверяем, что функция возвращает данные об ошибке
        assert result == [{"currency": "Нет данных", "rate": "Нет данных"}]


@patch("os.getenv")
@patch("src.utils.logger")
def test_exchange_rates_logging(mock_logger, mock_getenv):
    # Тест на проверку логирования
    mock_getenv.return_value = "mock_api_key"
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"USD": 0.014}}
    with patch('requests.request', return_value=mock_response):
        utils.exchange_rates("USD")
        # Проверяем, что логирование работает
        mock_logger.info.assert_any_call("Func <exchange_rates> started.")
        mock_logger.info.assert_any_call("Func <exchange_rates> completed.")