from src.views import main_page
from src.services import users_search
from src.reports import spending_by_category
from src.utils import read_excel_transactions


if __name__ == "__main__": # pragma: no cover
    web_page = main_page("2021-12-15 15:00:00")
    print(web_page)

    search_result = users_search("ЛюдиЛюбят")
    print(search_result)

    df = read_excel_transactions()
    reports = spending_by_category(df, "Перевод", "2020-02-12 13:00:00")
    print(reports)


