# Модуль с основной логикой функции для сервисов веб-страниц (Выгодные категории повышенного кешбэка, Инвесткопилка,
# Простой поиск, Поиск по телефонным номерам, Поиск переводов физическим лицам).
# Собирает вспомогательные функции из utils.py в одну.
from src import utils


def users_search(user_search_string: str) -> str:
    """Функция поиска по транзакциям (Категория, Описание). Принимает строку для поиска, возвращает JSON файл"""
    transactions = utils.read_excel_transactions()
    filt_transactions = utils.simple_search(transactions, user_search_string)
    json_str_answer = filt_transactions.to_json(orient="records", force_ascii=False, indent=4)
    return json_str_answer
