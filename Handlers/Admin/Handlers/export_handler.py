import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from wb_aio_parser_bot.FileFunction import export_db, export_users_table_csv, export_search_table_csv, export_logs_table_table_csv

from wb_aio_parser_bot.Keyboards.Admin import export_admin_db_keyboard, export_admin_table_keyboard, \
    admin_start_keyboard
from wb_aio_parser_bot.SendTextMessage import start_admin_text

router = Router()

@router.message(Command('lol'))
async def test_cmd(message: Message):
    await message.answer('Кнопка')

@router.callback_query(F.data.startswith('export_'))
async def admin_export_cmd(call_back: CallbackQuery):
    call_data = call_back.data.replace('export_', '')
    match call_data:
        # Экспорт Базы данных в виде файла в формате db
        case 'db':
            await call_back.message.delete()
            await call_back.message.answer_document(document=export_db(),
                                                    caption='✅ БАЗА ДАННЫХ УСПЕШНО ЭКСПОРТИРОВАНА!\n• 📦 Полная резервная копия (SQL)',)
        case 'table':
            await call_back.message.edit_text(text='📋 Доступные таблицы:', reply_markup=export_admin_table_keyboard)
        case 'back':
            await call_back.message.edit_text(text=start_admin_text, reply_markup=admin_start_keyboard)
        case _:
            await call_back.answer("Неизвестная команда!", show_alert=True)

@router.callback_query(F.data.startswith('table_admin_'))
async def admin_export_table_cmd(call_back: CallbackQuery):
    send_text = '✅ ДАННЫЕ УСПЕШНО ЭКСПОРТИРОВАНЫ 📦\n'
    call_data = call_back.data.replace('table_admin_', '')
    match call_data:
        case 'users':
            result = export_users_table_csv()
            await call_back.message.answer_document(caption=send_text, document=result.get('fsi_input_file'))
            os.remove(result.get('file_name'))
        case 'search_table':
            result = export_search_table_csv()
            await call_back.message.answer_document(caption=send_text,
                                                    document=result.get('fsi_input_file'))
            os.remove(result.get('file_name'))
        case 'log_table':
            result = export_logs_table_table_csv()
            await call_back.message.answer_document(caption=send_text,
                                                    document=result.get('fsi_input_file'))
            os.remove(result.get('file_name'))
        case 'back':
            await call_back.message.delete()
            await call_back.message.answer(text='🗃️ Управление базой данных', reply_markup=export_admin_db_keyboard)
        case _:
            await call_back.answer("Неизвестная команда!", show_alert=True)