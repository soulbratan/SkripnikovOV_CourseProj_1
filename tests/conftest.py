import datetime

import pytest
import pandas as pd

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
    test_data = pd.DataFrame({
        'Номер карты': ['1234', '1234', '5678', '5678'],
        'Сумма операции': [-1000, -2000, -500, -1500],
        'Другие колонки': [1, 2, 3, 4]
    })
    return test_data

@pytest.fixture
def cards_stats_expected() -> list[dict]:
    expected_result = [
        {
            'last_digits': '1234',
            'total_spent': 3000.0,
            'cashback': 30.0
        },
        {
            'last_digits': '5678',
            'total_spent': 2000.0,
            'cashback': 20.0
        }
    ]
    return expected_result