from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

# Импорт Клавиатур
from wb_aio_parser_bot.Keyboards.Admin.admin_keyboard import admin_start_keyboard

from wb_aio_parser_bot.Config.conf import ID_ADMIN

router = Router()

@router.message(Command('admin'))
async def admin_cmd(message: Message):
    if message.chat.id == ID_ADMIN:
        await message.answer(f'Добро пожаловать в Админ Панель'
                             f'\nПанель создана для управлением скрытых Данных в Боте',
                             reply_markup=admin_start_keyboard)
