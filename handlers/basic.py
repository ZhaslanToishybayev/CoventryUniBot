from telegram import Update
from telegram.ext import ContextTypes
from config import MESSAGES, ADMIN_IDS
from keyboards import get_main_menu_keyboard, get_admin_menu_keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    
    # Проверяем, является ли пользователь администратором
    if user_id in ADMIN_IDS:
        keyboard = get_admin_menu_keyboard()
    else:
        keyboard = get_main_menu_keyboard()
    
    await update.message.reply_text(
        MESSAGES['start'],
        reply_markup=keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
🎓 *Coventry University Bot*

*Доступные команды:*
/start - Главное меню
/help - Справка
/mybookings - Мои бронирования

*Функции бота:*
❓ FAQ - Часто задаваемые вопросы
📝 Booking - Бронирование комнат
📅 События - Университетские события

*Как пользоваться:*
1. Выберите нужный раздел в главном меню
2. Следуйте инструкциям бота
3. Используйте кнопки для навигации

*Поддержка:* @admin
    """
    
    await update.message.reply_text(
        help_text,
        parse_mode='Markdown',
        reply_markup=get_main_menu_keyboard()
    )

async def my_bookings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показать бронирования пользователя"""
    from database import db
    
    user_id = update.effective_user.id
    bookings = db.get_user_bookings(user_id)
    
    if not bookings:
        text = "📝 У вас нет активных бронирований."
    else:
        text = "📝 *Ваши бронирования:*\n\n"
        for booking_id, room_number, club_name, date, start_time, end_time, status in bookings:
            text += f"🏢 {club_name}\n"
            text += f"🚪 Комната {room_number}\n"
            text += f"📅 {date}\n"
            text += f"⏰ {start_time} - {end_time}\n"
            text += f"📊 Статус: {status}\n\n"
    
    await update.message.reply_text(
        text,
        parse_mode='Markdown',
        reply_markup=get_main_menu_keyboard()
    )
