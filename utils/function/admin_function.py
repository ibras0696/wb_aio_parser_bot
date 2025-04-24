from typing import Any, List, Dict

from aiogram import Bot
from aiogram.types import Message

from wb_aio_parser_bot.database.crud import all_get_table_info

from wb_aio_parser_bot.database.models import *


# Получение id всех пользователей из БД
def get_user_ids() -> List:
    '''
    Получение всех айди из бд
    :return: list[telegram_id1, telegram_id2, telegram_id3]
    '''
    result = all_get_table_info(USERS_TABLE, ['telegram_id'])
    return result.get('telegram_id')

# Массовая отправка текста
async def handle_and_send_text(bot: Bot, text: str = None) -> Dict[str, str | bool]:
    '''
    Массовая отправка теста
    :param bot: Класс бота
    :param text: Текст для передачи если оставить None отправляется только видео
    :return: dict{'telegram_id': log | True}
    '''
    dct = {}
    # Телеграмм ID Пользователей, передать списком list
    user_ids = get_user_ids()

    for user_id in user_ids:
        try:
            await bot.send_message(chat_id=user_id, text=f'{text}')

            dct[user_id] = True

        except Exception as ex:
            dct[user_id] = ex

    return dct


# Массовая отправка фото или фото с текстом
async def handle_and_send_photo(bot: Bot, photo_id: Any, text: str = None) -> Dict[str, str | bool]:
    '''
    Массовая отправка фото или фото с текстом
    :param bot: Класс бота
    :param photo_id: message.photo.file_id нужен айди видео
    :param text: Текст для передачи если оставить None отправляется только видео
    :return: dict{'telegram_id': log | True}
    '''
    dct = {}

    # Телеграмм ID Пользователей, передать списком list
    user_ids = get_user_ids()

    for user_id in user_ids:
        if text is not None:
            try:
                await bot.send_photo(chat_id=user_id, photo=photo_id, caption=text)

                dct[user_id] = True
            except Exception as ex:
                dct[user_id] = ex
        else:
            try:
                await bot.send_photo(chat_id=user_id, photo=photo_id)

                dct[user_id] = True
            except Exception as ex:
                dct[user_id] = ex

    return dct

# Массовая отправка видео или видео с текстом
async def handle_and_send_video(bot: Bot, video_id: Any, text: str = None) -> Dict[str, str | bool]:
    '''
    Массовая отправка видео или видео с текстом
    :param bot: Класс бота
    :param video_id: message.video.file_id нужен айди видео
    :param text: Текст для передачи если оставить None отправляется только видео
    :return: dict{'telegram_id': log | True}
    '''
    dct = {}

    # Телеграмм ID Пользователей, передать списком list
    user_ids = get_user_ids()

    for user_id in user_ids:
        if text is not None:
            try:
                await bot.send_video(chat_id=user_id, video=video_id, caption=text)

                dct[user_id] = True
            except Exception as ex:
                dct[user_id] = ex
        else:
            try:
                await bot.send_video(chat_id=user_id, video=video_id)

                dct[user_id] = True
            except Exception as ex:
                dct[user_id] = ex
    return dct
