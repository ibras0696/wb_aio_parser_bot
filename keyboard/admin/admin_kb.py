from keyboard import inline_keyboard_button, inline_keyboard_buttons


# Клавиатура стартовая для админ панели
admin_start_keyboard = inline_keyboard_buttons(
    buttons_dct={
    '🗃️ Управление базой данных': 'data_db',
    '📩 Рассылка сообщений': 'send_message',
},
    starts='admin_',
    adjust=2
)


# Клавиатура для работа с базой данных
export_admin_db_keyboard = inline_keyboard_buttons(
    buttons_dct={
    '📤  Экспорт полной базы данных': 'db',
    '📊  Выгрузка отдельных таблиц': 'table',
    '🔙 Назад в главное меню': 'back'
},
    starts='export_',
    adjust=1
)

# Клавиатура для получения определенной таблицы
export_admin_table_keyboard = inline_keyboard_buttons(
    buttons_dct={
        '👥 Пользователи': 'users',
        '🛒 Данные Запросов': 'search_table',
        '📝 Логи': 'log_table',
        '🔙 Назад': 'back'
    },
    starts='table_admin_',
    adjust=1
)


# Клавиатура для работы с массовой рассылкой
massing_admin_send_message = inline_keyboard_buttons(
    buttons_dct={
        '📄 Текст': 'text',
        '📸 Фотография':'photo',
        '🖼️ Фото + Текст 📄': 'photo_text',
        '🎥 Видео': 'video',
        '🎥 Видео + Текст 📄': 'video_text',
        '🔙 Назад': 'back'
    },
    starts='send_mass_',
    adjust=1
)