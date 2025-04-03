from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from wb_aio_parser_bot.Keyboards import massing_admin_send_message, admin_start_keyboard
from wb_aio_parser_bot.States import (AdminMassSendTextAndVideoState, AdminMassSendTextState, AdminMassSendTextAndPhotoState,
                                      AdminMassSendPhotoState, AdminMassSendVideoState)

from wb_aio_parser_bot.SendTextMessage import (photo_text_request, photo_request,
                                               video_text_request, video_request, text_request, mass_send_text,
                                               start_admin_text)
router = Router()

@router.callback_query(F.data.startswith('send_mass_'))
async def handle_mass_message_callback(call_back: CallbackQuery, state: FSMContext):
    call_data = call_back.data.replace('send_mass_', '')

    await state.clear()

    match call_data:
        # Отправка и обработка текста, фото и видео
        case 'text':
            await call_back.message.answer(text=text_request)
            await state.set_state(AdminMassSendTextState.text)
        case 'photo':
            await call_back.message.answer(text=photo_request)
            await state.set_state(AdminMassSendPhotoState.photo)
        case 'photo_text':
            await call_back.message.answer(text=photo_text_request)
            await state.set_state(AdminMassSendTextAndPhotoState.text)
        case 'video':
            await call_back.message.answer(text=video_request)
            await state.set_state(AdminMassSendVideoState.video)
        case 'video_text':
            await call_back.message.answer(text=video_text_request)
            await state.set_state(AdminMassSendTextAndVideoState.text)
        case 'back':
            await call_back.message.delete()
            await call_back.message.answer(text=start_admin_text, reply_markup=admin_start_keyboard)
        case _:
            pass

# Отправка Текста
# @router.message(AdminMassSendTextState.text)
# async def send_text_message_handler(message: Message, state: FSMContext):





