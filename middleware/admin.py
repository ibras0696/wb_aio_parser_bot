from aiogram import BaseMiddleware, Bot
from aiogram.types import Update
from wb_aio_parser_bot.config import ID_ADMIN
import traceback
import logging


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict):
        try:
            return await handler(event, data)
        except Exception as e:
            bot: Bot = data.get("bot")  # Извлекаем бота из контекста
            tb = traceback.format_exc()
            logging.error(f"Ошибка при обработке события: {tb}")

            # Отправляем админу
            if bot:
                await bot.send_message(
                    chat_id=ID_ADMIN,
                    text=f"❌ Ошибка!\n\n{type(e).__name__}: {e}\n\n{tb}",
                    parse_mode="HTML"
                )