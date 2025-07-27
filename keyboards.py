from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import db

def get_main_menu_keyboard():
    """Главное меню с inline кнопками"""
    keyboard = [
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("📝 Booking", callback_data="booking")],
        [InlineKeyboardButton("📅 События", callback_data="events")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_menu_keyboard():
    """Меню администратора"""
    keyboard = [
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("📝 Booking", callback_data="booking")],
        [InlineKeyboardButton("📅 События", callback_data="events")],
        [InlineKeyboardButton("👨‍💼 Админ панель", callback_data="admin_panel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_faq_keyboard():
    """Клавиатура с вопросами FAQ (inline кнопки)"""
    faq_list = db.get_all_faq()
    keyboard = []
    
    for faq_id, question, _ in faq_list:
        # Обрезаем длинные вопросы для кнопки
        button_text = question[:50] + "..." if len(question) > 50 else question
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"faq_{faq_id}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)

def get_faq_answer_keyboard():
    """Клавиатура для ответа FAQ"""
    keyboard = [
        [InlineKeyboardButton("⬅️ К вопросам", callback_data="faq")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_clubs_keyboard():
    """Клавиатура выбора клубов"""
    clubs = db.get_all_clubs()
    keyboard = []
    
    for club_id, name, _ in clubs:
        keyboard.append([InlineKeyboardButton(name, callback_data=f"club_{club_id}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)

def get_rooms_keyboard(club_id):
    """Клавиатура выбора комнат в клубе"""
    rooms = db.get_rooms_by_club(club_id)
    keyboard = []
    
    for room_id, number, room_type, capacity in rooms:
        button_text = f"Комната {number} ({room_type}, {capacity} мест)"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"room_{room_id}")])
    
    keyboard.append([
        InlineKeyboardButton("⬅️ К клубам", callback_data="booking"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")
    ])
    return InlineKeyboardMarkup(keyboard)

def get_time_slots_keyboard(room_id, date):
    """Клавиатура выбора времени"""
    # Доступные временные слоты
    time_slots = [
        "09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00",
        "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00",
        "17:00-18:00", "18:00-19:00", "19:00-20:00", "20:00-21:00"
    ]
    
    keyboard = []
    for i in range(0, len(time_slots), 2):
        row = []
        for j in range(2):
            if i + j < len(time_slots):
                slot = time_slots[i + j]
                callback_data = f"book_{room_id}_{date}_{slot}"
                row.append(InlineKeyboardButton(slot, callback_data=callback_data))
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton("⬅️ Назад", callback_data="booking"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")
    ])
    return InlineKeyboardMarkup(keyboard)

def get_date_keyboard(room_id):
    """Клавиатура выбора даты"""
    from datetime import datetime, timedelta
    
    keyboard = []
    today = datetime.now()
    
    # Показываем следующие 7 дней
    for i in range(7):
        date = today + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        display_date = date.strftime("%d.%m (%a)")
        
        keyboard.append([InlineKeyboardButton(display_date, callback_data=f"date_{room_id}_{date_str}")])
    
    keyboard.append([
        InlineKeyboardButton("⬅️ Назад", callback_data="booking"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")
    ])
    return InlineKeyboardMarkup(keyboard)

def get_events_keyboard():
    """Клавиатура событий"""
    events = db.get_all_events()
    keyboard = []
    
    for event_id, title, _, date in events:
        button_text = f"{title} ({date})" if date else title
        button_text = button_text[:50] + "..." if len(button_text) > 50 else button_text
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"event_{event_id}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)

def get_admin_panel_keyboard():
    """Панель администратора"""
    keyboard = [
        [InlineKeyboardButton("➕ Создать событие", callback_data="create_event")],
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard():
    """Простая кнопка назад"""
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
    return InlineKeyboardMarkup(keyboard)
