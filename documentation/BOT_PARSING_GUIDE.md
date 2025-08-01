# 🤖 Парсинг ботов в Telegram

## 🎯 Обзор

Парсинг ботов позволяет анализировать активность, команды и поведение Telegram ботов в группах. Это полезно для изучения функциональности ботов, анализа их популярности и понимания пользовательского взаимодействия.

## 📋 Что можно парсить у ботов

### ✅ **Доступные данные:**
- **Текстовые сообщения** - все сообщения от ботов
- **Команды** - `/start`, `/help`, `/settings` и другие
- **Кнопки** - inline keyboard в сообщениях ботов
- **Медиа файлы** - фото, видео, документы от ботов
- **Метаданные** - время, ID бота, статус верификации
- **Паттерны поведения** - частота сообщений, типы контента

### ❌ **Ограничения:**
- **Callback ответы** - нельзя отследить нажатия кнопок
- **Приватные данные** - внутренняя логика бота недоступна
- **Webhook данные** - информация о webhook недоступна

## 🔧 Настройка парсинга ботов

### В .env файле:
```env
# Включить парсинг ботов
PARSE_BOTS=true
PARSE_BOT_MESSAGES=true
PARSE_BOT_COMMANDS=true
PARSE_BOT_RESPONSES=true
PARSE_BOT_BUTTONS=true
PARSE_BOT_MEDIA=true

# Анализ ботов
ANALYZE_BOT_PATTERNS=true
ANALYZE_BOT_COMMANDS=true
ANALYZE_BOT_INTERACTIONS=true

# Фильтрация (опционально)
BOT_FILTER_ENABLED=false
ALLOWED_BOT_IDS=123456789,987654321
BLOCKED_BOT_IDS=111222333
```

## 📊 Структура данных ботов

### Пример JSON с данными бота:
```json
{
  "message_id": 12345,
  "chat_id": -1001234567890,
  "sender": {
    "id": 987654321,
    "name": "TestBot",
    "username": "@test_bot",
    "is_bot": true
  },
  "bot_info": {
    "bot_id": 987654321,
    "bot_name": "TestBot",
    "bot_username": "@test_bot",
    "is_verified": false,
    "is_scam": false,
    "is_fake": false
  },
  "content": {
    "text": "/start - Начать работу с ботом",
    "is_command": true,
    "command": "start",
    "buttons": [
      {
        "text": "Начать",
        "button_type": "callback",
        "data": "start_action"
      }
    ]
  },
  "metadata": {
    "timestamp": "2024-01-15T14:30:00Z",
    "message_type": "bot_command"
  }
}
```

## 🚀 Использование

### 1. **Запуск парсинга ботов:**
```python
# Включи парсинг ботов в .env
PARSE_BOTS=true
PARSE_BOT_MESSAGES=true

# Запусти парсинг
await parser.start_parsing(chat_id)
```

### 2. **Просмотр статистики ботов:**
```python
stats = parser.get_stats()
print(f"Сообщений от ботов: {stats['bot_messages']}")
print(f"Команд ботов: {stats['bot_commands']}")

# Анализ ботов
bot_analysis = parser.get_bot_analysis()
print(f"Всего ботов: {bot_analysis['total_bots']}")
```

### 3. **Анализ конкретного бота:**
```python
# Получи информацию о боте
if parsed_message.is_bot:
    bot_info = parsed_message.bot_info
    print(f"Бот: {bot_info['bot_name']}")
    print(f"Username: {bot_info['bot_username']}")
    print(f"Верифицирован: {bot_info['is_verified']}")
    
    # Проверь команду
    if await parser.is_bot_command(parsed_message.text):
        command = parser.extract_command(parsed_message.text)
        print(f"Команда: /{command}")
```

## 📈 Анализ данных ботов

### Статистика по ботам:
```python
def analyze_bots(messages):
    bot_stats = {}
    total_bot_messages = 0
    
    for message in messages:
        if message.get('is_bot'):
            bot_id = message['sender_id']
            bot_name = message['sender_name']
            
            if bot_id not in bot_stats:
                bot_stats[bot_id] = {
                    'name': bot_name,
                    'messages': 0,
                    'commands': [],
                    'buttons_used': 0,
                    'media_sent': 0
                }
            
            bot_stats[bot_id]['messages'] += 1
            total_bot_messages += 1
            
            # Анализируем команды
            if message.get('text', '').startswith('/'):
                command = message['text'].split()[0][1:]
                bot_stats[bot_id]['commands'].append(command)
            
            # Анализируем кнопки
            if message.get('buttons'):
                bot_stats[bot_id]['buttons_used'] += len(message['buttons'])
            
            # Анализируем медиа
            if message.get('media_type'):
                bot_stats[bot_id]['media_sent'] += 1
    
    return {
        'total_bot_messages': total_bot_messages,
        'bot_stats': bot_stats
    }
```

### Популярные команды ботов:
```python
def analyze_bot_commands(messages):
    command_stats = {}
    
    for message in messages:
        if message.get('is_bot') and message.get('text', '').startswith('/'):
            command = message['text'].split()[0][1:]
            command_stats[command] = command_stats.get(command, 0) + 1
    
    return dict(sorted(command_stats.items(), key=lambda x: x[1], reverse=True))
```

### Анализ активности ботов:
```python
def analyze_bot_activity(messages):
    bot_activity = {}
    
    for message in messages:
        if message.get('is_bot'):
            bot_id = message['sender_id']
            timestamp = message['timestamp']
            hour = timestamp.split('T')[1][:2]  # Извлекаем час
            
            if bot_id not in bot_activity:
                bot_activity[bot_id] = {}
            
            bot_activity[bot_id][hour] = bot_activity[bot_id].get(hour, 0) + 1
    
    return bot_activity
```

## 🔍 Примеры использования

### 1. **Анализ популярных ботов:**
```python
# Найди самых активных ботов
bot_messages = [msg for msg in messages if msg.get('is_bot')]
bot_counts = {}

for message in bot_messages:
    bot_name = message['sender_name']
    bot_counts[bot_name] = bot_counts.get(bot_name, 0) + 1

top_bots = sorted(bot_counts.items(), key=lambda x: x[1], reverse=True)[:5]
print("Топ-5 ботов:")
for bot, count in top_bots:
    print(f"- {bot}: {count} сообщений")
```

### 2. **Анализ команд ботов:**
```python
# Найди все команды ботов
bot_commands = []
for message in messages:
    if message.get('is_bot') and message.get('text', '').startswith('/'):
        command = message['text'].split()[0]
        bot_commands.append({
            'command': command,
            'bot': message['sender_name'],
            'timestamp': message['timestamp']
        })

print(f"Найдено команд: {len(bot_commands)}")
```

### 3. **Анализ кнопок ботов:**
```python
# Найди все кнопки от ботов
bot_buttons = []
for message in messages:
    if message.get('is_bot') and message.get('buttons'):
        for button in message['buttons']:
            bot_buttons.append({
                'text': button['text'],
                'type': button['button_type'],
                'bot': message['sender_name']
            })

print(f"Кнопок от ботов: {len(bot_buttons)}")
```

### 4. **Анализ временных паттернов:**
```python
# Анализируй активность ботов по времени
hourly_activity = {}
for message in messages:
    if message.get('is_bot'):
        hour = message['timestamp'].split('T')[1][:2]
        hourly_activity[hour] = hourly_activity.get(hour, 0) + 1

print("Активность ботов по часам:")
for hour in sorted(hourly_activity.keys()):
    print(f"{hour}:00 - {hourly_activity[hour]} сообщений")
```

## ⚠️ Ограничения и этика

### 1. **Технические ограничения:**
- Парсинг только новых сообщений (не исторических)
- Нет доступа к callback данным
- Ограничения API Telegram

### 2. **Этические соображения:**
- Получи разрешение на парсинг
- Не используй данные для спама
- Соблюдай правила группы
- Уважай приватность ботов

### 3. **Права доступа:**
- ✅ Достаточно быть участником группы
- ❌ НЕ нужно быть администратором
- ✅ Нужны права на чтение сообщений

## 🛠️ Отладка и мониторинг

### Проверка парсинга ботов:
```python
# Включи отладочный режим
LOG_LEVEL=DEBUG

# Проверь логи
docker-compose logs -f telegram-userbot
```

### Команды для анализа:
```python
# Статус парсинга
.parsing_status

# Анализ ботов
.bot_analysis

# Экспорт данных
.parsing_export
```

## 📊 Экспорт и анализ

### CSV экспорт с данными ботов:
```python
# Экспортируй данные с информацией о ботах
await parser.export_to_csv("data/bot_analysis.csv")
```

### JSON анализ:
```python
# Получи анализ ботов
bot_analysis = parser.get_bot_analysis()

# Сохрани в файл
with open("data/bot_analysis.json", "w") as f:
    json.dump(bot_analysis, f, indent=2)
```

## 🎯 Лучшие практики

### 1. **Фильтрация ботов:**
```python
# Фильтруй только нужных ботов
def filter_bots_by_name(messages, bot_names):
    filtered = []
    for message in messages:
        if message.get('is_bot'):
            bot_name = message['sender_name']
            if bot_name in bot_names:
                filtered.append(message)
    return filtered
```

### 2. **Анализ паттернов:**
```python
# Анализируй паттерны команд
def analyze_command_patterns(messages):
    patterns = {}
    for message in messages:
        if message.get('is_bot') and message.get('text', '').startswith('/'):
            command = message['text'].split()[0]
            bot_name = message['sender_name']
            
            if bot_name not in patterns:
                patterns[bot_name] = []
            patterns[bot_name].append(command)
    
    return patterns
```

### 3. **Визуализация:**
```python
# Создай график активности ботов
import matplotlib.pyplot as plt

def plot_bot_activity(bot_stats):
    bots = list(bot_stats.keys())
    messages = [bot_stats[bot]['messages'] for bot in bots]
    
    plt.figure(figsize=(12, 6))
    plt.bar(bots, messages)
    plt.title('Активность ботов')
    plt.ylabel('Количество сообщений')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('bot_activity.png')
```

## 🎯 Итог

Парсинг ботов позволяет:
- ✅ **Изучать функциональность** - понимать возможности ботов
- ✅ **Анализировать популярность** - определять самые активные боты
- ✅ **Исследовать команды** - изучать доступные команды
- ✅ **Отслеживать паттерны** - анализировать поведение ботов
- ✅ **Создавать отчеты** - генерировать статистику по ботам

**Важно:** Всегда получай разрешение на парсинг и используй данные этично! 🤖🔒 