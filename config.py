import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip()]

# Database configuration
DATABASE_PATH = 'bot_database.db'

# Messages
MESSAGES = {
    'start': '🎓 Добро пожаловать в бот Coventry University!\n\nВыберите нужный раздел:',
    'faq_title': '❓ Часто задаваемые вопросы\n\nВыберите интересующий вас вопрос:',
    'booking_title': '📝 Бронирование комнат\n\nВыберите клуб:',
    'booking_confirmed': '✅ Бронь подтверждена!',
    'booking_error': '❌ Ошибка при бронировании. Попробуйте еще раз.',
    'admin_panel': '👨‍💼 Панель администратора',
    'event_created': '📅 Событие успешно создано!',
    'back_to_menu': '⬅️ Главное меню'
}

# Clubs configuration
CLUBS = [
    {'id': 1, 'name': 'Chess Club', 'description': 'Шахматный клуб'},
    {'id': 2, 'name': 'Music Club', 'description': 'Музыкальный клуб'},
    {'id': 3, 'name': 'IT Club', 'description': 'IT клуб'},
    {'id': 4, 'name': 'Art Club', 'description': 'Художественный клуб'}
]
