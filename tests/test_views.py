import json
from datetime import datetime
from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest

from src.views import main_page

# Тестовые данные
test_date = "2021-12-15 15:00:00"
test_user_settings = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}

# Моки для возвращаемых значений
mock_converted_date = datetime(2021, 12, 15, 15, 0, 0)
mock_greeting = "Добрый день"
mock_transactions = [
    {"amount": 100, "card": "1234", "date": "2021-12-15"},
    {"amount": 200, "card": "5678", "date": "2021-12-16"},
]
mock_cards_stats = {"total": 300, "count": 2}
mock_top5 = [{"amount": 200}, {"amount": 100}]
mock_currency_rates = {"USD": 75.5, "EUR": 85.3}
mock_stock_prices = {"AAPL": 150.2, "GOOGL": 2750.5}


@pytest.fixture
def mock_utils() -> Generator:
    # Создаем мок для utils.date отдельно
    mock_date = MagicMock()
    mock_date.convert.return_value = mock_converted_date
    with patch.multiple(
        "src.utils",
        date_convert=mock_date,  # Подменяем utils.date
        greeting=MagicMock(return_value=mock_greeting),
        read_excel_monthly=MagicMock(return_value=mock_transactions),
        cards_statistic=MagicMock(return_value=mock_cards_stats),
        top5_transactions=MagicMock(return_value=mock_top5),
        exchange_rates=MagicMock(return_value=mock_currency_rates),
        stocks_prices=MagicMock(return_value=mock_stock_prices),
    ) as mocks:
        yield mocks


@pytest.fixture
def mock_json_load() -> Generator:
    with patch("json.load", return_value=test_user_settings) as mock:
        yield mock


def test_main_page_success(mock_utils: MagicMock, mock_json_load: MagicMock) -> None:
    """Тест успешной работы функции"""
    result: Any = main_page(test_date)  # Вызываем тестируемую функцию
    result_data: Any = json.loads(result)  # Проверяем, что результат является валидным JSON
    # Проверяем структуру ответа
    assert isinstance(result_data, dict)
    assert set(result_data.keys()) == {"greeting", "cards", "top_transactions", "currency_rates", "stock_prices"}
    # Проверяем значения
    assert result_data["greeting"] == mock_greeting
    assert result_data["cards"] == mock_cards_stats
    assert result_data["top_transactions"] == mock_top5
    assert result_data["currency_rates"] == mock_currency_rates
    assert result_data["stock_prices"] == mock_stock_prices
