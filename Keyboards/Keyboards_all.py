# Кнопки пользователей
import asyncio

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


# Inline Keyboard
async def inline_keyboard_buttons(buttons_dct: dict, starts: str='st_', adjust: int=2, url_btn: bool= False) -> InlineKeyboardMarkup:
    '''
    Функция возвращает несколько кнопок
    :param buttons_dct: Словарь {кнопка: ссылка или callback}
    :param starts: Начало callback
    :param adjust: общий ряд сколь кнопок должно быть в ряд
    :param url_btn: Если поставить True передаваться будут ссылки
    :return: InlineKeyboardMarkup
    '''
    try:
        if url_btn:
            kb = InlineKeyboardBuilder()
            for key, value in buttons_dct.items():
                kb.add(InlineKeyboardButton(text=key, url=value))
            return kb.adjust(adjust).as_markup()
        else:
            kb = InlineKeyboardBuilder()
            for key, value in buttons_dct.items():
                kb.add(InlineKeyboardButton(text=key, callback_data=f'{starts}{value}'))
            return kb.adjust(adjust).as_markup()
    except Exception as ex:
        raise f'Ошибка: {ex}'


# Inline Keyboard
async def inline_keyboard_button(buttons_dct: dict, starts: str='st_', url_btn: bool= False)-> InlineKeyboardMarkup:
    '''
    Функция возвращает только одну кнопку
    :param buttons_dct: Словарь {кнопка: ссылка или callback}
    :param starts: Начало callback
    :param url_btn: Если поставить True передаваться будут ссылки
    :return: InlineKeyboardMarkup
    '''
    try:
        if url_btn:
            for key, value in buttons_dct.items():
                kb = InlineKeyboardMarkup(inline_keyboard=(
                    [[InlineKeyboardButton(text=key, url=value)]]
                ))
                return kb
        else:
            for key, value in buttons_dct.items():
                kb = InlineKeyboardMarkup(inline_keyboard=(
                    [[InlineKeyboardButton(text=key, callback_data=f'{starts}{value}')]]
                ))
                return kb
    except Exception as ex:
        raise f'Ошибка: {ex}'