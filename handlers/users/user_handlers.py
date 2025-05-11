from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

# Импорт функции для взаимодействий с БД
from database import register_user_in_table

# Импорт клавиатур
from keyboard.users import start_user_button

# Импорт Текстов для сообщений
from utils.message_text import welcome_message, start_help_text

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    # Очищение состояний
    await state.clear()
    # Функция для регистрации пользователя
    register_user_in_table(
        telegram_id=message.chat.id,
        telegram_name=message.chat.username,
    )
    await message.answer(text=welcome_message, reply_markup=start_user_button)


@router.callback_query(F.data.startswith('start_'))
async def back_start_cmd(call_back: CallbackQuery, state: FSMContext):
    # Очищение состояний
    await state.clear()
    await call_back.message.edit_text(text=welcome_message, reply_markup=start_user_button)


# Обработка help
@router.message(Command('help'))
async def help_cmd(message: Message, state: FSMContext):
    # Очистка прежних состояний
    await state.clear()
    await message.answer(text=start_help_text)


@router.message(Command('test'))
async def test_cmd(message: Message):
    await message.answer('Вызов ошибки')
    raise Exception('Ошибка в test handler')
