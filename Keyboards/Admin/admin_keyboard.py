from wb_aio_parser_bot.Keyboards.Keyboards_all import inline_keyboard_button, inline_keyboard_buttons


# Клавиатура стартовая для админ панели
ad_dct = {
    'Взаимодействие с Базой Данных': 'data_db'
}
admin_start_keyboard = inline_keyboard_buttons(
    buttons_dct=ad_dct,
    starts='admin_',
    adjust=2
)