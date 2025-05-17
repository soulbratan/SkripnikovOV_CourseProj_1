# Модуль с основной логикой функции для веб-страниц (страница "Главная", страница "События").
# Собирает вспомогательные функции из utils.py в одну.
import json
from pathlib import Path
from typing import Dict, List, Union

from src import utils

JSONValue = Union[str, int, float, bool, None, List["JSONValue"], Dict[str, "JSONValue"]]


def main_page(user_date: str) -> JSONValue:
    """
    Функция главной страницы. Принимает на вход строку с датой в формате 'YYYY-MM-DD HH:MM:SS'.
    Возвращает JSON-ответ. Функция собирает в себе вспомогательные функции.
    """
    date = utils.date_convert(user_date)
    greet = utils.greeting(date)
    transactions = utils.read_excel_monthly("../data/operations.xlsx", date)
    cards = utils.cards_statistic(transactions)
    top5_tr = utils.top5_transactions(transactions)
    current_dir = Path(__file__).parent
    file_path = current_dir.parent / "user_settings.json"
    absolute_path = file_path.resolve()
    with open(absolute_path) as f:
        users_data = json.load(f)
    user_currencies_symbols = ", ".join(users_data.get("user_currencies"))
    user_stocks_symbols = users_data.get("user_stocks")
    currency_rates = utils.exchange_rates(user_currencies_symbols)
    stocks = utils.stocks_prices(user_stocks_symbols)
    result = {
        "greeting": greet,
        "cards": cards,
        "top_transactions": top5_tr,
        "currency_rates": currency_rates,
        "stock_prices": stocks,
    }
    main_page_answer = json.dumps(result, indent=4, ensure_ascii=False)
    return main_page_answer


res = main_page("2021-12-15 15:00:00")
print(type(res))
print(res)
