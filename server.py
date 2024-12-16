from flask import Flask, send_file
import os
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)
load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBAPP_URL = "https://your-domain.com"  # Замените на ваш домен

# Маршрут для отдачи HTML файла
@app.route('/')
def serve_webapp():
    return send_file('index.html')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send message with WebApp button"""
    keyboard = [[KeyboardButton(
        text="Открыть меню",
        web_app=WebAppInfo(url=f"{WEBAPP_URL}")
    )]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Нажмите кнопку ниже, чтобы открыть меню:",
        reply_markup=reply_markup
    )

def main():
    """Start the bot and Flask server"""
    # Create application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))

    # Start the Flask server
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)).start()

    # Start the bot
    print("Бот и сервер запущены")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
