import sqlite3

# Таблицы Пользователей
USERS_TABLE = 'Users_table'
SEARCH_TABLE = 'Search_table'
LOGS_TABLE = 'Logs_table'



BASE_NAME = './database/Data_Base_WB.db'

# Функция для создания Таблиц для Баз Данных
async def create_table():
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()

        # _____________________________________________________________
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {USERS_TABLE}(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id UNIQUE,
            telegram_name TEXT,
            data_connect TEXT,
            search_count INTEGER
        )
        ''')

        # _____________________________________________________________
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {SEARCH_TABLE}(
            id_order INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            search TEXT,
            type_search TEXT,
            data_search TEXT,

            FOREIGN KEY (telegram_id) REFERENCES {USERS_TABLE}(telegram_id)
        )
        ''')

        # _____________________________________________________________
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {LOGS_TABLE}(
        id_log INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        log_error TEXT,
        data_log TEXT,
        
        FOREIGN KEY (telegram_id) REFERENCES {USERS_TABLE}(telegram_id)
        )
        ''')

        conn.commit()