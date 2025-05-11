import os

import pandas as pd
from typing import Dict, List, Any



def create_csv_file(data: Dict[str, List[Any]], filename: str) -> str:
    """
    Асинхронно создает CSV-файл на диске из словаря данных и возвращает путь к нему.

    :param data: Словарь, где ключи — это названия столбцов, а значения — списки данных.
                 Например: {'Name': ['Alice', 'Bob'], 'Age': [30, 25]}.
    :param filename: Имя файла для сохранения. Например: 'output.csv'.
    :return: Абсолютный путь к созданному файлу.
    """
    # Преобразуем словарь в DataFrame
    df = pd.DataFrame(data)
    filename = filename if filename.endswith('.csv') else filename+'.csv'

    # Сохранение в CSV
    df.to_csv(
        path_or_buf=filename,
        index=False,
        sep=';',  # Разделитель
        encoding='utf-8-sig',  # Кодировка
        decimal=','  # Использование запятой в качестве десятичного разделителя
    )

    # Возвращаем абсолютный путь к созданному файлу
    path = os.path.abspath(filename)

    return filename

