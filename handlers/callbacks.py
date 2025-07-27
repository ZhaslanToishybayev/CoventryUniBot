from telegram import Update
from telegram.ext import ContextTypes
from config import MESSAGES, ADMIN_IDS
from keyboards import (
    get_main_menu_keyboard, get_admin_menu_keyboard, get_faq_keyboard, 
    get_faq_answer_keyboard, get_clubs_keyboard, get_rooms_keyboard,
    get_date_keyboard, get_time_slots_keyboard, get_events_keyboard,
    get_admin_panel_keyboard
)
from database import db

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главный обработчик callback запросов"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    
    # Определяем клавиатуру в зависимости от пользователя
    main_keyboard = get_admin_menu_keyboard() if user_id in ADMIN_IDS else get_main_menu_keyboard()
    
    try:
        if data == "back_to_main":
            await query.edit_message_text(
                MESSAGES['start'],
                reply_markup=main_keyboard
            )
        
        elif data == "faq":
            await query.edit_message_text(
                MESSAGES['faq_title'],
                reply_markup=get_faq_keyboard()
            )
        
        elif data.startswith("faq_"):
            faq_id = int(data.split("_")[1])
            faq_data = db.get_faq_by_id(faq_id)
            
            if faq_data:
                _, question, answer = faq_data
                text = f"❓ *{question}*\n\n{answer}"
                await query.edit_message_text(
                    text,
                    parse_mode='Markdown',
                    reply_markup=get_faq_answer_keyboard()
                )
        
        elif data == "booking":
            await query.edit_message_text(
                MESSAGES['booking_title'],
                reply_markup=get_clubs_keyboard()
            )
        
        elif data.startswith("club_"):
            club_id = int(data.split("_")[1])
            clubs = db.get_all_clubs()
            club_name = next((name for cid, name, _ in clubs if cid == club_id), "Клуб")
            
            text = f"📝 *{club_name}*\n\nВыберите комнату:"
            await query.edit_message_text(
                text,
                parse_mode='Markdown',
                reply_markup=get_rooms_keyboard(club_id)
            )
        
        elif data.startswith("room_"):
            room_id = int(data.split("_")[1])
            text = "📅 Выберите дату:"
            await query.edit_message_text(
                text,
                reply_markup=get_date_keyboard(room_id)
            )
        
        elif data.startswith("date_"):
            parts = data.split("_")
            room_id = int(parts[1])
            date = parts[2]
            
            text = f"⏰ Выберите время для {date}:"
            await query.edit_message_text(
                text,
                reply_markup=get_time_slots_keyboard(room_id, date)
            )
        
        elif data.startswith("book_"):
            await handle_booking(query, data)
        
        elif data == "events":
            await query.edit_message_text(
                "📅 *События университета:*",
                parse_mode='Markdown',
                reply_markup=get_events_keyboard()
            )
        
        elif data.startswith("event_"):
            event_id = int(data.split("_")[1])
            events = db.get_all_events()
            event = next((e for e in events if e[0] == event_id), None)
            
            if event:
                _, title, description, date = event
                text = f"📅 *{title}*\n\n"
                if description:
                    text += f"{description}\n\n"
                if date:
                    text += f"📆 Дата: {date}"
                
                await query.edit_message_text(
                    text,
                    parse_mode='Markdown',
                    reply_markup=get_events_keyboard()
                )
        
        elif data == "admin_panel" and user_id in ADMIN_IDS:
            await query.edit_message_text(
                MESSAGES['admin_panel'],
                reply_markup=get_admin_panel_keyboard()
            )
        
        elif data == "create_event" and user_id in ADMIN_IDS:
            await query.edit_message_text(
                "📝 Для создания события отправьте сообщение в формате:\n\n"
                "`/create_event Название события | Описание | YYYY-MM-DD`\n\n"
                "Пример:\n"
                "`/create_event Лекция по AI | Интересная лекция о машинном обучении | 2024-02-15`",
                parse_mode='Markdown',
                reply_markup=get_admin_panel_keyboard()
            )
        
        elif data == "admin_stats" and user_id in ADMIN_IDS:
            await show_admin_stats(query)
    
    except Exception as e:
        await query.edit_message_text(
            "❌ Произошла ошибка. Попробуйте еще раз.",
            reply_markup=main_keyboard
        )

async def handle_booking(query, data):
    """Обработка бронирования"""
    try:
        parts = data.split("_")
        room_id = int(parts[1])
        date = parts[2]
        time_slot = parts[3]
        
        start_time, end_time = time_slot.split("-")
        user_id = query.from_user.id
        
        booking_id = db.create_booking(user_id, room_id, date, start_time, end_time)
        
        if booking_id:
            # Получаем информацию о комнате и клубе
            rooms = db.get_rooms_by_club(None)  # Получаем все комнаты
            room_info = None
            for room in rooms:
                if room[0] == room_id:
                    room_info = room
                    break
            
            clubs = db.get_all_clubs()
            club_name = "Клуб"
            if room_info:
                for club in clubs:
                    club_rooms = db.get_rooms_by_club(club[0])
                    if any(r[0] == room_id for r in club_rooms):
                        club_name = club[1]
                        break
            
            text = f"✅ *Бронь подтверждена!*\n\n"
            text += f"🏢 Клуб: {club_name}\n"
            text += f"🚪 Комната: {room_info[1] if room_info else 'N/A'}\n"
            text += f"📅 Дата: {date}\n"
            text += f"⏰ Время: {time_slot}\n\n"
            text += f"ID брони: #{booking_id}"
            
            await query.edit_message_text(
                text,
                parse_mode='Markdown',
                reply_markup=get_main_menu_keyboard()
            )
        else:
            await query.edit_message_text(
                "❌ К сожалению, это время уже занято. Выберите другое время.",
                reply_markup=get_main_menu_keyboard()
            )
    
    except Exception as e:
        await query.edit_message_text(
            "❌ Ошибка при бронировании. Попробуйте еще раз.",
            reply_markup=get_main_menu_keyboard()
        )

async def show_admin_stats(query):
    """Показать статистику для админа"""
    try:
        # Получаем статистику из базы
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Количество активных бронирований
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'active'")
        active_bookings = cursor.fetchone()[0]
        
        # Количество FAQ
        cursor.execute("SELECT COUNT(*) FROM faq")
        faq_count = cursor.fetchone()[0]
        
        # Количество событий
        cursor.execute("SELECT COUNT(*) FROM events")
        events_count = cursor.fetchone()[0]
        
        # Количество уникальных пользователей
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM bookings")
        unique_users = cursor.fetchone()[0]
        
        conn.close()
        
        text = f"📊 *Статистика бота:*\n\n"
        text += f"👥 Уникальных пользователей: {unique_users}\n"
        text += f"📝 Активных бронирований: {active_bookings}\n"
        text += f"❓ Вопросов в FAQ: {faq_count}\n"
        text += f"📅 Событий: {events_count}\n"
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=get_admin_panel_keyboard()
        )
    
    except Exception as e:
        await query.edit_message_text(
            "❌ Ошибка при получении статистики.",
            reply_markup=get_admin_panel_keyboard()
        )
