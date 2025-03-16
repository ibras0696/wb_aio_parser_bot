from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from wb_aio_parser_bot.Handlers.Users.SendTextMessage.message_text import info_search_default_message


# Импорт состояний
from wb_aio_parser_bot.States.user_states import SearchStates

# Импорт Клавиатур
from wb_aio_parser_bot.Keyboards.Users.user_keyboards import back_start_keyboard

from wb_aio_parser_bot.Keyboards.Users.default_search_keyboard import default_search_button, default_sorting_button

# Функция для парсминга данных
from wb_aio_parser_bot.FileFunction.ParsingFunction import parsing_function_wb

router = Router()


@router.callback_query(F.data == 'default') # Обработчик для Обычного поиска
async def default_search_cmd(call_back: CallbackQuery, state: FSMContext):
    # Очистка прежних состояний
    await state.clear()
    # Работа с состояниями
    await state.set_state(SearchStates.search)
    # Отправка сообщении и сменя состояний
    await call_back.message.edit_text(text=info_search_default_message, reply_markup=back_start_keyboard)


@router.message(SearchStates.search)
async def search_state_cmd(message: Message, state: FSMContext):
    if message.text is not None and len(message.text) != 0:

        await state.update_data(search=message.text)
        await state.set_state(SearchStates.sorting)

        await message.answer('Сортировка товаров:', reply_markup=default_search_button)
    else:
        # Работа с состояниями
        await state.set_state(SearchStates.search)

        await message.answer('Нужно ввести текст! ')


@router.callback_query(F.data.startswith('def_search_'))
async def sorting_state_cmd(call_back: CallbackQuery, state: FSMContext):
    call_data = call_back.data.replace('def_search_', '')

    await state.update_data(sorting=call_data)
    await state.set_state(SearchStates.limited)

    await call_back.message.edit_text('Количество Товаров 🛍️', reply_markup=default_sorting_button)


@router.callback_query(F.data.startswith('def_sorting_'))
async def result_search_cmd(call_back: CallbackQuery, state: FSMContext):
    call_data = call_back.data.replace('def_sorting_', '')
    await state.update_data(limited=call_data)
    data = await state.get_data()
    search = data.get('search')
    sorting = data.get('sorting')
    limited = data.get('limited')
    try:
        result = await parsing_function_wb(
            search=search,
            sorting=sorting,
            limit=limited
        )
    except Exception:
        await call_back.message.answer('Попробуйте чуть позже возникла ошибка! ')


