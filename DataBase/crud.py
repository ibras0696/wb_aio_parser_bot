import asyncio
import sqlite3
from datetime import datetime


# Таблицы Пользователей
Users_table = 'Users_table'
Search_table = 'Search_table'
Order_table = 'Order_table'


BASE_NAME = './DataBase/Data_Base_WB.db'

# Функция для создания Таблиц для Баз Данных
async def create_table():
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()

        # _____________________________________________________________
        f'''
        Таблица {Users_table} для пользователей
            user_id Айди пользователя в общем количестве
            telegram_id Айди Телеграм 
            telegram_name Имя Пользователя
            free_search Количество бесплатных дней
            data_connect Дата Регистрации Пользователя
        '''
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {Users_table}(
            user_id INTEGER AUTO_INCREMENT,
            telegram_id INTEGER PRIMARY KEY,
            telegram_name TEXT,
            free_search INTEGER,
            data_connect TEXT
        )
        ''')

        # _____________________________________________________________
        f'''
        Таблица {Search_table}
            id_order Айди операции
            telegram_id Айди Телеграм 
            search Название товара который искал пользователь
            data_search Дата запроса поиска товара
            FOREIGN KEY (telegram_id) REFERENCES {Users_table}(telegram_id) Связка Айди телеграмма 
        '''
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {Search_table}(
            id_order INTEGER AUTO_INCREMENT,
            telegram_id INTEGER PRIMARY KEY,
            search TEXT,
            data_search TEXT,
            
            FOREIGN KEY (telegram_id) REFERENCES {Users_table}(telegram_id)
        )
        ''')



        conn.commit()

# Функции для работы с таблицей Users_table
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
            INSERT INTO {Users_table}(telegram_id, telegram_name,  data_connect) 
            VALUES (?, ?, ? )
            ''', (telegram_id, f'{telegram_name} ',  data_connect))
            conn.commit()
            return False


# Проверка существования пользователя Users_table
async def checking_user_in_table(telegram_id: int) -> bool:
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()
        items = cur.execute(f"SELECT telegram_id FROM {Users_table} WHERE telegram_id == ?", (telegram_id,)).fetchall()
        return True if len(items) != 0 else False


# Функция для получения данных с Users_table
async def get_user_table():
    '''
            Функция для получения данных например
            {1033560490: {'data_connect': '07.03.2025',
                  'free_search': 10,
                  'status': 'User',
                  'telegram_name': 'kokokp95'}}
            :return dict
            '''
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()
        items = cur.execute(f"SELECT telegram_id, telegram_name, free_search, data_connect, status FROM {Users_table}").fetchall()
        # Заключение данных в Словарь
        result_data = {
            i[0]: {
                'telegram_name': i[1],
                'free_search': i[2],
                'data_connect': i[3],
                'status': i[4]
            } for i in items}
        return result_data

# Функция для получения данных одного пользователя с Users_table
async def get_one_user_table(telegram_id: int) -> dict:
    '''
            Функция для получения данных одного пользователя например
            {1033560490: {'data_connect': '07.03.2025',
                  'free_search': 10,
                  'status': 'User',
                  'telegram_name': 'kokokp95'}}
            :return dict
            '''
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()
        items = cur.execute(f"SELECT telegram_id, telegram_name, free_search, data_connect, status "
                            f"FROM {Users_table} "
                            f"WHERE telegram_id == ?", (telegram_id,)).fetchall()
        # Заключение данных в Словарь
        result_data = {
            i[0]: {
                'telegram_name': i[1],
                'free_search': i[2],
                'data_connect': i[3],
                'status': i[4]
            } for i in items}
        return result_data





# asyncio.run(create_table())



