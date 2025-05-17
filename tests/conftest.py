import datetime

import pandas as pd
import pytest
from pytest import MonkeyPatch


@pytest.fixture
def x_1() -> datetime.datetime:
    x_1 = datetime.datetime(2021, 12, 15, 6, 0)
    return x_1


@pytest.fixture
def x_2() -> datetime.datetime:
    x_2 = datetime.datetime(2021, 12, 15, 12, 0)
    return x_2


@pytest.fixture
def x_3() -> datetime.datetime:
    x_3 = datetime.datetime(2021, 12, 15, 18, 0)
    return x_3


@pytest.fixture
def x_4() -> datetime.datetime:
    x_4 = datetime.datetime(2021, 12, 15, 0, 0)
    return x_4


@pytest.fixture
def data_frame() -> pd.DataFrame:
    test_data = pd.DataFrame(
        {
            "Номер карты": ["1234", "1234", "5678", "5678"],
            "Сумма операции": [-1000, -2000, -500, -1500],
            "Другие колонки": [1, 2, 3, 4],
        }
    )
    return test_data


@pytest.fixture
def cards_stats_expected() -> list[dict]:
    expected_result = [
        {"last_digits": "1234", "total_spent": 3000.0, "cashback": 30.0},
        {"last_digits": "5678", "total_spent": 2000.0, "cashback": 20.0},
    ]
    return expected_result


@pytest.fixture
def data_frame_2() -> pd.DataFrame:
    test_data = pd.DataFrame(
        {
            "Статус": ["OK", "FAIL", "OK", "OK", "OK", "OK", "FAIL"],
            "Сумма операции": [1000, 2000, 3000, 4000, 5000, 6000, 7000],
            "Сумма операции с округлением": [1000, 2000, 3000, 4000, 5000, 6000, 7000],
            "Дата операции": [
                datetime.datetime(2023, 1, 1),
                datetime.datetime(2023, 1, 2),
                datetime.datetime(2023, 1, 3),
                datetime.datetime(2023, 1, 4),
                datetime.datetime(2023, 1, 5),
                datetime.datetime(2023, 1, 6),
                datetime.datetime(2023, 1, 7),
            ],
            "Категория": ["A", "B", "C", "D", "E", "F", "G"],
            "Описание": ["Desc1", "Desc2", "Desc3", "Desc4", "Desc5", "Desc6", "Desc7"],
        }
    )
    return test_data


@pytest.fixture
def top5_expected() -> list[dict]:
    expected_result = [
        {"date": "06.01.2023", "amount": 6000, "category": "F", "description": "Desc6"},
        {"date": "05.01.2023", "amount": 5000, "category": "E", "description": "Desc5"},
        {"date": "04.01.2023", "amount": 4000, "category": "D", "description": "Desc4"},
        {"date": "03.01.2023", "amount": 3000, "category": "C", "description": "Desc3"},
        {"date": "01.01.2023", "amount": 1000, "category": "A", "description": "Desc1"},
    ]
    return expected_result


@pytest.fixture
def mock_env(monkeypatch: MonkeyPatch) -> None:
    """Фикстура для мокирования переменных окружения"""
    monkeypatch.setenv("API_KEY_stocks", "test_api_key")


@pytest.fixture
def sample_transactions() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Категория": ["Продукты", "Кафе", "Транспорт", "Аптека", None],
            "Описание": ["Супермаркет", "Ресторан", "Метро", "Аптека 24", "Онлайн платеж"],
            "Сумма": [1000, 500, 150, 300, 200],
        }
    )
