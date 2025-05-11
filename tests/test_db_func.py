import pytest

from database.crud import *

from database.models import USERS_TABLE, SEARCH_TABLE, LOGS_TABLE

# Тестирование Регистрации пользователя в БД
@pytest.mark.parametrize(
    'telegram_id, telegram_name, result',
    [
        (123, 'Test', True | False),
        (321, 'Test2', True | False),
    ]
)
def test_register_user_in_table(telegram_id, telegram_name, result):
    assert register_user_in_table(telegram_id, telegram_name) == result, (
        Exception('Ошибка при Тестировании регистрации пользователя'))
    print('Тестирование регистрации пользователей успешно')


# Тестирование для получения данных и базы данных
@pytest.mark.parametrize(
    'table_name, columns, result',
    [
        (USERS_TABLE, ['user_id', 'telegram_id', 'data_connect', 'search_count'], dict),
        (SEARCH_TABLE, ['id_order', 'telegram_id', 'search', 'type_search', 'data_search'], dict),
        (LOGS_TABLE, ['id_log', 'telegram_id', 'log_error', 'data_log'], dict),
    ]
)
def test_all_get_table_info(table_name, columns, result):
    data = all_get_table_info(table_name, columns)

    # Проверка полученных данных
    assert isinstance(data, dict), Exception('Ошибка в тестировании получение данных')

    # Проверка количества полученных данных
    assert len(data) == len(columns), Exception('Получено не верное количество данных')

    print('Тестирование получение данных с таблиц выполнено успешно')

# Тестирование регистрации поискового запроса пользователя и увеличение счетчика поисков
@pytest.mark.parametrize(
    'telegram_id, search, type_search',
    [
        (123, 'Тест1', 'TEST1'),
        (321, 'Тест2', 'TEST2')
    ]
)
def test_search_reg_table(telegram_id, search, type_search):
    assert search_reg_table(telegram_id, search, type_search) is None

# Тестирование регистрация лога ошибки
@pytest.mark.parametrize(
    'telegram_id, error_text',
    [
        (123, 'Тестовая ошибка'),
        (321, 'Тестовая ошибка')
    ]
)
def test_save_error_to_db(telegram_id, error_text):
    assert save_error_to_db(telegram_id, error_text) is None, Exception('Ошибка при записи лог ошибки')
