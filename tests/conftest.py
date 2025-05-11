import pytest



# Получение базового URL по API
@pytest.fixture()
def get_url_api_wb():
    return 'https://search.wb.ru/exactmatch/ru/common/v9/search'