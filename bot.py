import os
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBAPP_URL = "https://ваш_юзернейм.github.io/tg-webapp-menu/"  # Замените на ваш URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send message with WebApp button"""
    keyboard = [[InlineKeyboardButton(
        text="Открыть меню",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Нажмите кнопку ниже, чтобы открыть меню:",
        reply_markup=reply_markup
    )

def main():
    """Start the bot"""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
