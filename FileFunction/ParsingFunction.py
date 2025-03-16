import aiohttp
from typing import Dict, List, Any, Optional


# Код Прошел ревью Deepseek
async def parsing_function_wb(
        search: str,
        page: int = 1,
        sorting: int = None,
        limit: Optional[int] = None
) -> Dict[str, List[Any]]:
    """
    Асинхронно парсит данные с Wildberries по заданному запросу.

    :param search: Поисковый запрос.
    :param page: Количество страниц для парсинга (по умолчанию 1).
    :param sorting: Тип сортировки (1 Возрастанию, 2 Убыванию, 3 Рейтинг, 4 Оценки).
    :param limit: Ограничение на количество возвращаемых товаров (по умолчанию None — все товары).
    :return: Словарь с результатами парсинга.
    """
    # Базовый URL для запроса
    base_url = 'https://search.wb.ru/exactmatch/ru/common/v9/search'

    # Инициализация словаря для результатов
    dct_result = {
        'Бренд': [],
        'Название': [],
        'Цена после скидки': [],
        'Цена до скидки': [],
        'Рейтинг': [],
        'Оценки': [],
        'Артикул': [],
        'Ссылка': []
    }
    # Асинхронный HTTP-клиент
    async with aiohttp.ClientSession() as session:
        for pa in range(1, page + 1):
            # Формируем URL с учетом номера страницы
            url = f'{base_url}?ab_testing=false&appType=1&curr=rub&dest=-1116963&hide_dtype=10&lang=ru&page={pa}&query={search}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false'

            # Выполняем запрос
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json(encoding='utf-8', content_type=None)

                    # Проверяем, есть ли товары
                    if not data.get('data', {}).get('products'):
                        break

                    # Парсим данные о товарах
                    for product in data['data']['products']:
                        # Бренд товара
                        brand = product.get('brand', '')
                        # Полное название товара
                        name = product.get('name', '')
                        # Цена после скидки
                        price_after = product.get('sizes', [{}])[0].get('price', {}).get('total', 0) / 100
                        # Цена до скидки
                        price_before = product.get('sizes', [{}])[0].get('price', {}).get('basic', 0) / 100
                        # Рейтинг товара
                        rating = product.get('nmReviewRating', 0)
                        # Количество оценок
                        total = product.get('feedbacks', 0)
                        # Артикул
                        artikul = product.get('id', '')
                        # Ссылка на товар
                        product_url = f'https://www.wildberries.ru/catalog/{artikul}/detail.aspx?targetUrl=SP'

                        # Добавляем данные в словарь
                        dct_result['Бренд'].append(brand)
                        dct_result['Название'].append(name)
                        dct_result['Цена после скидки'].append(price_after)
                        dct_result['Цена до скидки'].append(price_before)
                        dct_result['Рейтинг'].append(rating)
                        dct_result['Оценки'].append(total)
                        dct_result['Артикул'].append(artikul)
                        dct_result['Ссылка'].append(product_url)
                else:
                    print(f"Ошибка при запросе: {response.status}")
                    break
    # Сортировка результатов
    if sorting == 1:
        # Сортировка по возрастанию цены (Цена после скидки)
        sorted_indices = sorted(range(len(dct_result['Цена после скидки'])),
                                key=lambda x: dct_result['Цена после скидки'][x])
    elif sorting == 2:
        # Сортировка по убыванию цены (Цена после скидки)
        sorted_indices = sorted(range(len(dct_result['Цена после скидки'])),
                                key=lambda x: dct_result['Цена после скидки'][x], reverse=True)
    elif sorting == 3:
        # Сортировка по рейтингу
        sorted_indices = sorted(range(len(dct_result['Рейтинг'])), key=lambda x: dct_result['Рейтинг'][x],
                                reverse=True)
    elif sorting == 4:
        # Сортировка по количеству оценок
        sorted_indices = sorted(range(len(dct_result['Оценки'])), key=lambda x: dct_result['Оценки'][x],
                                reverse=True)
    else:
        # Если sorting не указан, возвращаем без сортировки
        sorted_indices = range(len(dct_result['Бренд']))

    # Применяем сортировку ко всем спискам в словаре
    for key in dct_result:
        dct_result[key] = [dct_result[key][i] for i in sorted_indices]

    # Ограничение количества товаров если нужно
    if limit is not None and limit > 0:
        for key in dct_result:
            dct_result[key] = dct_result[key][:limit]

    return dct_result
