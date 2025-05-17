import json
from typing import Any
from unittest.mock import patch

import pandas as pd

from src.services import users_search


def test_users_search_success(sample_transactions: pd.DataFrame) -> None:
    """Тест успешной работы программы users_search"""
    with (
        patch("src.utils.read_excel_transactions", return_value=sample_transactions),
        patch("src.utils.simple_search", return_value=sample_transactions.iloc[0:1]),
    ):
        result = users_search("Продукты")
        json_data: Any = json.loads(result)  # Проверяем что результат валидный JSON
        assert isinstance(json_data, list)
        assert len(json_data) == 1
        assert json_data[0]["Категория"] == "Продукты"


def test_users_search_empty_result(sample_transactions: pd.DataFrame) -> None:
    """Тест пустого ответа поиска функции users_search"""
    with (
        patch("src.utils.read_excel_transactions", return_value=sample_transactions),
        patch("src.utils.simple_search", return_value=pd.DataFrame()),
    ):
        result = users_search("Несуществующий запрос")
        json_data = json.loads(result)
        assert isinstance(json_data, list)
        assert len(json_data) == 0


def test_users_search_json_format(sample_transactions: pd.DataFrame) -> None:
    """Тест JSON формата на выходе функции users_search"""
    with (
        patch("src.utils.read_excel_transactions", return_value=sample_transactions),
        patch("src.utils.simple_search", return_value=sample_transactions.iloc[0:1]),
    ):
        result = users_search("Продукты")
        json_data = json.loads(result)  # Проверяем что результат можно корректно разобрать
        assert json.dumps(json_data)  # Проверка сериализации обратно


def test_users_search_empty_dataframe() -> None:
    """Тест пустого DF на входе функции users_search"""
    empty_df = pd.DataFrame(columns=["Категория", "Описание", "Сумма"])
    with (
        patch("src.utils.read_excel_transactions", return_value=empty_df),
        patch("src.utils.simple_search", return_value=empty_df),
    ):
        result = users_search("запрос")
        json_data: Any = json.loads(result)
        assert isinstance(json_data, list)
        assert len(json_data) == 0
