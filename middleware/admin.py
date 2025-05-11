from datetime import datetime
from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware, Bot
from aiogram.types import Update
from config import ID_ADMIN
import traceback
import logging
import asyncio

from database import save_error_to_db


class ErrorHandlerMiddleware(BaseMiddleware):
    """
    Middleware для глобального перехвата ошибок в Aiogram 3.
    При возникновении исключений:
    - логирует ошибку в консоль;
    - отправляет уведомление админу;
    - записывает информацию в базу данных.
    """

    async def __call__(
        self,
        handler: Callable[[Update, dict], Awaitable[Any]],
        event: Update,
        data: dict
    ) -> Any:
        try:
            return await handler(event, data)

        except Exception as e:
            bot: Bot = data.get("bot")
            tb = traceback.format_exc()
            logging.error(f"Ошибка при обработке события: {tb}")

            # Безопасно определяем Telegram ID
            telegram_id = None
            telegram_name = None
            if event.message:
                telegram_id = event.message.from_user.id
                telegram_name = event.message.from_user.username
            elif event.callback_query:
                telegram_id = event.callback_query.from_user.id
                telegram_name = event.callback_query.from_user.username
            elif event.inline_query:
                telegram_id = event.inline_query.from_user.id
                telegram_name = event.inline_query.from_user.username

            # Получаем текущую дату и время
            now = datetime.now()

            # Форматируем в нужный формат
            formatted_time = now.strftime("%H:%M %d.%m.%Y")

            # Отправка админу
            if bot:
                await bot.send_message(
                    chat_id=ID_ADMIN,
                    text=f"❌ Ошибка!"
                         f"\nТелеграм ID: {telegram_id}"
                         f"\nТелеграм Ник: {telegram_name}"
                         f"\nВремя: {formatted_time}"
                         f"\n\n<b>{type(e).__name__}:</b> {e}\n\n<pre>{tb[-500:-1]}</pre>",
                    parse_mode="HTML"
                )

            # Сохраняем ошибку в БД (через run_in_executor, чтобы не блокировать event loop)
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, save_error_to_db, telegram_id, tb[-500:-1])

            raise
