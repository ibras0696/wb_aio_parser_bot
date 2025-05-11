import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, FSInputFile

# Функция для работы с БД
from database import search_reg_table

# Функция для работы с данными и создания csv файла
from utils import create_csv_file

# Импорт функции Парсинга
from utils.parsing import parsing_function_wb

# Импорт состояний
from states.user_state import TableSearchStates

# Импорт текстов
from utils.message_text import info_table_message, welcome_message, \
    table_send_result_message

# Импорт Клавиатур
from keyboard.users import back_start_keyboard, start_user_button
# Импорт Клавиатур
from keyboard.users import table_sorting_button, table_total_button

router = Router()


@router.callback_query(F.data == 'table')
async def table_search_cmd(call_back: CallbackQuery, state: FSMContext):
    await state.clear()

    await call_back.message.edit_text(text=info_table_message, reply_markup=back_start_keyboard)

    await state.set_state(TableSearchStates.search)


@router.message(TableSearchStates.search)
async def table_search_cmd(message: Message, state: FSMContext):
    if message.text is not None and len(message.text) != 0:
        await state.update_data(search=message.text)
        await state.set_state(TableSearchStates.sorting)

        await message.answer('Сортировка товаров:', reply_markup=table_sorting_button)
    else:
        # Работа с состояниями
        await state.set_state(TableSearchStates .search)

        await message.answer('Нужно ввести текст! ')

@router.callback_query(F.data.startswith('table_search_'))
async def sorting_state_cmd(call_back: CallbackQuery, state: FSMContext):
    call_data = call_back.data.replace('table_search_', '')

    await state.update_data(sorting=call_data)
    await state.set_state(TableSearchStates.total)

    await call_back.message.edit_text('Количество Товаров 🛍️', reply_markup=table_total_button)


@router.callback_query(F.data.startswith('table_sorting_'))
async def result_search_cmd(call_back: CallbackQuery, state: FSMContext):
    call_data = call_back.data.replace('table_sorting_', '')
    await call_back.message.delete()

    await state.update_data(total=call_data)

    # Получение данных и их обработка
    data = await state.get_data()
    search = data.get('search')
    sorting = int(data.get('sorting'))
    total = int(data.get('total'))

    try:
        # Сбор данных Парсинг
        result = await parsing_function_wb(
            search=search,
            sorting=sorting,
            page=total
        )
        if len(result.get('Бренд')) != 0:

            # Создания Таблицы и возврат пути к нему
            file_name = f'{call_back.message.chat.id}_file'
            path_csv = create_csv_file(result, file_name)

            # Отправка файла
            file_result = FSInputFile(path_csv)
            await call_back.message.answer_document(caption=table_send_result_message, document=file_result)
            # Удаление Файла
            os.remove(path_csv)
    except Exception as ex:
        await call_back.message.answer(f'Попробуйте чуть позже возникла ошибка! {ex}')
    finally:
        await search_reg_table(
            telegram_id=call_back.message.chat.id,
            search=search,
            type_search='Table'
        )
        # Очистка прежних состояний
        await state.clear()
        await call_back.message.answer(text=welcome_message, reply_markup=start_user_button)