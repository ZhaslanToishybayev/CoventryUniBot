import logging
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

# Импорты наших модулей
from config import BOT_TOKEN, ADMIN_IDS
from database import db
from handlers.basic import start_command, help_command, my_bookings_command
from handlers.callbacks import handle_callback
from handlers.admin import create_event_command, add_faq_command, admin_help_command

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update: Update, context):
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")

async def unknown_command(update: Update, context):
    """Обработчик неизвестных команд"""
    await update.message.reply_text(
        "❌ Неизвестная команда. Используйте /help для получения справки."
    )

def main():
    """Основная функция запуска бота"""
    # Проверяем токен
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Ошибка: Не установлен BOT_TOKEN!")
        print("Создайте файл .env и добавьте:")
        print("BOT_TOKEN=your_actual_bot_token")
        print("ADMIN_IDS=your_user_id")
        return

    # Инициализируем базу данных
    print("🔄 Инициализация базы данных...")
    db.init_database()
    print("✅ База данных инициализирована")

    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("mybookings", my_bookings_command))

    # Админские команды
    application.add_handler(CommandHandler("create_event", create_event_command))
    application.add_handler(CommandHandler("add_faq", add_faq_command))
    application.add_handler(CommandHandler("admin_help", admin_help_command))

    # Обработчик callback запросов
    application.add_handler(CallbackQueryHandler(handle_callback))

    # Обработчик неизвестных команд
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Обработчик ошибок
    application.add_error_handler(error_handler)

    print("🚀 Бот запускается...")
    print(f"👨‍💼 Администраторы: {ADMIN_IDS}")

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()