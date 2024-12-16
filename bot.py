import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TimedOut, NetworkError
from telegram.request import HTTPXRequest

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("Не найден TELEGRAM_TOKEN в файле .env")
logger.info(f"Токен загружен: {TOKEN[:10]}...")

WEBAPP_URL = "https://luissssselderei.github.io/tg-webapp-menu/index.html"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info(f"Получена команда /start от пользователя {update.effective_user.id}")
        keyboard = [[InlineKeyboardButton(
            text="Открыть подарки 🎁",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Нажмите кнопку ниже, чтобы открыть подарки:",
            reply_markup=reply_markup
        )
        logger.info("Сообщение с кнопкой успешно отправлено")
    except (TimedOut, NetworkError) as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        await asyncio.sleep(1)
        try:
            await update.message.reply_text(
                "Нажмите кнопку ниже, чтобы открыть подарки:",
                reply_markup=reply_markup
            )
            logger.info("Повторная попытка успешна")
        except Exception as e:
            logger.error(f"Повторная попытка не удалась: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Произошла ошибка: {context.error}")

def main():
    try:
        logger.info("Запуск бота...")
        
        request = HTTPXRequest(
            connection_pool_size=8,
            read_timeout=30,
            write_timeout=30,
            connect_timeout=30,
        )
        
        application = (
            Application.builder()
            .token(TOKEN)
            .request(request)
            .build()
        )

        application.add_handler(CommandHandler("start", start))
        application.add_error_handler(error_handler)

        logger.info("Бот успешно настроен и запускается...")
        print("Бот запущен. Нажмите Ctrl+C для остановки.")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            read_timeout=30
        )
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}")
        raise

if __name__ == '__main__':
    main()
