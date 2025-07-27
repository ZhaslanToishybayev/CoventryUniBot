# 🚀 Инструкция по развертыванию CoventryUniBot

## 📋 Быстрый старт

### 1. Получение токена бота
1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен

### 2. Получение ID администратора
1. Найдите [@userinfobot](https://t.me/userinfobot) в Telegram
2. Отправьте любое сообщение
3. Скопируйте ваш User ID

### 3. Настройка конфигурации
```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте .env файл
nano .env
```

Заполните файл `.env`:
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_IDS=123456789,987654321
```

### 4. Запуск бота
```bash
# Установка зависимостей
pip install -r requirements.txt

# Тестирование
python test_bot.py

# Запуск бота
python main.py
```

## 🔧 Расширенная настройка

### Добавление FAQ через команды
```bash
/add_faq Как поступить в университет? | Подайте документы через онлайн портал до 31 мая
```

### Создание событий
```bash
/create_event Лекция по AI | Интересная лекция о машинном обучении | 2024-02-15
```

### Команды администратора
- `/admin_help` - Справка для админов
- `/create_event` - Создать событие
- `/add_faq` - Добавить FAQ

## 🐳 Docker развертывание (опционально)

Создайте `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

Создайте `docker-compose.yml`:
```yaml
version: '3.8'
services:
  bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - ADMIN_IDS=${ADMIN_IDS}
    volumes:
      - ./bot_database.db:/app/bot_database.db
    restart: unless-stopped
```

## 🔍 Мониторинг и логи

Бот автоматически создает логи. Для просмотра в реальном времени:
```bash
python main.py 2>&1 | tee bot.log
```

## 🛠️ Устранение неполадок

### Проблема: "BOT_TOKEN не настроен"
**Решение:** Проверьте файл `.env` и убедитесь, что токен указан правильно

### Проблема: "Ошибка базы данных"
**Решение:** Удалите файл `bot_database.db` и перезапустите бота

### Проблема: Бот не отвечает
**Решение:** 
1. Проверьте интернет соединение
2. Убедитесь, что токен действителен
3. Проверьте логи на наличие ошибок

## 📊 Мониторинг работы

Используйте команду `/admin_help` для доступа к статистике:
- Количество пользователей
- Активные бронирования
- Количество FAQ и событий

## 🔄 Обновление бота

```bash
# Остановите бота (Ctrl+C)
git pull origin main
pip install -r requirements.txt
python test_bot.py
python main.py
```

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи бота
2. Запустите `python test_bot.py`
3. Убедитесь, что все зависимости установлены
4. Проверьте права доступа к файлам
