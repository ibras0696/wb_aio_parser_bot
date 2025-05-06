from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from wb_aio_parser_bot.keyboard import admin_start_keyboard
from wb_aio_parser_bot.states.admin_state import (AdminMassSendTextAndVideoState, AdminMassSendTextState, AdminMassSendTextAndPhotoState,
                                     AdminMassSendPhotoState, AdminMassSendVideoState)
from wb_aio_parser_bot.utils.function.admin_function import handle_and_send_text, handle_and_send_photo, \
    handle_and_send_video

from wb_aio_parser_bot.utils.message_text import (photo_text_request, photo_request,
                                                  video_text_request, video_request, text_request, start_admin_text)
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
@router.message(AdminMassSendTextState.text)
async def send_text_message(message: Message, bot: Bot, state: FSMContext):
    text = message.text if message.text is not None else ''
    if len(text) != 0:
        await state.update_data(text=message.text)

        data = await state.get_data()

        await handle_and_send_text(bot=bot, text=data.get('text'))

        await state.clear()
    else:
        await message.answer('⚠️ Нужно отправить Текст ⚠️')
#--------------------------------------------------------

# Отправка Фото
@router.message(AdminMassSendPhotoState.photo)
async def send_photo_message(message: Message, bot: Bot, state: FSMContext):
    if message.photo:
        photo_id = message.photo[-1].file_id

        await state.update_data(photo=photo_id)

        data = await state.get_data()

        await handle_and_send_photo(bot=bot, photo_id=data.get('photo'))
    else:
        await message.answer('⚠️ Нужно отправить Фото ⚠️')
#--------------------------------------------------------

# Отправка Фото и текста
@router.message(AdminMassSendTextAndPhotoState.text)
async def send_text_and_photo_message_cmd_1(message: Message, state: FSMContext):
    text = message.text if message.text is not None else ''
    if len(text) != 0:
        await state.update_data(text=f'{message.text}')
        await message.answer(text='📸 Теперь Фотографию')
        await state.set_state(AdminMassSendTextAndPhotoState.photo)
    else:
        await message.answer('⚠️ Нужно отправить Текст ⚠️')

@router.message(AdminMassSendTextAndPhotoState.photo)
async def send_text_and_photo_message_cmd_2(message: Message, state: FSMContext, bot: Bot):
    if message.photo:
        photo_id = message.photo[-1].file_id

        await state.update_data(photo=photo_id)

        data = await state.get_data()

        await handle_and_send_photo(bot=bot, photo_id=data.get('photo'), text=data.get('text'))
        await state.clear()
    else:
        await message.answer('⚠️ Нужно отправить Фото ⚠️')
#--------------------------------------------------------

#  Отправка только видео
@router.message(AdminMassSendVideoState.video)
async def send_video_message(message: Message, bot: Bot, state: FSMContext):
    if message.video:
        video_id = message.video.file_id
        await state.update_data(video=video_id)

        data = await state.get_data()

        await handle_and_send_video(bot=bot, video_id=data.get('video'))
        await state.clear()
    else:
        await message.answer('⚠️ Нужно отправить Видео ⚠️')

# Отправка видео с текстом
@router.message(AdminMassSendTextAndVideoState.text)
async def send_text_and_video_cmd_1(message: Message, state: FSMContext):
    text = message.text.strip()
    if text:
        await state.update_data(text=text)
        await message.answer(text='📹 Теперь отправьте видео')
        await state.set_state(AdminMassSendTextAndVideoState.video)
    else:
        await message.answer('⚠️ Нужно отправить Текст ⚠️')

@router.message(AdminMassSendTextAndVideoState.video)
async def send_text_and_video_cmd_2(message: Message, state: FSMContext, bot: Bot):
    if message.video:
        video_id = message.video.file_id
        await state.update_data(video=video_id)

        data = await state.get_data()
        await handle_and_send_video(bot=bot, video_id=data.get('video'), text=data.get('text'))
        await state.clear()
    else:
        await message.answer('⚠️ Нужно отправить Видео ⚠️')

#--------------------------------------------------------