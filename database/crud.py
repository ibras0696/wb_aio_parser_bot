import logging
import sqlite3
from datetime import datetime
from typing import Dict, List
from database.models import USERS_TABLE, SEARCH_TABLE, LOGS_TABLE, BASE_NAME


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
        items = cur.execute(f"SELECT telegram_id FROM {USERS_TABLE} WHERE telegram_id == ?", (telegram_id, )).fetchall()

        if len(items) != 0:
            return True
        else:
            cur.execute(f'''
            INSERT INTO {USERS_TABLE}(telegram_id, telegram_name,  data_connect, search_count) 
            VALUES (?, ?, ?, ?)
            ''', (telegram_id, f'{telegram_name}',  data_connect, 0))
            conn.commit()
            return False


# Проверка существования пользователя Users_table
async def checking_user_in_table(telegram_id: int) -> bool:
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()
        items = cur.execute(f"SELECT telegram_id FROM {USERS_TABLE} WHERE telegram_id == ?", (telegram_id,)).fetchone()
        return True if len(items) != 0 else False


async def get_user_table(get: int = 1) -> Dict:
    """
    Получает данные из таблицы пользователей в двух форматах:
    1 - Словарь {tg_id: {user_data}}
    2 - Словарь {field_name: [values]}

    :param get: Тип возвращаемых данных (1 или 2)
    :return: Данные пользователей в указанном формате
    """
    # Инициализация структуры для case 2
    list_data = {
        'tg_id': [],  # Telegram ID
        'tg_name': [],  # Имя в Telegram
        'data_con': [],  # Дата регистрации
        'search_count': []  # Количество поисков
    }

    with sqlite3.connect(BASE_NAME) as conn:
        try:
            cur = conn.cursor()
            query = f"""
                SELECT 
                    telegram_id, 
                    telegram_name, 
                    data_connect, 
                    search_count 
                FROM {USERS_TABLE}
            """
            items = cur.execute(query).fetchall()

            match get:
                case 1:
                    return {
                        i[0]: {
                            'telegram_name': i[1],
                            'data_connect': i[2],
                            'search_count': i[3]
                        } for i in items
                    }

                case 2:
                    for tg_id, name, date, searches in items:
                        list_data['tg_id'].append(tg_id)
                        list_data['tg_name'].append(name)
                        list_data['data_con'].append(date)
                        list_data['search_count'].append(searches)
                    return list_data

                case _:
                    return {'None': 'None'}

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {'error': str(e)} if get == 1 else {k: [] for k in list_data}


# Функция для получения данных и базы данных
def all_get_table_info(table_name: str, columns: list) -> dict:
    """
    Получает данные из указанных столбцов таблицы и возвращает словарь,
    где ключи - названия столбцов, а значения - списки данных.

    :param table_name: Название таблицы в базе данных
    :param columns: Список нужных столбцов
    :return: Словарь вида {столбец1: [данные], столбец2: [данные], ...}
    """
    if not columns:
        return {}

    dct_result = {column: [] for column in columns}

    with sqlite3.connect(BASE_NAME) as conn:
        conn.row_factory = sqlite3.Row  # Для доступа к столбцам по имени
        cur = conn.cursor()

        try:
            # Безопасное формирование запроса
            query = f"SELECT {', '.join(columns)} FROM {table_name}"
            cur.execute(query)

            for row in cur.fetchall():
                for column in columns:
                    dct_result[column].append(row[column])

        except sqlite3.Error as e:
            print(f"Ошибка при работе с БД: {e}")
            return {}

    return dct_result


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
                            f"FROM {USERS_TABLE} "
                            f"WHERE telegram_id == ?", (telegram_id,)).fetchall()
        # Заключение данных в Словарь
        result_data = {
            i[0]: {
                'telegram_name': i[1],
                'data_connect': i[2],
            } for i in items}
        return result_data


async def search_reg_table(telegram_id: int, search: str, type_search: str) -> None:
    """
    Регистрирует поисковый запрос пользователя и увеличивает счетчик поисков.

    :param telegram_id: ID пользователя в Telegram
    :param search: Текст поискового запроса
    :param type_search: Тип поиска
    :return: None
    """
    with sqlite3.connect(BASE_NAME) as conn:
        try:
            cur = conn.cursor()
            current_date = datetime.now().strftime("%d.%m.%Y")

            # Вставка данных поиска
            cur.execute(
                f"""INSERT INTO {SEARCH_TABLE}(
                    telegram_id, 
                    search, 
                    type_search, 
                    data_search
                ) VALUES (?, ?, ?, ?)""",
                (telegram_id, search.strip(), type_search.strip(), current_date)
            )

            # Обновление счетчика поисков
            cur.execute(
                f"""UPDATE {USERS_TABLE}
                SET search_count = search_count + 1
                WHERE telegram_id = ?""",
                (telegram_id,)
            )

            conn.commit()

        except sqlite3.Error as e:
            conn.rollback()
            logging.error(f"Database error in search_reg_table: {e}")
            raise


def save_error_to_db(telegram_id: int | None, error_text: str):
    with sqlite3.connect(BASE_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(f'''
            INSERT INTO {LOGS_TABLE} (telegram_id, log_error, data_log)
            VALUES (?, ?, ?)
        ''', (
            telegram_id,
            error_text,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))

        conn.commit()