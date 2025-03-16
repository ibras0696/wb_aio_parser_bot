from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

# Импорт функции для взаимодействий с БД
from wb_aio_parser_bot.DataBase.crud import register_user_in_table

# Импорт клавиатур
from wb_aio_parser_bot.Keyboards.Users.user_keyboards import start_user_button

# Импорт Текстов для сообщений
from wb_aio_parser_bot.Handlers.Users.SendTextMessage.message_text import welcome_message


router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    # Очищение состояний
    await state.clear()
    # Функция для регистрации пользователя
    await register_user_in_table(
        telegram_id=message.chat.id,
        telegram_name=message.chat.username,
    )
    await message.answer(text=welcome_message, reply_markup=start_user_button)


@router.callback_query(F.data.startswith('start_'))
async def back_start_cmd(call_back: CallbackQuery, state: FSMContext):
    # Очищение состояний
    await state.clear()
    await call_back.message.edit_text(text=welcome_message, reply_markup=start_user_button)


