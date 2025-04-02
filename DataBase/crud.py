import sqlite3
from datetime import datetime
from typing import Dict

# Таблицы Пользователей
Users_table = 'Users_table'
Search_table = 'Search_table'
user_limits = 'user_limits '



BASE_NAME = './DataBase/Data_Base_WB.db'

# Функция для регистрации пользователей
async def register_user_in_table(telegram_id: int, telegram_name: str | None) -> bool:
    '''
    Функция регистрирует пользователя
    :param telegram_id: Айди телеграмма
    :param telegram_name: Имя Телеграмма
    :return: bool
    '''
    with sqlite3.connect(BASE_NAME) as conn:
        # Получаем текущую дату и время
        current_date = datetime.now()
        # Форматируем текущую дату в строку
        data_connect = current_date.strftime("%d.%m.%Y")
        cur = conn.cursor()
        items = cur.execute(f"SELECT telegram_id FROM {Users_table} WHERE telegram_id == ?", (telegram_id, )).fetchall()

        if len(items) != 0:
            return True
        else:
            cur.execute(f'''
            INSERT INTO {Users_table}(telegram_id, telegram_name,  data_connect, search_count) 
            VALUES (?, ?, ?, ?)
            ''', (telegram_id, f'{telegram_name}',  data_connect, 0))
            conn.commit()
            return False

# # Функция для обновление значения поиска на +1
# async def update_search_count(telegram_id: int):

# Проверка существования пользователя Users_table
async def checking_user_in_table(telegram_id: int) -> bool:
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()
        items = cur.execute(f"SELECT telegram_id FROM {Users_table} WHERE telegram_id == ?", (telegram_id,)).fetchone()
        return True if len(items) != 0 else False


# Функция для получения данных с Users_table
async def get_user_table(get: int = 1) -> Dict:
    '''
            Функция для получения данных например
            {1033560490: {'data_connect': '07.03.2025','telegram_name': 'kokokp95'}}
            :param get Параметр для получения нужных данных 1 выдача данных в виде словаря, 2 выдача словарём со списками пример
            \n 1
            :return dict
            '''
    list_data = {
        'tg_id': [], # Айди Телеграмма
        'tg_name': [], # Название в Телеграмме
        'data_con': [], # Дата регистрации
        'search_count': [], # Количество сделанных поиска
    }
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()
        items = cur.execute(f"SELECT telegram_id, telegram_name, data_connect, search_count FROM {Users_table}").fetchall()
        match get:
            case 1:
                # Заключение данных в Словарь
                dict_data = {
                    i[0]: {
                        'telegram_name': i[1],
                        'data_connect': i[2],
                        'search_count': i[3]
                    } for i in items}
                return dict_data
            case 2:
                # Заключение данных в словарь со списками
                for i in items:
                    list_data['telegram_id'].append(i[0])
                    list_data['telegram_name'].append(i[1])
                    list_data['data_connect'].append(i[2])
                    list_data['search_count'].append(i[3])
                return list_data
            case _:
                return {'None': 'None'}


# Функция для получения данных одного пользователя с Users_table
async def get_one_user_table(telegram_id: int) -> dict:
    '''
            Функция для получения данных одного пользователя например
            {1033560490: {'data_connect': '07.03.2025',
                  'telegram_name': 'kokokp95'}}
            :return dict
            '''
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()
        items = cur.execute(f"SELECT telegram_id, telegram_name, data_connect"
                            f"FROM {Users_table} "
                            f"WHERE telegram_id == ?", (telegram_id,)).fetchall()
        # Заключение данных в Словарь
        result_data = {
            i[0]: {
                'telegram_name': i[1],
                'data_connect': i[2],
            } for i in items}
        return result_data


# Функция для сохранения данных о запросе пользователя
async def search_reg_table(telegram_id: int, search: str, type_search: str) -> None:
    '''
    Функция для регистрация ордера поиска
    :param type_search: Вид поиска
    :param telegram_id: Телеграм Айди
    :param search: Поиск
    :return: None
    '''
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()

        # Получаем текущую дату и время
        current_date = datetime.now()
        # Форматируем текущую дату в строку
        data_connect = current_date.strftime("%d.%m.%Y")

        cur.execute(f'''
                    INSERT INTO {Search_table}(telegram_id, search, type_search, data_search) 
                    VALUES (?, ?, ?, ?)
                    ''', (telegram_id, f'{search}', type_search, data_connect))
        cur.execute(f'''
                    UPDATE {Users_table}
                    SET search_count = search_count + 1
                    WHERE telegram_id == ?
                    ''', (telegram_id, ))
        conn.commit()

