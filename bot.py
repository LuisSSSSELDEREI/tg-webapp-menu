import os
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TimedOut, NetworkError
from telegram.request import HTTPXRequest

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("Не найден TELEGRAM_TOKEN в файле .env")
logger.info(f"Токен загружен: {TOKEN[:10]}...")

WEBAPP_URL = "https://luissssselderei.github.io/tg-webapp-menu/"  # Обновляем URL на актуальный GitHub Pages URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send message with WebApp button"""
    try:
        logger.info(f"Получена команда /start от пользователя {update.effective_user.id}")
        keyboard = [[InlineKeyboardButton(
            text="Открыть меню",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Нажмите кнопку ниже, чтобы открыть меню:",
            reply_markup=reply_markup
        )
        logger.info("Сообщение с кнопкой успешно отправлено")
    except (TimedOut, NetworkError) as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        await asyncio.sleep(1)
        try:
            # Повторная попытка
            await update.message.reply_text(
                "Нажмите кнопку ниже, чтобы открыть меню:",
                reply_markup=reply_markup
            )
            logger.info("Повторная попытка успешна")
        except Exception as e:
            logger.error(f"Повторная попытка не удалась: {e}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Произошла ошибка: {context.error}")

def main():
    """Start the bot"""
    try:
        logger.info("Запуск бота...")
        
        # Создаем HTTP клиент с увеличенным таймаутом
        request = HTTPXRequest(
            connection_pool_size=8,
            read_timeout=30,
            write_timeout=30,
            connect_timeout=30,
        )
        
        # Создаем приложение с настроенным HTTP клиентом
        application = (
            Application.builder()
            .token(TOKEN)
            .request(request)
            .build()
        )

        # Добавляем обработчики
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
