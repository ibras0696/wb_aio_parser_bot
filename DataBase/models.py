import sqlite3

# Таблицы Пользователей
Users_table = 'Users_table'
Search_table = 'Search_table'
Logs_table = 'Logs_table'



BASE_NAME = './DataBase/Data_Base_WB.db'

# Функция для создания Таблиц для Баз Данных
async def create_table():
    with sqlite3.connect(BASE_NAME) as conn:
        cur = conn.cursor()

        # _____________________________________________________________
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

        # _____________________________________________________________
        cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {Logs_table}(
        id_log INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        log_error TEXT,
        data_log TEXT,
        
        FOREIGN KEY (telegram_id) REFERENCES {Users_table}(telegram_id)
        )
        ''')

        conn.commit()