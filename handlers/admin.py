from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS, MESSAGES
from keyboards import get_main_menu_keyboard, get_admin_menu_keyboard
from database import db

async def create_event_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда создания события (только для админов)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text(
            "❌ У вас нет прав для выполнения этой команды.",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    # Получаем текст команды
    text = update.message.text
    
    # Убираем команду из текста
    if text.startswith('/create_event'):
        event_data = text[13:].strip()  # Убираем '/create_event '
    else:
        await update.message.reply_text(
            "❌ Неверный формат команды.\n\n"
            "Используйте: `/create_event Название | Описание | YYYY-MM-DD`",
            parse_mode='Markdown',
            reply_markup=get_admin_menu_keyboard()
        )
        return
    
    if not event_data:
        await update.message.reply_text(
            "📝 Для создания события используйте формат:\n\n"
            "`/create_event Название события | Описание | YYYY-MM-DD`\n\n"
            "Пример:\n"
            "`/create_event Лекция по AI | Интересная лекция о машинном обучении | 2024-02-15`",
            parse_mode='Markdown',
            reply_markup=get_admin_menu_keyboard()
        )
        return
    
    try:
        # Парсим данные события
        parts = [part.strip() for part in event_data.split('|')]
        
        if len(parts) < 2:
            raise ValueError("Недостаточно данных")
        
        title = parts[0]
        description = parts[1] if len(parts) > 1 else ""
        date = parts[2] if len(parts) > 2 else None
        
        if not title:
            raise ValueError("Название не может быть пустым")
        
        # Создаем событие
        event_id = db.create_event(title, description, date, user_id)
        
        if event_id:
            text = f"✅ *Событие создано успешно!*\n\n"
            text += f"📅 Название: {title}\n"
            if description:
                text += f"📝 Описание: {description}\n"
            if date:
                text += f"📆 Дата: {date}\n"
            text += f"🆔 ID события: #{event_id}"
            
            await update.message.reply_text(
                text,
                parse_mode='Markdown',
                reply_markup=get_admin_menu_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ Ошибка при создании события. Попробуйте еще раз.",
                reply_markup=get_admin_menu_keyboard()
            )
    
    except Exception as e:
        await update.message.reply_text(
            "❌ Ошибка в формате данных.\n\n"
            "Используйте: `/create_event Название | Описание | YYYY-MM-DD`\n\n"
            "Все части разделяются символом `|`",
            parse_mode='Markdown',
            reply_markup=get_admin_menu_keyboard()
        )

async def add_faq_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда добавления FAQ (только для админов)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text(
            "❌ У вас нет прав для выполнения этой команды.",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    text = update.message.text
    
    if text.startswith('/add_faq'):
        faq_data = text[8:].strip()  # Убираем '/add_faq '
    else:
        await update.message.reply_text(
            "❌ Неверный формат команды.\n\n"
            "Используйте: `/add_faq Вопрос | Ответ`",
            parse_mode='Markdown',
            reply_markup=get_admin_menu_keyboard()
        )
        return
    
    if not faq_data:
        await update.message.reply_text(
            "📝 Для добавления FAQ используйте формат:\n\n"
            "`/add_faq Вопрос | Ответ`\n\n"
            "Пример:\n"
            "`/add_faq Как подать документы? | Документы подаются через онлайн портал`",
            parse_mode='Markdown',
            reply_markup=get_admin_menu_keyboard()
        )
        return
    
    try:
        parts = [part.strip() for part in faq_data.split('|')]
        
        if len(parts) != 2:
            raise ValueError("Неверное количество частей")
        
        question, answer = parts
        
        if not question or not answer:
            raise ValueError("Вопрос и ответ не могут быть пустыми")
        
        # Добавляем FAQ в базу
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO faq (question, answer) VALUES (?, ?)', (question, answer))
        conn.commit()
        faq_id = cursor.lastrowid
        conn.close()
        
        text = f"✅ *FAQ добавлен успешно!*\n\n"
        text += f"❓ Вопрос: {question}\n\n"
        text += f"💬 Ответ: {answer}\n\n"
        text += f"🆔 ID: #{faq_id}"
        
        await update.message.reply_text(
            text,
            parse_mode='Markdown',
            reply_markup=get_admin_menu_keyboard()
        )
    
    except Exception as e:
        await update.message.reply_text(
            "❌ Ошибка в формате данных.\n\n"
            "Используйте: `/add_faq Вопрос | Ответ`\n\n"
            "Вопрос и ответ разделяются символом `|`",
            parse_mode='Markdown',
            reply_markup=get_admin_menu_keyboard()
        )

async def admin_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Справка для администраторов"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text(
            "❌ У вас нет прав для выполнения этой команды.",
            reply_markup=get_main_menu_keyboard()
        )
        return
    
    help_text = """
👨‍💼 *Команды администратора:*

📅 *Создание событий:*
`/create_event Название | Описание | YYYY-MM-DD`

❓ *Добавление FAQ:*
`/add_faq Вопрос | Ответ`

📊 *Статистика:*
Доступна через админ панель

*Примеры:*
`/create_event Лекция по AI | Интересная лекция | 2024-02-15`
`/add_faq Как поступить? | Подайте документы онлайн`

*Примечания:*
• Все части команд разделяются символом `|`
• Дата в формате YYYY-MM-DD
• События отображаются всем пользователям
• FAQ сразу становятся доступными
    """
    
    await update.message.reply_text(
        help_text,
        parse_mode='Markdown',
        reply_markup=get_admin_menu_keyboard()
    )
