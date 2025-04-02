import sqlite3

# Таблицы Пользователей
Users_table = 'Users_table'
Search_table = 'Search_table'
user_limits = 'user_limits '



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
            data_connect Дата Регистрации Пользователя
        '''
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {Users_table}(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id UNIQUE,
            telegram_name TEXT,
            data_connect TEXT,
            search_count INTEGER
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
            id_order INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            search TEXT,
            type_search TEXT,
            data_search TEXT,

            FOREIGN KEY (telegram_id) REFERENCES {Users_table}(telegram_id)
        )
        ''')


        conn.commit()