from aiogram import Router, F
from aiogram.types import CallbackQuery

from wb_aio_parser_bot.Handlers.Users.SendTextMessage.message_text import info_search_default_message


# Импорт состояний

# Импорт Клавиатур
from wb_aio_parser_bot.Keyboards.Users.user_keyboards import back_start_keyboard


router = Router()

@router.callback_query(F.data == 'default')
async def default_search_cmd(call_back: CallbackQuery):
    await call_back.message.edit_text(text=info_search_default_message, reply_markup=back_start_keyboard)