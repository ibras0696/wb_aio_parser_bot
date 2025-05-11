import os

import pytest

from utils import export_users_table_csv, create_csv_file


# Тестирование экспорта таблицы Пользователей с БД и его удаления
def test_export_users_table_csv():
    result = export_users_table_csv()
    file = result.get('file_name')
    fsi_input_file = result.get('fsi_input_file')

    # Проверяем что экспорт прошел успешно
    assert fsi_input_file is not None, Exception('Ошибка: экспорта таблицы Пользователей с БД')

    # Проверка существования файла и его удаления
    assert os.path.exists(file), Exception('Ошибка: Файл не создан')

    #  Удаляем в случае успешности создание файла
    os.remove(file)

    assert os.path.exists(file) is False, Exception('Объект не удалился при экспорте таблицы Пользователей с БД')

    print('Тестирование Экспорта и авто удаления Таблицы Пользователей файла успешно')


# Тестирование экспорта таблицы Поиска с БД и его удаления
def test_export_search_table_csv():
    result = export_users_table_csv()
    file = result.get('file_name')
    fsi_input_file = result.get('fsi_input_file')

    # Проверяем что экспорт прошел успешно
    assert fsi_input_file is not None, Exception('Ошибка: экспорта таблицы Поиска с БД')

    # Проверка существования файла и его удаления
    assert os.path.exists(file), Exception('Ошибка: Файл не создан')

    #  Удаляем в случае успешности создание файла
    os.remove(file)

    assert os.path.exists(file) is False, Exception('Объект не удалился при экспорте таблицы Поиска с БД')

    print('Тестирование Экспорта и авто удаления Таблицы Поиска файла успешно')

# Тестирование экспорта таблицы Логов с БД и его удаления
def test_export_logs_table_table_csv():
    result = export_users_table_csv()
    file = result.get('file_name')
    fsi_input_file = result.get('fsi_input_file')

    # Проверяем что экспорт прошел успешно
    assert fsi_input_file is not None, Exception('Ошибка: экспорта таблицы Логов с БД')

    # Проверка существования файла и его удаления
    assert os.path.exists(file), Exception('Ошибка: Файл не создан')

    #  Удаляем в случае успешности создание файла
    os.remove(file)

    assert os.path.exists(file) is False, Exception('Объект не удалился при экспорте таблицы Логов с БД')

    print('Тестирование Экспорта и авто удаления файла Таблицы Логов успешно')


# Тестирование создание и удаление CSV файла
@pytest.mark.parametrize(
    'data, filename, result',
    [
        ({
            'name': ['Боб', 'Кеннеди', 'Трамп'],
            'age': [20, 'Неизвестно', 57]
         }, 'test', 'test.csv'),

        ({
            'name': ['Боб', 'Кеннеди', 'Трамп'],
            'age': [20, 'Неизвестно', 57]
         }, 'test.csv', 'test.csv'),

        ({
            'name': ['Боб', 'Кеннеди', 'Трамп'],
            'age': [20, 'Неизвестно', 57]
         }, 'no_test', 'no_test.csv')
    ]
)
def test_create_csv_file_async(data, filename, result):

    # Проверка работы csv создателя
    assert create_csv_file(data, filename) == result, Exception('Ошибка при создании CSV файла')

    # Проверка существования файла и его удаления
    assert os.path.exists(result), Exception('Ошибка: Файл не создан')

    #  Удаляем в случае успешности создание файла
    os.remove(result)

    # Проверка существования после удаления
    assert os.path.exists(result) is False, Exception('Объект не удалился при экспорте таблицы Логов с БД')

    print('Тестирование CSV функция создания успешно')
