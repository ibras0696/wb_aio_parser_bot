import asyncio

# Импорт Основных Клавиатур
from wb_aio_parser_bot.Keyboards.Keyboards_all import inline_keyboard_button, inline_keyboard_buttons

# Стартовые кнопки
start_user_dct = {
    '🔍 Обычный Поиск': 'default',
    '📊 Табличный Поиск': 'table'
}
start_user_button = inline_keyboard_buttons(
    buttons_dct=start_user_dct,
    starts='',
    adjust=2,
)

back_start_keyboard = inline_keyboard_button(
    buttons_dct={'🔙 Назад': 'back'},
    starts='start_',
)
