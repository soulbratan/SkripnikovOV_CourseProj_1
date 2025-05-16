import datetime

import pytest


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
