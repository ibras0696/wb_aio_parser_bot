import asyncio

from wb_aio_parser_bot.keyboard.kb_all import inline_keyboard_buttons

dct_btns = {
    '⭐ По рейтингу': '3',
    '📝 По оценкам': '4',
    '💰 По цене(убывание)': '2',
    '💸 По цене(возрастание)': '1',
    '🛍️ Без сортировки!': '0'
}
table_sorting_button = inline_keyboard_buttons(
    buttons_dct=dct_btns,
    starts='table_search_',
    adjust=1
)

dct_btns = {
    '100': 1,
    '200': 2,
    '300': 3,
    '400': 4,
    '500': 5,
    '700': 7,
    '800': 8,
    '900': 9,
    '1000': 10
}
table_total_button = inline_keyboard_buttons(
    buttons_dct=dct_btns,
    starts='table_sorting_',
    adjust=3
)