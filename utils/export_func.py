from typing import Dict

from aiogram.types import FSInputFile

from wb_aio_parser_bot.database.crud import all_get_table_info
from wb_aio_parser_bot.utils import create_csv_file_async


def export_db(db_path: str = './database/Data_Base_WB.db') -> FSInputFile:
    return FSInputFile(db_path)

# Таблицы Пользователей
Users_table = 'Users_table'
Search_table = 'Search_table'
Logs_table = 'Logs_table'

def export_users_table_csv() -> Dict[str: FSInputFile, str: str]:
    '''

    :return: {'fsi_input_file': FSInputFile(result), 'file_name': file_name}
    '''
    items = all_get_table_info(Users_table, [
        'user_id',
        'telegram_id',
        'telegram_name',
        'data_connect',
        'search_count'
    ])
    file_name = f'./FileFunction/{Users_table}.csv'
    result = create_csv_file_async(items, filename=file_name)
    dct = {'fsi_input_file': FSInputFile(result), 'file_name': file_name}
    return dct

def export_search_table_csv() -> Dict[str: FSInputFile, str: str]:
    '''

    :return: {'fsi_input_file': FSInputFile(result), 'file_name': file_name}
    '''
    items = all_get_table_info(Search_table, [
        'id_order',
        'telegram_id',
        'search',
        'type_search',
        'data_search',
    ])
    file_name = f'./FileFunction/{Search_table}.csv'
    result = create_csv_file_async(items, filename=file_name)
    dct = {'fsi_input_file': FSInputFile(result), 'file_name': file_name}
    return dct


def export_logs_table_table_csv() -> Dict[str: FSInputFile, str: str]:
    '''

    :return: {'fsi_input_file': FSInputFile(result), 'file_name': file_name}
    '''
    items = all_get_table_info(Logs_table, [
        'id_log',
        'telegram_id',
        'log_error',
        'data_log',
    ])
    file_name = f'./FileFunction/{Logs_table}.csv'
    result = create_csv_file_async(items, filename=file_name)
    dct = {'fsi_input_file': FSInputFile(result), 'file_name': file_name}
    return dct

