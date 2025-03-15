from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from DataBase.crud import register_user_in_table
from Keyboards.Users.user_keyboards import start_user_button

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message):
    # Функция для регистрации пользователя
    result = await register_user_in_table(
        telegram_id=message.chat.id,
        telegram_name=message.chat.username,
    )
    await message.answer('''
    👋 Привет! Я — твой помощник по работе с Wildberries! 🛍️

    С моей помощью ты можешь:
    \n✅ Найти товары по названию.
    \n✅ Получить подробную информацию: название, ссылку, артикул, цену, рейтинг и оценки.
    \n✅ Увидеть данные в виде текста или удобной таблицы, если товаров много.
    
    Чтобы начать, просто отправь мне название товара. Я сделаю всё остальное! 🚀
    
    Нажми /help, если нужна инструкция. 😊
    ''', reply_markup=start_user_button)

@router.callback_query(F.data.startswith('start_'))
async def start_call_cmd(call_back: CallbackQuery):
    data = call_back.message.text.replace('start_', '')
    match data:
        case 'default':
            pass

        case 'table':
            pass
