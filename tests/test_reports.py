from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
from _pytest.logging import LogCaptureFixture

from src.reports import spending_by_category
from src.utils import report_to_file


def test_spending_by_category(sample_transactions_2: pd.DataFrame) -> None:
    """Тестируем основную функциональность"""
    result = spending_by_category((sample_transactions_2), "Еда")
    assert isinstance(result, str)  # Проверяем, что возвращается JSON строка
    assert "Еда" in result
    assert "Транспорт" not in result


def test_spending_by_category_with_date(sample_transactions_2: pd.DataFrame) -> None:
    """Тестируем основную функциональность"""
    result = spending_by_category((sample_transactions_2), "Еда", "2025-03-01")
    assert "01.01.2024" not in result  # Проверяем, что старые данные не включены


def test_report_to_file_decorator(tmp_path: Any) -> None:
    """Тестируем основную функциональность декоратора"""
    test_data = pd.DataFrame({"A": [1, 2], "B": [3, 4]})  # Создаем тестовые данные
    # Мокаем Path, чтобы контролировать возвращаемые пути
    mock_path = MagicMock(spec=Path)
    mock_path.parent.parent = tmp_path
    mock_path.__truediv__.side_effect = lambda x: tmp_path / x
    # Мокаем остальные зависимости
    with patch("pathlib.Path", return_value=mock_path), patch("builtins.open", mock_open()) as mock_file:

        @report_to_file(filename="test_report.txt")  # Создаем тестируемую функцию с декоратором
        def mock_func() -> Any:
            return test_data

        result = mock_func()  # Вызываем функцию
        assert result.equals(test_data)  # Проверяем, что функция вернула корректный результат
        # Проверяем запись в файл
        assert mock_file.call_count == 1
        call_args = mock_file.call_args[0]
        assert str("test_report.txt") in str(call_args[0])
        assert call_args[1] == "w"


def test_report_to_file_error_handling(caplog: LogCaptureFixture) -> None:
    """Тестируем обработку ошибок при записи в файл"""

    @report_to_file(filename="test_error.txt")
    def error_func() -> Any:
        return "test data"

    # Имитируем ошибку при записи в файл
    with patch("builtins.open", side_effect=Exception("Test error")):
        result = error_func()
        # Проверяем, что функция вернула данные несмотря на ошибку
        assert result == "test data"
        # Проверяем, что ошибка была залогирована
        assert "Error saving report" in caplog.text
