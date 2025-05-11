import logging
import sqlite3
from datetime import datetime
from typing import Dict, List
from database.models import USERS_TABLE, SEARCH_TABLE, LOGS_TABLE, BASE_NAME


# Функция для регистрации пользователей
def register_user_in_table(telegram_id: int, telegram_name: str | None) -> bool:
    '''
    Функция регистрирует пользователя
    :param telegram_id: Айди телеграмма
    :param telegram_name: Имя Телеграмма
    :return: bool
    '''
    with sqlite3.connect(BASE_NAME) as conn:
        try:
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
        except Exception as ex:
            raise Exception(f'Ошибка при регистрации пользователя: {ex}')


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


def search_reg_table(telegram_id: int, search: str, type_search: str) -> None:
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
            raise Exception(e)


def save_error_to_db(telegram_id: int | None, error_text: str):
    '''
    Запись Лог Ошибки в БД
    :param telegram_id: ID пользователя в Telegram
    :param error_text: Текст ошибки лога
    :return: None
    '''
    with sqlite3.connect(BASE_NAME) as conn:
        try:
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
        except Exception as ex:
            raise Exception(f'Ошибка при записи лог ошибки в БД: {ex}')