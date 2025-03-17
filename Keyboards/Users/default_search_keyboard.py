import asyncio

from wb_aio_parser_bot.Keyboards.Keyboards_all import inline_keyboard_button, inline_keyboard_buttons

dct_btns = {
    '⭐ По рейтингу': '3',
    '📝 По оценкам': '4',
    '💰 По цене(убывание)': '2',
    '💸 По цене(возрастание)': '1',
    '🛍️ Без сортировки!': '0'
}
default_sorting_button = inline_keyboard_buttons(
    buttons_dct=dct_btns,
    starts='def_search_',
    adjust=1
)

dct_btns = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10
}
default_total_button = inline_keyboard_buttons(
    buttons_dct=dct_btns,
    starts='def_sorting_',
    adjust=3
)