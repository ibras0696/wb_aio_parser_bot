from typing import Dict

from aiogram.types import FSInputFile

from utils import export_users_table_csv

def test_export_users_table_csv():
    assert export_users_table_csv() == True