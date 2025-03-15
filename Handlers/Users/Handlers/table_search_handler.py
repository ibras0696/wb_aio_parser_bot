from aiogram import Router, F
from aiogram.types import CallbackQuery

# Импорт состояний

# Импорт текстов
from Handlers.Users.SendTextMessage.message_text import info_table_message

# Импорт Клавиатур
from Keyboards.Users.user_keyboards import back_start_keyboard

router = Router()


@router.callback_query(F.data == 'table')
async def table_search_cmd(call_back: CallbackQuery):
    await call_back.message.edit_text(text=info_table_message, reply_markup=back_start_keyboard)