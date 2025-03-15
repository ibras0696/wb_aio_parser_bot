import asyncio

from Keyboards.Keyboards_all import inline_keyboard_button, inline_keyboard_buttons


# Стартовые кнопки
start_user_dct = {
    'Обычный Поиск': 'default',
    'Табличный Поиск': 'table'
}
start_user_button = asyncio.run(inline_keyboard_buttons(
    buttons_dct=start_user_dct,
    starts='start_',
    adjust=2,
))