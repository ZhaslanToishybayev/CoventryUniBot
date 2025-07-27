#!/usr/bin/env python3
"""
Тестовый скрипт для проверки функциональности бота
"""

import sys
import os
from database import db

def test_database():
    """Тестирование базы данных"""
    print("🔄 Тестирование базы данных...")
    
    try:
        # Тестируем FAQ
        faq_list = db.get_all_faq()
        print(f"✅ FAQ записей: {len(faq_list)}")
        
        # Тестируем клубы
        clubs = db.get_all_clubs()
        print(f"✅ Клубов: {len(clubs)}")
        
        # Тестируем комнаты
        for club_id, club_name, _ in clubs:
            rooms = db.get_rooms_by_club(club_id)
            print(f"✅ {club_name}: {len(rooms)} комнат")
        
        # Тестируем события
        events = db.get_all_events()
        print(f"✅ События: {len(events)}")
        
        print("✅ База данных работает корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка базы данных: {e}")
        return False

def test_config():
    """Тестирование конфигурации"""
    print("🔄 Тестирование конфигурации...")
    
    try:
        from config import BOT_TOKEN, ADMIN_IDS, MESSAGES, CLUBS
        
        if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
            print("⚠️  Предупреждение: BOT_TOKEN не настроен")
        else:
            print("✅ BOT_TOKEN настроен")
        
        print(f"✅ Администраторов: {len(ADMIN_IDS)}")
        print(f"✅ Сообщений: {len(MESSAGES)}")
        print(f"✅ Клубов в конфиге: {len(CLUBS)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def test_keyboards():
    """Тестирование клавиатур"""
    print("🔄 Тестирование клавиатур...")
    
    try:
        from keyboards import (
            get_main_menu_keyboard, get_admin_menu_keyboard,
            get_faq_keyboard, get_clubs_keyboard
        )
        
        # Тестируем основные клавиатуры
        main_kb = get_main_menu_keyboard()
        admin_kb = get_admin_menu_keyboard()
        faq_kb = get_faq_keyboard()
        clubs_kb = get_clubs_keyboard()
        
        print("✅ Все клавиатуры создаются без ошибок")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка клавиатур: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Запуск тестов CoventryUniBot\n")
    
    tests = [
        ("Конфигурация", test_config),
        ("База данных", test_database),
        ("Клавиатуры", test_keyboards)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Результаты: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены успешно!")
        print("🚀 Бот готов к запуску!")
    else:
        print("⚠️  Некоторые тесты не пройдены")
        print("🔧 Проверьте конфигурацию и исправьте ошибки")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
