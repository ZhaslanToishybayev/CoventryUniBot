import sqlite3
import asyncio
from datetime import datetime
from config import DATABASE_PATH, CLUBS

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица FAQ
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faq (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица клубов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clubs (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT
            )
        ''')
        
        # Таблица комнат
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                club_id INTEGER,
                number TEXT NOT NULL,
                type TEXT,
                capacity INTEGER,
                FOREIGN KEY (club_id) REFERENCES clubs (id)
            )
        ''')
        
        # Таблица бронирований
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (room_id) REFERENCES rooms (id)
            )
        ''')
        
        # Таблица событий
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                date TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        
        # Заполнение начальными данными
        self.populate_initial_data(cursor)
        conn.commit()
        conn.close()
    
    def populate_initial_data(self, cursor):
        """Заполнение начальными данными"""
        # Добавляем клубы
        for club in CLUBS:
            cursor.execute('INSERT OR IGNORE INTO clubs (id, name, description) VALUES (?, ?, ?)',
                         (club['id'], club['name'], club['description']))
        
        # Добавляем комнаты для каждого клуба
        rooms_data = [
            (1, 'A101', 'Большая комната', 20),
            (1, 'A102', 'Малая комната', 10),
            (2, 'B201', 'Студия звукозаписи', 8),
            (2, 'B202', 'Репетиционная', 15),
            (3, 'C301', 'Компьютерный класс', 25),
            (3, 'C302', 'Лекционная', 30),
            (4, 'D401', 'Мастерская', 12),
            (4, 'D402', 'Выставочный зал', 50)
        ]
        
        for club_id, number, room_type, capacity in rooms_data:
            cursor.execute('INSERT OR IGNORE INTO rooms (club_id, number, type, capacity) VALUES (?, ?, ?, ?)',
                         (club_id, number, room_type, capacity))
        
        # Добавляем FAQ
        faq_data = [
            ('Какие документы нужны для поступления?', 'Для поступления необходимы: паспорт, диплом о предыдущем образовании, сертификат IELTS (минимум 6.0), мотивационное письмо.'),
            ('Сколько стоит обучение?', 'Стоимость обучения зависит от программы. Бакалавриат: £14,000-16,000 в год, магистратура: £15,000-18,000 в год.'),
            ('Есть ли общежития?', 'Да, университет предоставляет различные варианты размещения: от комнат в общежитии до отдельных квартир.'),
            ('Как подать заявку на стипендию?', 'Заявки на стипендии подаются через портал университета. Доступны академические стипендии и стипендии для иностранных студентов.'),
            ('Какие клубы и общества есть в университете?', 'В университете более 100 клубов: спортивные, академические, культурные. Можете присоединиться к любому или создать свой.')
        ]
        
        for question, answer in faq_data:
            cursor.execute('INSERT OR IGNORE INTO faq (question, answer) VALUES (?, ?)',
                         (question, answer))
    
    # FAQ методы
    def get_all_faq(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, question, answer FROM faq ORDER BY id')
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_faq_by_id(self, faq_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, question, answer FROM faq WHERE id = ?', (faq_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    # Клубы и комнаты
    def get_all_clubs(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, description FROM clubs ORDER BY id')
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_rooms_by_club(self, club_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, number, type, capacity FROM rooms WHERE club_id = ? ORDER BY number', (club_id,))
        result = cursor.fetchall()
        conn.close()
        return result
    
    # Бронирования
    def create_booking(self, user_id, room_id, date, start_time, end_time):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Проверяем пересечения
        cursor.execute('''
            SELECT id FROM bookings 
            WHERE room_id = ? AND date = ? AND status = 'active'
            AND ((start_time <= ? AND end_time > ?) OR (start_time < ? AND end_time >= ?))
        ''', (room_id, date, start_time, start_time, end_time, end_time))
        
        if cursor.fetchone():
            conn.close()
            return False  # Пересечение найдено
        
        cursor.execute('''
            INSERT INTO bookings (user_id, room_id, date, start_time, end_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, room_id, date, start_time, end_time))
        
        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()
        return booking_id
    
    def get_user_bookings(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.id, r.number, c.name, b.date, b.start_time, b.end_time, b.status
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            JOIN clubs c ON r.club_id = c.id
            WHERE b.user_id = ? AND b.status = 'active'
            ORDER BY b.date, b.start_time
        ''', (user_id,))
        result = cursor.fetchall()
        conn.close()
        return result
    
    # События
    def create_event(self, title, description, date, created_by):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (title, description, date, created_by)
            VALUES (?, ?, ?, ?)
        ''', (title, description, date, created_by))
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()
        return event_id
    
    def get_all_events(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, description, date FROM events ORDER BY date DESC')
        result = cursor.fetchall()
        conn.close()
        return result

# Глобальный экземпляр базы данных
db = Database()
