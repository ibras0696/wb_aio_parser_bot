from typing import Dict, List, Any

import pytest

from utils import parsing_function_wb

# Тестирование url для парсера


# Тестирование Парсера
@pytest.mark.asyncio
@pytest.mark.parametrize(
    'search, page, sorting, limit, result',
    [
        ('игра', 1, 1, None, Dict[str, List[Any]]),
        ('еда', 10, 2, None, Dict[str, List[Any]]),
        ('цвет', 1, 3, 10, Dict[str, List[Any]]),
        ('хлеб', 1, 3, 5, Dict[str, List[Any]]),

    ]
)
async def test_parsing_function_wb(search, page, sorting, limit, result):
    #  Получение данных парсера
    result = await parsing_function_wb(search=search, page=page, limit=limit)
    # Проверка полученных данных
    assert type(result) == dict
    print('Тестирование Парсер WB Успешно')



