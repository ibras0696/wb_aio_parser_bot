from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

# Фильтр админа
from filters import is_admin_filter, call_is_admin_filter

# Импорт Клавиатур
from keyboard.admin import massing_admin_send_message, admin_start_keyboard, export_admin_db_keyboard

from utils.message_text import start_admin_text, mass_send_text

router = Router()


@router.message(Command('admin'), is_admin_filter)
async def admin_cmd(message: Message):
    await message.answer(text=start_admin_text,
                         reply_markup=admin_start_keyboard)


@router.callback_query(F.data.startswith('admin_'), call_is_admin_filter)
async def call_back_admin_cmd(call_back: CallbackQuery):

    data_call = call_back.data.replace('admin_', '')

    match data_call:
        case 'data_db':
            await call_back.message.edit_text(text='🗃️ Управление базой данных', reply_markup=export_admin_db_keyboard)
        case 'send_message':
            await call_back.message.edit_text(text=mass_send_text, reply_markup=massing_admin_send_message)
        # case 'control':
        #     await call_back.message.edit_text(text='', reply_markup=None)
        # case _:
        #     return
